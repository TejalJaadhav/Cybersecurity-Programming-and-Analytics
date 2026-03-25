from scapy.all import sniff, IP, TCP
from collections import defaultdict, deque
import argparse
import time
import csv

packet_memory = deque() # Store packets from the last 10 minutes.


syn_rate = defaultdict(lambda: defaultdict(int)) # Dictionary to count SYN packets per second for each IP.

flood_history = defaultdict(list) # Store times when floods were detected.

MEMORY_LIMIT = 600        # 10 minutes.
FLOOD_THRESHOLD = 100     # More than 100 SYN packets per second.
FLOOD_DURATION = 3        # Must last 3 seconds
HISTORY_WINDOW = 1800     # Check last 30 minutes.


# Function to check CSV log file to see if this IP flooded before.
def check_csv_history(src_ip):

    try:
        with open("traffic_log.csv", "r") as file:

            reader = csv.reader(file)
            next(reader) 

            for row in reader:

                # Skip bad rows if any.
                if len(row) < 6:
                    continue

                timestamp, src, dst, port, protocol, flag = row

                # Check if this IP previously sent SYN packets.
                if src == src_ip and protocol == "TCP" and flag == "S":
                    return True

    except FileNotFoundError:
        pass

    return False


# Function to check SYN packet rate for possible flood.
def detect_syn_flood(src_ip, current_time):

    second = int(current_time)

    syn_rate[src_ip][second] += 1  # Increase packet count for this IP in this second.

    counts = []

    # Get SYN counts for last 3 seconds.
    for i in range(FLOOD_DURATION):
        counts.append(syn_rate[src_ip].get(second - i, 0))

    if all(count > FLOOD_THRESHOLD for count in counts):

        # Check if flood was detected recently.
        recent_floods = [
            t for t in flood_history[src_ip]
            if current_time - t < HISTORY_WINDOW
        ]

        previous_in_csv = check_csv_history(src_ip)
        if recent_floods or previous_in_csv:

            avg_rate = sum(counts) // FLOOD_DURATION

            print("\nALERT: SYN Flood Detected!")
            print(f"Source: {src_ip} | Rate: {avg_rate} SYN packets/sec | Duration: 3 sec")

            if previous_in_csv:
                print("Previous SYN flood detected in last 30 minutes: YES\n")
            else:
                print("Previous SYN flood detected in last 30 minutes: NO\n")

        # Store detection time.
        flood_history[src_ip].append(current_time)


# Function to called every time a packet is captured.
def packet_callback(packet):

    if IP not in packet:
        return

    # Check if packet is a TCP SYN packet.
    if TCP in packet and packet[TCP].flags == "S":

        src_ip = packet[IP].src
        current_time = time.time()

        packet_memory.append((current_time, src_ip))   # Save packet in memory.

        # Remove packets older than 10 minutes.
        while packet_memory and current_time - packet_memory[0][0] > MEMORY_LIMIT:
            packet_memory.popleft()

        detect_syn_flood(src_ip, current_time)


# Function to start packet sniffer.
def start_sniffer(interface):

    print("SYN Flood Detector Running...\n")

    sniff(
        iface=interface,   # Listen on selected interface.
        prn=packet_callback,
        store=0
    )


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--interface", required=True)

    args = parser.parse_args()

    start_sniffer(args.interface)


if __name__ == "__main__":
    main()