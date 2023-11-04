import socket
import random

receiver_host = "127.0.0.1"
receiver_port = 54321
receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receiver_socket.bind((receiver_host, receiver_port))

# Track received packets
received_packets = {}
expected_seq_num = 0

def send_acknowledgment(seq_num, addr):
    if random.random() < 0.2:  # Simulate acknowledgment loss with 20% probability
        print(f"Acknowledgment for packet {seq_num} is lost.")
    else:
        ack = str(seq_num)
        receiver_socket.sendto(ack.encode(), addr)
        print(f"Sent acknowledgment for packet {seq_num}")

while expected_seq_num < 12:
    packet, addr = receiver_socket.recvfrom(1024)
    packet_data = packet.decode()
    seq_num, message = packet_data.split(":", 1)
    seq_num = int(seq_num)

    if seq_num == expected_seq_num:
        print(f"Received packet with sequence number {seq_num}: {message}")
        received_packets[seq_num] = message
        send_acknowledgment(seq_num, addr)
        expected_seq_num += 1
    else:
        print(f"Received out-of-order packet {seq_num}. Discarding.")

receiver_socket.close()
