import time
import argparse
from prometheus_client import start_http_server, Gauge, Counter


log_file = '/var/log/dnsmasq.log'

DNS_QUERIES = Gauge('dnsmasq_dns_queries', 'Number of DNS queries', ['source_port', 'action', 'source_address', 'domain', 'ip'])
PARSE_FAILURES = ('dnsmasq_parsing_failures', 'Number of log parsing failures')
# Function to parse the log line and extract relevant information
def parse_log_line(log_line):
    parts = log_line.split()

    try:
        ip_addr_split = parts[5].split("/")
        data = {
            'timestamp': ' '.join(parts[:3]),
            'process': parts[3],
            'sequence_number': parts[4],
            'ip_address': ip_addr_split[0],
            'port': ip_addr_split[1],
            'log_type': parts[6],
            'domain': parts[7],
            'ip': parts[9],
        }
    except Exception as ex:
        print(log_line)
        print(parts)
        PARSE_FAILURES.inc()
        data = {}

    return data

# tail implementation in python
def follow(thefile):
    thefile.seek(0,2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

# Function to read the log file and parse the log lines
def read_log_file(file_path):
    ip_query_list = []
    with open(file_path, 'r') as file:
        lines = follow(file)
        for line in lines:
            if 'query[' in line or 'forwarded' in line or 'reply' in line or 'cached' in line:
                try:
                    log_data = parse_log_line(line)
                    DNS_QUERIES.labels(
                        source_port=log_data["port"],
                        action=log_data["log_type"],
                        source_address=log_data["ip_address"],
                        domain=log_data["domain"],
                        ip=log_data["ip"]
                    ).inc()
                except Exception as ex:
                    print(line)
                    PARSE_FAILURES.inc()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--log-file-path", help="DNSMasq log file path", default="/var/log/dnsmasq.log")
    parser.add_argument("-p", "--port", help="Port to expose metrics on", default=8000)
    args = parser.parse_args()

    start_http_server(args.port)
    ip_query_map = read_log_file(args.log_file_path)
    