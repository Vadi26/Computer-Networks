import socket
import time
import random

sender_host = "127.0.0.1"
sender_port = 12345
receiver_host = "127.0.0.1"
receiver_port = 54321
sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

window_size = 4
base = 0
next_seq_num = 0
packets = [f"Packet {i}" for i in range(12)]
acked = [False] * len(packets)

def send_packets():
    global next_seq_num
    while next_seq_num < len(packets):
        if next_seq_num < base + window_size:
            packet = f"{next_seq_num}:{packets[next_seq_num]}"
            sender_socket.sendto(packet.encode(), (receiver_host, receiver_port))
            print(f"Sent packet {next_seq_num}")
            if base == next_seq_num:
                time.sleep(1)
            next_seq_num += 1
        else:
            break

def receive_acks():
    global base
    sender_socket.settimeout(2)
    try:
        while True:
            ack, addr = sender_socket.recvfrom(1024)
            ack_num = int(ack.decode())
            print(f"Received acknowledgment for packet {ack_num}")
            acked[ack_num] = True
    except socket.timeout:
        pass

while base < len(packets):
    send_packets()
    receive_acks()

sender_socket.close()
