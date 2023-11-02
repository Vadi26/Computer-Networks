import socket
import time
import random
import copy

SERVER_ADDRESS = ("localhost", 12345)
SEQ_NUM = 0

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def calculate_checksum(message):
    checksum = 0

    # Calculate the checksum by XOR-ing all the bytes in the message
    for byte in message.encode('utf-8'):
        checksum ^= byte  # Use the integer representation of the byte

    return checksum

while True:
    try:
        message = input("Client: Enter your message (or 'exit' to quit): ")
        prevseq = SEQ_NUM
        SEQ_NUM = SEQ_NUM ^ 1
        if message.lower() == 'exit':
            packet = message.encode('utf-8')
            client_socket.sendto(packet, SERVER_ADDRESS)
            break
        
        originalMessage = copy.deepcopy(message)
        checksum = calculate_checksum(message)
        message = message + ':' + str(checksum) + ':' + str(SEQ_NUM)
        originalMessage = originalMessage + ':' + str(checksum) + ':' + str(SEQ_NUM)
        
        if random.random() < 0.5:
            error_position = random.randint(0, len(message) - 4)
            message = message[:error_position] + chr(ord(message[error_position]) ^ 1) + message[error_position + 1:]

        # packet = message + ":" + bytes(checksum)
        packet = message.encode('utf-8')

        client_socket.sendto(packet, SERVER_ADDRESS)

        ack_received = False
        ackNAK, _ = client_socket.recvfrom(5)
        ack, seqNum = ackNAK.decode('utf-8').split(':', 1)
        if seqNum == str(SEQ_NUM):
            print(f"ACK {SEQ_NUM} received ")
        else:
            while int(seqNum) != SEQ_NUM:
                print(f"ACK {seqNum} received")
                print("Received ACK number : ", seqNum, "Expected ACK number : ", SEQ_NUM)
                print("Resending the packet ...")
                time.sleep(2)
                checksum = calculate_checksum(originalMessage)
                message = originalMessage + ':' + str(checksum) + ':' + str(SEQ_NUM)

                if random.random() < 0.1:
                    error_position = random.randint(0, len(message) - 4)
                    message = message[:error_position] + chr(ord(message[error_position]) ^ 1) + message[error_position + 1:]

                packet = message.encode('utf-8')
                client_socket.sendto(packet, SERVER_ADDRESS)
                time.sleep(2)
                ackNAK, _ = client_socket.recvfrom(5)
                ack, seqNum = ackNAK.decode('utf-8').split(':', 1)

    except Exception as e:
        print(f"Error: {e}")

client_socket.close()

