import socket
import time

SERVER_PORT = 12345
SEQ_NUM = 0

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_socket.bind(("localhost", SERVER_PORT))
print(f"Server listening on {'localhost'}:{SERVER_PORT}")

def calculate_checksum(message):
    checksum = 0
    # Calculate the checksum by XOR-ing all the bytes in the message
    for byte in message.encode('utf-8'):
        checksum ^= byte  # Use the integer representation of the byte
    return checksum

while True:
    try:
        prev = SEQ_NUM
        data, client_address = server_socket.recvfrom(1024)
        if (data.decode('utf-8') == 'exit'):
            break
        message, rest = data.decode('utf-8').split(':', 1)
        checksum, seqNum = rest.split(':', 1)
        if ':' in checksum:
            checksum, _ = checksum.split(':', 1)
        print(message, ':', checksum)

        if checksum == str(calculate_checksum(message)):
            SEQ_NUM = SEQ_NUM ^ 1
            packet = "ACK" + ':' + str(SEQ_NUM)
            print("ACK being sent : ", packet)
            print(f"Received message: \"{message}\". Sending ACK.")
            time.sleep(2)
            server_socket.sendto(packet.encode(), client_address)

        else:
            if prev == SEQ_NUM:
                packet = "ACK" + ':' + str(prev)
            else:
                packet = "ACK" + ':' + str(SEQ_NUM)
            print(f"Received message: \"{message}\". Sending NACK.")
            print("PACKET being sent : ", packet)
            print("Erroneous packet received ...")
            server_socket.sendto(packet.encode(), client_address)

        if message.lower() == 'exit':
            print(f"Connection terminated with {client_address}.")
            break

    except KeyboardInterrupt:
        print(f"Connection interrupted with {client_address}.")

server_socket.close()
