import socket
import threading

nickname = input("Choose a nickname : ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            print("An error occurred :(")
            client.close()
            print("Closing the connection !")
            break

def write():
    while True:
        message = f'{nickname}: {input("")}'
        if message == f"{nickname}: exit":
            break
        client.send(message.encode('ascii'))
    print("Closing the connection !")
    client.close()

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()