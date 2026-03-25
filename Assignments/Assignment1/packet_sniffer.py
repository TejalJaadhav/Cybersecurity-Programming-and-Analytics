from scapy.all import sniff, IP, TCP, UDP, ICMP
from datetime import datetime
from collections import deque
import csv
import argparse
import time

packet_memory = deque() # deque(): To keep packets from the last 10 minutes.

csv_buffer = [] # Temporary buffer that holds packets before writing to CSV.


MEMORY_LIMIT = 600 # Memory limit: 10 minutes = 600 seconds

output_file = None

last_write_time = time.time() # To control writing packets to CSV every few seconds.


# Function to extracts the required fields from each packet.
def extract_packet_info(packet):

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    src_ip = packet[IP].src
    dst_ip = packet[IP].dst

    protocol = "-"
    dst_port = "-"
    tcp_flags = "-"

    if TCP in packet:
        protocol = "TCP"
        dst_port = packet[TCP].dport

        tcp_flags = packet.sprintf("%TCP.flags%")  # Convert TCP flags to readable format.

    elif UDP in packet:
        protocol = "UDP"
        dst_port = packet[UDP].dport

    elif ICMP in packet:
        protocol = "ICMP"

        # ICMP type 8 = ping request.
        if packet[ICMP].type == 8:
            tcp_flags = "ECHO_REQUEST"

        # ICMP type 0 = ping reply.
        elif packet[ICMP].type == 0:
            tcp_flags = "ECHO_REPLY"

        else:
            tcp_flags = f"TYPE_{packet[ICMP].type}"

    return [timestamp, src_ip, dst_ip, dst_port, protocol, tcp_flags]  # Returns all fields in required format.


# Function to run every time a packet is captured.
def packet_callback(packet):

    global last_write_time

    # Ignore packets that do not have an IP layer.
    if IP not in packet:
        return

    packet_info = extract_packet_info(packet)   # Extract required information.

    current_time = time.time()

    packet_memory.append((current_time, packet_info))   # Store packet in memory.

    csv_buffer.append(packet_info)  # Store packet in CSV buffer.

    # Remove packets older than 10 minutes.
    while packet_memory and current_time - packet_memory[0][0] > MEMORY_LIMIT:
        packet_memory.popleft()

    print(",".join(map(str, packet_info)))

    # Writes buffered packets to CSV every 10 seconds.
    if current_time - last_write_time >= 10:
        write_csv()
        last_write_time = current_time


# Function to writes packets from buffer to CSV file.
def write_csv():

    global csv_buffer

    if output_file is None:
        return

    if len(csv_buffer) == 0:
        return

    # Open CSV file and append packet rows.
    with open(output_file, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(csv_buffer)

    # Clear buffer after writing.
    csv_buffer = []


# Functio to start packet sniffing.
def start_sniffer(interface):
    print("timestamp,src_ip,dst_ip,dst_port,protocol,tcp_flags")

    # Sniff packets on selected interface.
    sniff(iface=interface, prn=packet_callback, store=0)


def main():

    global output_file

    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--interface", required=True)   # Argument for network interface.

    parser.add_argument("-o", "--output")   # Optional argument for CSV output file.

    args = parser.parse_args()

    output_file = args.output

    # Create CSV file and write header.
    if output_file:
        with open(output_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(
                ["timestamp", "src_ip", "dst_ip", "dst_port", "protocol", "tcp_flags"]
            )

    start_sniffer(args.interface)  # Start capturing packets.


if __name__ == "__main__":
    main()