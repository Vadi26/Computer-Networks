import socket
import time
import random

# Sender configuration
sender_host = "127.0.0.1"
sender_port = 12345
receiver_host = "127.0.0.1"
receiver_port = 54321

# Create a UDP socket
sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

window_size = 4
base = 0
next_seq_num = 0
packets = [f"Packet {i}" for i in range(12)]
acked = [False] * len(packets)

def send_packets():
    global next_seq_num, base
    while next_seq_num < len(packets):
        if next_seq_num < base + window_size:
            if random.random() < 0.8:  # Simulating packet loss
                packet = f"{next_seq_num}:{packets[next_seq_num]}"
                sender_socket.sendto(packet.encode(), (receiver_host, receiver_port))
                print(f"Sent packet {next_seq_num}")
                if base == next_seq_num:
                    time.sleep(1)  # Add a delay
                next_seq_num += 1
            else:
                print(f"Packet {next_seq_num} dropped (simulated packet loss)")
                next_seq_num += 1
        else:
            break

def receive_acks():
    global next_seq_num, base
    sender_socket.settimeout(2)  # Set a timeout for acknowledgments
    try:
        while True:
            ack, addr = sender_socket.recvfrom(1024)
            ack_num = int(ack.decode())
            print(f"Received acknowledgment for packet {ack_num}")
            if ack_num == 11:
                break
            if base <= ack_num < base + window_size:
                acked[ack_num] = True
                while acked[base]:
                    base += 1
    except socket.timeout:
        for i in range(len(acked)):
            if acked[i] == False:
                next_seq_num = i
                break
        send_packets()

while base < len(packets):
    send_packets()
    receive_acks()

sender_socket.close()
