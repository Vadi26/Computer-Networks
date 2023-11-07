import socket
import random
import time

# Client configuration
server_host = '127.0.0.1'
server_port = 12345

def calculate_checksum(message):
    checksum = 0
    for byte in message.encode('utf-8'):
        checksum ^= byte
    return checksum

# Create a socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(4)

seq = 0

while True:
    message = input("Enter your message: ")
    checksum = calculate_checksum(message)
    print(checksum)
    packet = f"{message}:{checksum}:{seq}"

    client_socket.sendto(packet.encode('utf-8'), (server_host, server_port))
    ack = False
    start_time = time.time()

    if ack:
        print("ACK received")

    while not ack:
        try:
            data, server_address = client_socket.recvfrom(1024)
            print("DATA RECEIVED : ", data.decode('utf-8'))
            response, received_checksum, received_seqnum = data.decode('utf-8').split(':')
            received_seqnum = int(received_seqnum)

            if calculate_checksum(response) != int(received_checksum):
                print("Corrupted message received...")
            elif seq != received_seqnum:
                print("Response with wrong seq received...")
            else:
                print(f"ACK received with seq number -> {received_seqnum}")
                seq +=1
                ack = True
        except socket.timeout:
            if time.time() - start_time >= 4:
                print("Timeout occurred!! Resending the message...")
                client_socket.sendto(packet.encode('utf-8'), (server_host, server_port))

client_socket.close()


