import socket
import sys

def udp_dns_scanner(target, port=53):
    """
    We use socket.SOCK_DGRAM because UDP is a datagram-based protocol.
    SOCK_DGRAM creates a UDP socket.
    """
    try:
        udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # settimeout(2.0) makes the socket wait 2 seconds for a reply
        # If no reply comes, it stops waiting and raises a timeout
        udp_sock.settimeout(2.0)

        # This is a simple DNS query packet asking for example.com
        # It is manually crafted in binary format
        query = b'\x12\x34\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00' \
                b'\x07example\x03com\x00\x00\x01\x00\x01'

        udp_sock.sendto(query, (target, port))

        # recvfrom(512) reads up to 512 bytes from the response
        # 512 bytes is the standard maximum size of a DNS UDP response
        response, _ = udp_sock.recvfrom(512)

        if response:
            print(f"[*] Port {port}/udp (DNS) is open and responding")
            return True

    except socket.timeout:
        # Timeout is common in UDP because UDP does not guarantee a response
        print(f"[-] Port {port}/udp (DNS) did not respond")
        return False

    finally:
        # We close the socket to release system resources
        udp_sock.close()


def main():
    """
    sys.argv is used to take input from the command line.
    It allows the user to provide the target IP address.
    """
    if len(sys.argv) != 2:
        print("Usage: python udp_dns_scanner.py <Metasploitable-2_IP>")
        sys.exit(1)

    target = sys.argv[1]
    print(f"Scanning UDP DNS port on {target}...")
    udp_dns_scanner(target)


if __name__ == "__main__":
    main()
