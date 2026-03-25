#!/bin/bash
# variables
#
  SUBNET="192.168.64.0/24"
  TARGET="192.168.64.4"
#
  echo "Enhanced Security Script"
  echo "Script Execution Started"
  echo "========================="
  echo
#
# part 1: Collect Information About the Local Machine
  echo "Part 1: Information About My Own Machine"
  echo "========================================="
  echo "[*] System Information:"
  uname -a # This command shows detailed information about the system, such  # as operating system, kernel version, and hardware details.
  echo
#                                 
  echo "[*] Network Interfaces and IP Addresses:"
  # This command lists all available network interfaces, their # assigned IP addresses, and interface states.
  ip addr show || echo "Error - Unable to fetch network inerface information." 
  echo
#
  echo "[*] ARP Table:"
  arp -a # This command shows IP-to-MAC address mappings on the local network
  echo
#
  echo "[*] Open Ports on Local Machine:"
  sudo netstat -tuln # This command lists all active listening TCP and UDP   # ports on the local machine:
  # -t : TCP Ports
  # -u : UDP Ports
  # -l : Listening services
  # -n : shows numeric addresses without numeric DNS lookup
  echo
#
# Part 2: Information About a Target"
  echo "Part 2: Information About a Target"
  echo "================================="
  echo "Active Hosts in Subnet ($SUBNET): "
  sudo nmap -sP $SUBNET # This command performs a ping scan on the given 
# subnet to identify which hosts are currently online. This option checks
# hosts availability only and does not scan ports.
  echo 
#
  echo "[*] Services Scan on Target ($TARGET): "
  sudo nmap -sV $TARGET # This command scans the target for open ports and
# attempts to identify the services and their version numbers running on
# those ports. This helps determine what software is running and whether it
# may have vulnerailities.
  echo
#
  echo "[*] Vulnerability scan on Target ($TARGET): "
  sudo nmap --script vuln $TARGET # This command runs Nmap vulnerability 
# detection script against the target system. This script checks for known
# security vulnerabilities in services running on the target by using the
# Nmap Scripting Engine (NSE).
  echo

  echo "==========================="
  echo "Script Execution Completed."
  echo "==========================="
