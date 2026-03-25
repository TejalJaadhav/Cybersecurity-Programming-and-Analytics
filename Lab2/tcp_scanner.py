def tcp_scanner(target, port):
   """
   We use socket.AF_INET to work with IPv4 addresses.
   We use socket.SOCK_STREAM because TCP is a reliable connection-based protocol.
   This lets us try to connect to a specific port on the target machine.   
   
   """
   try:
         tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         tcp_sock.settimeout(1)  # Socket wait only 1 second If the port does not respond, it moves to the next port quickly.         
         tcp_sock.connect((target, port))
         tcp_sock.close()
         return True
   except:
         """
        An exception can happen if:
         - The port is closed
         - The host is not reachable
         - The connection times out
         - There is a network error
        We handle it so the program does not crash.
        
        """
         return False

def main():
   """
     We check len(sys.argv) to make sure the user enters the target IP address when running the script. If not, we show a usage message.   

    """
   if len(sys.argv) != 2:
         print("Usage: python tcp_scanner.py <Metasploitable-2_IP>")
         sys.exit(1)

   target = sys.argv[1]
   print(f"Scanning TCP ports on {target}...")
   """
   We scan ports 1 to 1023 because these are well-known ports.
   Common services like FTP, SSH, and HTTP use these ports.
   
   """
   for port in range(1, 1024):
         if tcp_scanner(target, port):
            print(f"[*] Port {port}/tcp is open")

if __name__ == "__main__":
   main()
                                                      