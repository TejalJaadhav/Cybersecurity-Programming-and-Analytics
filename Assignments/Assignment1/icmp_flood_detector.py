from scapy.all import sniff, IP, ICMP
from collections import defaultdict, deque
import argparse
import time
import csv

# Store packets captured in the last 10 minutes.
packet_memory = deque()

# Count ICMP Echo Requests per second for each source IP.
icmp_rate = defaultdict(lambda: defaultdict(int))

# Store timestamps when a flood was previously detected.
flood_history = defaultdict(list)

MEMORY_LIMIT = 600        # 10 minutes.
FLOOD_THRESHOLD = 50      # Packets per second.
FLOOD_DURATION = 3        # Seconds.
HISTORY_WINDOW = 1800     # 30 minutes.

# Function to check the CSV log from Part 1 to see if this IP previously exceeded the flood threshold.
def check_csv_history(src_ip):

    try:
        with open("traffic_log.csv", "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header.

            for row in reader:

                # Ensure the row has expected fields.
                if len(row) < 6:
                    continue

                timestamp, src, dst, port, protocol, flag = row

                # Check if this source IP sent ICMP echo requests.
                if src == src_ip and protocol == "ICMP" and flag == "ECHO_REQUEST":
                    return True

    except FileNotFoundError:
        pass

    return False


# Function to analyze ICMP request rate and determine if it meets the flood detection conditions.
def detect_flood(src_ip, current_time):

    second = int(current_time) 

    icmp_rate[src_ip][second] += 1  # Increment counter for this IP in this second.

    counts = []   # Check packet counts for the last 3 seconds.

    for i in range(FLOOD_DURATION):
        counts.append(icmp_rate[src_ip].get(second - i, 0))

    # Verify if each second exceeded threshold.
    if all(count > FLOOD_THRESHOLD for count in counts):

        # Check if this IP triggered a flood recently in memory.
        recent_floods = [
            t for t in flood_history[src_ip]
            if current_time - t < HISTORY_WINDOW
        ]

        previous_in_csv = check_csv_history(src_ip)  # Check historical CSV logs.

        # Alert only if flood was previously seen.
        if recent_floods or previous_in_csv:

            average_rate = sum(counts) // FLOOD_DURATION

            print("\nALERT: ICMP Flood Detected!")
            print(f"Source: {src_ip} | Rate: {average_rate} requests/sec | Duration: 3 sec")

            if previous_in_csv:
                print("Previous flood detected in last 30 minutes: YES\n")
            else:
                print("Previous flood detected in last 30 minutes: NO\n")

        flood_history[src_ip].append(current_time)   # Store detection time.



# Function to called every time a packet is captured. Filters ICMP Echo Requests and analyzes them.
def packet_callback(packet):

    # Ignore packets without IP layer.
    if IP not in packet:
        return

    # Check if packet is ICMP Echo Request.
    if ICMP in packet and packet[ICMP].type == 8:

        src_ip = packet[IP].src
        current_time = time.time()

        packet_memory.append((current_time, src_ip))   # Store packet in memory.

        # Remove packets older than 10 minutes.
        while packet_memory and current_time - packet_memory[0][0] > MEMORY_LIMIT:
            packet_memory.popleft()

        detect_flood(src_ip, current_time)    # Analyze packet rate for flood detection.

# Function to start packet capture on selected interface.
def start_sniffer(interface):

    print("ICMP Flood Detector Running...\n")

    sniff(
        iface=interface,
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