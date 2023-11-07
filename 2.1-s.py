import socket
import time
import random
import copy

SERVER_ADDRESS = ("localhost", 12345)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def calculate_checksum(message):
    checksum = 0
    for byte in message.encode('utf-8'):
        checksum ^= byte
    return checksum

SEQ_NUM = 0

while True:
    try:
        message = input("Client: Enter your message (or 'exit' to quit): ")
        if message.lower() == 'exit':
            packet = message.encode('utf-8')
            client_socket.sendto(packet, SERVER_ADDRESS)
            break

        originalMessage = copy.deepcopy(message)
        checksum = calculate_checksum(message)
        message = message + ':' + str(SEQ_NUM) + ':' + str(checksum)

        if random.random() < 0.75:
            error_position = random.randint(0, len(message) - 4)
            message = message[:error_position] + chr(ord(message[error_position]) ^ 1) + message[error_position + 1:]

        packet = message.encode('utf-8')

        ack_received = False
        while not ack_received:
            client_socket.sendto(packet, SERVER_ADDRESS)
            print(f"Sent message: \"{originalMessage}\" with SEQ: {SEQ_NUM} and Checksum: {checksum}")
            ackNAK, _ = client_socket.recvfrom(5)
            ackNAK = ackNAK.decode()

            if ackNAK == f"ACK:{SEQ_NUM}":
                print(f"ACK received for SEQ: {SEQ_NUM}")
                SEQ_NUM = 1 - SEQ_NUM  # Toggle between 0 and 1 for the next sequence number
                ack_received = True
            else:
                print(f"NAK received for SEQ: {SEQ_NUM}. Resending...")
                time.sleep(2)
                checksum = calculate_checksum(originalMessage)
                message = originalMessage + ':' + str(SEQ_NUM) + ':' + str(checksum)

                if random.random() < 0.1:
                    error_position = random.randint(0, len(message) - 4)
                    message = message[:error_position] + chr(ord(message[error_position]) ^ 1) + message[error_position + 1:]
                
                packet = message.encode('utf-8')

    except Exception as e:
        print(f"Error: {e}")

client_socket.close()
