from scapy.all import sniff, Ether, IP, TCP, UDP
from scapy.layers.inet import ICMP
from scapy.layers.dns import DNS


def packet_callback(packet):
    if TCP in packet and IP in packet and Ether in packet:
        # Extract MAC, IP, and port details.
        mac_src = packet[Ether].src
        mac_dst = packet[Ether].dst
        ip_src = packet[IP].src
        ip_dst = packet[IP].dst
        tcp_sport = packet[TCP].sport
        tcp_dport = packet[TCP].dport

        # Print packet details
        print(f"MAC: {mac_src} -> {mac_dst}, IP: {ip_src}:{tcp_sport} -> {ip_dst}:{tcp_dport}")

# Starts capturing packets on the specified interface using Scapy.
def start_sniffing():
    print("Starting packet sniffing with Scapy...")
    sniff(prn=packet_callback, filter="tcp", store=0, iface="eth0")

# Extracts source and destination MAC addresses from Ethernet layer.
def parse_ethernet(packet):
    return {
        'Source MAC': packet[Ether].src,
        'Destination MAC': packet[Ether].dst,
    }

# Extracts source/destination IP and protocol from IP layer.
def parse_ip(packet):
    return {
        'Source IP': packet[IP].src,
        'Destination IP': packet[IP].dst,
        'Protocol': packet[IP].proto
    }


def packet_callback(packet):
    if IP in packet and Ether in packet:
        eth_info = parse_ethernet(packet)
        ip_info = parse_ip(packet)

        print(f"Ethernet: {eth_info}")
        print(f"IP: {ip_info}")

def start_sniffing():
    print("Starting packet sniffing with Scapy...")
    sniff(prn=packet_callback, filter="ip", store=0, iface="eth0")

# Extracts TCP flags (SYN, ACK, FIN, RST) using bitwise operations.
def parse_tcp_flags(packet):
    flags = packet[TCP].flags
    return {
        'SYN': flags & 0x02 != 0,
        'ACK': flags & 0x10 != 0,
        'FIN': flags & 0x01 != 0,
        'RST': flags & 0x04 != 0
    }

# Extracts TCP source port, destination port, and flag details.
def parse_tcp(packet):
    return {
        'Source Port': packet[TCP].sport,
        'Destination Port': packet[TCP].dport,
        'Flags': parse_tcp_flags(packet)
    }

# Extracts UDP source port, destination port, and packet length.
def parse_udp(packet):
    return {
        'Source Port': packet[UDP].sport,
        'Destination Port': packet[UDP].dport,
        'Length': packet[UDP].len
    }


def packet_callback(packet):
    if TCP in packet:
        tcp_info = parse_tcp(packet)
        print(f"TCP Info: {tcp_info}")
    elif UDP in packet:
        udp_info = parse_udp(packet)
        print(f"UDP Info: {udp_info}")

# Extracts ICMP type, code, and checksum values.
def parse_icmp(packet):
    return {
        'Type': packet[ICMP].type,
        'Code': packet[ICMP].code,
        'Checksum': packet[ICMP].chksum
    }

# Extracts HTTP payload data from TCP packets on port 80.
def packet_callback(packet):
    if ICMP in packet:
        icmp_info = parse_icmp(packet)
        print(f"ICMP Info: {icmp_info}")

# Extracts DNS header details like transaction ID and record counts.
def parse_http(packet):
    try:
        payload = bytes(packet[TCP].payload).decode('utf-8')
        return payload if "HTTP" in payload else None
    except UnicodeDecodeError:
        return None

def packet_callback(packet):
    if TCP in packet and (packet[TCP].sport == 80 or packet[TCP].dport == 80):
        http_data = parse_http(packet)
        if http_data:
            print(f"HTTP Data: {http_data[:100]}")

# Handles each captured packet and decides which parser to apply.
def parse_dns(packet):
    if DNS in packet:
        return {
            'Transaction ID': packet[DNS].id,
            'Questions': packet[DNS].qdcount,
            'Answer RRs': packet[DNS].ancount,
            'Authority RRs': packet[DNS].nscount,
            'Additional RRs': packet[DNS].arcount
        }

def packet_callback(packet):
    if DNS in packet:
        dns_info = parse_dns(packet)
        print(f"DNS Info: {dns_info}")

if __name__ == "__main__":
    start_sniffing()
