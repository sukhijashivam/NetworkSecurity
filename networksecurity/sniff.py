# networksecurity/sniff.py
from scapy.all import sniff, Raw
import re

def http_packet_callback(pkt):
    if pkt.haslayer(Raw):
        payload = bytes(pkt[Raw].load).decode('utf-8', errors='ignore')
        m = re.search(r"GET\s+([^\s]+)\s+HTTP/1\.\d", payload)
        host = re.search(r"Host:\s*([^\r\n]+)", payload)
        if m and host:
            url = "http://" + host.group(1).strip() + m.group(1)
            print("Captured URL:", url)

def start_sniff():
    sniff(filter="tcp port 80", prn=http_packet_callback, store=0)
