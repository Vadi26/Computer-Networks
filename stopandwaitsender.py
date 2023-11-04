import socket
import time

# Sender configuration
sender_host = "127.0.0.1"
sender_port = 12345
receiver_host = "127.0.0.1"
receiver_port = 54321

# Create a UDP socket
sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

seq_num = 0
message = "Hello, Receiver!"
packet = f"{seq_num}:{message}"

while True:
    # Send the packet
    packet = f"{seq_num}:{message}"
    sender_socket.sendto(packet.encode(), (receiver_host, receiver_port))
    print(f"Sent packet with sequence number {seq_num}")

    # Wait for acknowledgment
    sender_socket.settimeout(2)  # Set a timeout for acknowledgment
    try:
        ack, addr = sender_socket.recvfrom(1024)
        ack_num = int(ack.decode())
        if ack_num == seq_num:
            print(f"Received acknowledgment for packet {seq_num}")
            seq_num = 1 - seq_num  # Toggle sequence number
        else:
            print(f"Received incorrect acknowledgment. Resending packet {seq_num}")
    except socket.timeout:
        print(f"Timeout, resending packet {seq_num}")

    time.sleep(1)  # Add a delay for demonstration

sender_socket.close()
