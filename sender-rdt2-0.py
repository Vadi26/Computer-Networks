import socket
import random
import time

seq_num = 0

def calculate_checksum(data):
    checksum = 0
    for c in data:
        checksum += ord(c)
    return str(checksum)

def sender(segment, receiver_host, receiver_port):
    global seq_num
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # seq_num = 0
    packet = f"{seq_num}:{segment}:{calculate_checksum(segment)}"
    sock.sendto(packet.encode(), (receiver_host, receiver_port))
    print(f"Sent: {segment}")
    seq_num = (seq_num + 1) % 2

    # Wait for ACK or NAK
    while True:
        ack_or_nak, addr = sock.recvfrom(1024)
        if ack_or_nak.decode() == f"ACK:{seq_num}":
            print(f"Received ACK for packet {seq_num}")
            break
        elif ack_or_nak.decode() == "NAK":
            print(f"Received NAK for packet {seq_num}, resending...")
            sock.sendto(packet.encode(), (receiver_host, receiver_port))

while True:
    data = input("Enter the data you want to send : ")
    sender(data, 'localhost', 12345)
    yesorno = input("Do you want to send more data ? (y/n)")
    if yesorno == 'n':
        break
    else :
        continue

sender(["Segment 1", "Segment 2", "Segment 3"], 'localhost', 12345)
