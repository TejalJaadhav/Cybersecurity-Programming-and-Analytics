from scapy.all import sniff, IP, TCP
from collections import defaultdict
import argparse
import time
import csv

# Store all ports contacted by each source IP.
port_activity = defaultdict(list)

PORTS_PER_SECOND = 5
PORTS_PER_MINUTE = 100
PORTS_PER_5MIN = 300

# Time windows.
WINDOW_SECOND = 1
WINDOW_MINUTE = 60
WINDOW_5MIN = 300


# Function to check CSV log to see if this IP scanned before.
def check_csv_history(src_ip):

    try:
        with open("traffic_log.csv", "r") as file:

            reader = csv.reader(file)
            next(reader)  # skip header

            for row in reader:

                if len(row) < 6:
                    continue

                timestamp, src, dst, port, protocol, flag = row

                if src == src_ip and protocol == "TCP":
                    return True

    except FileNotFoundError:
        pass

    return False


# Function tocheck number of unique ports contacted.
def detect_port_scan(src_ip, current_time):

    ports = port_activity[src_ip]

    # Collect ports contacted in each time window.
    ports_last_sec = {p for t, p in ports if current_time - t <= WINDOW_SECOND}
    ports_last_min = {p for t, p in ports if current_time - t <= WINDOW_MINUTE}
    ports_last_5min = {p for t, p in ports if current_time - t <= WINDOW_5MIN}

    reason = None
    rate = 0

    # To check thresholds.
    if len(ports_last_sec) > PORTS_PER_SECOND:
        reason = "Exceeded 5 ports/sec threshold"
        rate = len(ports_last_sec)

    elif len(ports_last_min) > PORTS_PER_MINUTE:
        reason = "Exceeded 100 ports/min threshold"
        rate = len(ports_last_min)

    elif len(ports_last_5min) > PORTS_PER_5MIN:
        reason = "Exceeded 300 ports/5min threshold"
        rate = len(ports_last_5min)

    if reason:

        previous = check_csv_history(src_ip)

        print("\nALERT: Port Scanner Detected!")
        print(f"Source: {src_ip} | Fan-Out Rate: {rate} ports | Reason: {reason}")

        if previous:
            print("Previous port scan detected in last 30 minutes: YES\n")
        else:
            print("Previous port scan detected in last 30 minutes: NO\n")


# Function to called for every captured packet.
def packet_callback(packet):

    if IP not in packet:
        return

    # Check only TCP SYN packets.
    if TCP in packet and packet[TCP].flags == "S":

        src_ip = packet[IP].src
        dst_port = packet[TCP].dport
        current_time = time.time()

        # Store the time and port.
        port_activity[src_ip].append((current_time, dst_port))

        detect_port_scan(src_ip, current_time)


# Function to start the sniffer.
def start_sniffer(interface):

    print("Port Scanner Detector Running...\n")

    sniff(
        iface=interface,
        prn=packet_callback,
        store=0
    )


def main():

    parser = argparse.ArgumentParser()

    # Network interface argument.
    parser.add_argument("-i", "--interface", required=True)

    args = parser.parse_args()

    start_sniffer(args.interface)


if __name__ == "__main__":
    main()