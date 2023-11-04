import socket
import random

# Receiver configuration
receiver_host = "127.0.0.1"
receiver_port = 54321

# Create a UDP socket
receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receiver_socket.bind((receiver_host, receiver_port))

expected_seq_num = 0

while True:
    packet, addr = receiver_socket.recvfrom(1024)
    packet_data = packet.decode()
    seq_num, message = packet_data.split(":", 1)
    seq_num = int(seq_num)

    if seq_num == expected_seq_num:
        print(f"Received packet with sequence number {seq_num}: {message}")

        # Randomly decide whether to send an acknowledgment
        if random.random() < 0.5:
            ack = str(seq_num)
            receiver_socket.sendto(ack.encode(), addr)
            print(f"Sent acknowledgment for packet {seq_num}")
        
        expected_seq_num = 1 - expected_seq_num  # Toggle sequence number
    else:
        print(f"Received out-of-order packet. Discarding.")

receiver_socket.close()
