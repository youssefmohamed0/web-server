import socket as sk
import threading
import time
import os

closeThreads = False

server_ip = sk.gethostbyname(sk.gethostname())
server_port = 9999



file_size=os.path.getsize("kitten.jpg")

def proccess_request(request):
    if request.startswith(b"GET"):
        pass
    pass


if __name__ == '__main__':
    SERVER = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    SERVER.bind((server_ip, server_port))
    SERVER.listen(5)

    print(f"Server with IP {server_ip} on port {server_port} is now running")

    request = b""
    while True:
        packet = SERVER.recv(1024)
        if not packet:
            break
        request += packet
    
    reponse = proccess_request(request)

    pass


# def manage_client(client_sock:sk.socket, client_addr):
#     while not closeThreads:
#         file = open("kitten.jpg","rb")
#         data = client_sock.recv(1024)   # client request
#         if not data:
#             break
#         print(f"Received data from {client_addr}: {data.decode()}")
#         if data.decode().startswith("GET"):
#             client_sock.send("kitten.jpg".encode())
#             client_sock.send(str(file_size).encode())
#             response = file.read()
#             client_sock.sendall(response)
#             client_sock.send(b"<END>")
        
#         elif data.decode().startswith("POST"):
#             file_name = SERVER.recv(1024).decode()   # recieves response
#             file_size = SERVER.recv(1024).decode()
#             print(file_name)
#             print(file_size)

#             file_bytes = b""

#             data = SERVER.recv(int(file_size))

#             file_bytes+=data

#             file = open(file_name,"wb")
#             file.write(file_bytes)
#             file.close()

#             pass

#     print("Connection closed")
#     file.close()
#     client_sock.close()

# SERVER = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
# SERVER.bind((server_ip, server_port))

# SERVER.listen(5)

# print(f"Server with IP {server_ip} on port {server_port} is now running")

# while True:
#     try:
#         client_sock, client_addr = SERVER.accept()
#         print(f"Connected to client {client_addr}")
#         thread = threading.Thread(target=manage_client, args=(client_sock, client_addr))
#         thread.start()
#     except KeyboardInterrupt:
#         closeThreads = True
#         print("Server stopping...")
#         break
#     except Exception as e:
#         print(f"Server error: {e}")
#         break

# print("Server stopped")