import socket

def calculate_checksum(data):
    checksum = 0
    for c in data:
        checksum += ord(c)
    return str(checksum)

def receiver(receiver_host, receiver_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((receiver_host, receiver_port))
    expected_seq = 0
    while True:
        data, addr = sock.recvfrom(1024)
        print
        if not data:
            break
        packet = data.decode()
        seq, segment, checksum = packet.split(":")
        print("Tell me whyyii")
        if int(seq) == expected_seq and int(checksum) == int(calculate_checksum(segment)):
            print(f"Received: {segment}")
            expected_seq = (expected_seq + 1) % 2
            print("Whyyyy")
            # Send an ACK for the received packet
            ack_packet = f"ACK:{seq}"
            sock.sendto(ack_packet.encode(), addr)
        else:
            print(f"Received packet with errors: {segment}")
            # Send a NAK for the packet with errors
            nak_packet = "NAK"
            sock.sendto(nak_packet.encode(), addr)

receiver('localhost', 12345)
