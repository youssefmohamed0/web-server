import socket as sk
import threading
import time
import os

closeThreads = False

server_ip = "192.168.1.8"
server_port = 9999



file_size=os.path.getsize("kitten.jpg")


def manage_client(client_sock:sk.socket, client_addr):
    while not closeThreads:
        file = open("kitten.jpg","rb")
        data = client_sock.recv(1024)   # client request
        if not data:
            break
        print(f"Received data from {client_addr}: {data.decode()}")
        if data.decode().startswith("GET") or data.decode().startswith("POST"):
            client_sock.send("received_image.jpg".encode())
            client_sock.send(str(file_size).encode())
            response = file.read()
            client_sock.sendall(response)
            client_sock.send(b"<END>")
    print("Connection closed")
    file.close()
    client_sock.close()

SERVER = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
SERVER.bind((server_ip, server_port))

SERVER.listen(5)

print(f"Server with IP {server_ip} on port {server_port} is now running")

while True:
    try:
        client_sock, client_addr = SERVER.accept()
        print(f"Connected to client {client_addr}")
        thread = threading.Thread(target=manage_client, args=(client_sock, client_addr))
        thread.start()
    except KeyboardInterrupt:
        closeThreads = True
        print("Server stopping...")
        break
    except Exception as e:
        print(f"Server error: {e}")
        break

print("Server stopped")