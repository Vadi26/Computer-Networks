import socket
import hashlib
import random

SERVER_PORT = 12345
LOSS_PROBABILITY = 0.8

def cal_checksum(data):
    hash_obj = hashlib.sha256()
    hash_obj.update(data.encode())
    return hash_obj.hexdigest()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_socket.bind(("localhost", SERVER_PORT))
print(f"Server listening on {'localhost'}:{SERVER_PORT}")
expected_seq = 0

while True:
    try:
        data, client_address = server_socket.recvfrom(1024)
        message, checksum, seq_no = data.decode('utf-8').split(':')

        if cal_checksum(message) != checksum:
            print("Received corrupted message.")
            
        elif int(seq_no) != expected_seq % 2:
            print(f"Incorrect Sequence Number.")
            
        else:
            print(f"Received message: \"{message}\". Sending ACK.")
            checksum = cal_checksum("ACK")
            packet = f"ACK:{checksum}:{expected_seq%2}"
            server_socket.sendto(packet.encode(), client_address)
            expected_seq += 1

        if message.lower() == 'exit':
            print(f"Connection terminated with {client_address}.")
            break

    except KeyboardInterrupt:
        print(f"Connection interrupted with {client_address}.")

server_socket.close()
