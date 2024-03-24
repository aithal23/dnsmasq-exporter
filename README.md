# dnsmasq-exporter

A simply python script which continuously parses DNSMasq logs and emits DNS query stats on port 8000 by default. 

Accepts 2 arguments:

* `--log-file-path` DNSMasq logs file path
* `--port` Port to expose metrics on 

# Metrics

## dnsmasq_dns_queries

* Name: dnsmasq_dns_queries
* Labels: ['source_port', 'action', 'source_address', 'domain', 'ip']
* Description: Metric for emitting DNS query stats

## dnsmasq_parsing_failures

* Name: dnsmasq_parsing_failures
* Labels: []
* Description: Metric for emitting DNSMasq query parsing failures

# Installation and usage

## Standalone

* Install python3 
* Run `pip install -r requirements.txt` 
* Run `python3 src/dnsmasq_exporter.py` (by default it reads from /var/log/dnsmasq.log and hosts the webserver on port 8000)

## As systemd service

* Modify `dnsmasq_exporter.service` as per your needs. 
* Copy the file to `/etc/systemd/system/` or any directory where your systemd daemon reads from. 
* Run `systemctl daemon-reload && systemctl enable dnsmasq_exporter.service && systemctl start dnsmasq_exporter.service`

# Troubleshooting

## Unable to open file exception

Try running the script with sudo or change the ownership of the log files you are trying to access. 

## Address already in use exception

Another service is already using the port you specified to host the metrics. Try using another port. 