import socket as sk
import threading
import time
import os
import re

closeThreads = False

server_ip = sk.gethostbyname(sk.gethostname())
server_port = 9999



def proccess_request(client_socket):

    request = b""
    response = b""
    print("server reciving now")
    while b'<end>' not in request:
        request += client_socket.recv(1024)
    print("server recieved")

    if request.startswith(b"GET"):
        filename = re.search(r"/(\w+)", request.decode()).group(1)
        file = open(f"{filename}","rb")
        file_bytes = file.read()

        get_response = f"""
HTTP/1.1 200 OK\r\n
Content-Length: {len(file_bytes)}\r\n
Content-Type: application/socket-stream\r\n
Content-Disposition: attachment; filename=\"{filename}\"\r\n
<end>
"""
        get_response_bytes = get_response.encode() + file_bytes # to be sent to client

        file.close()
        response += get_response_bytes

    elif request.startswith(b"POST"):

        filename = re.search(r"filename=\"(.*?)\"", request.decode()).group(1)

        headers, body = request.split(b'<end>', 1)

        file = open(filename,"wb")
        file.write(body)

        post_response=f"""
HTTP/1.1 200 OK\r\n
Content-Length: {len(file.read())}\r\n
Content-Type: application/socket-stream\r\n
Content-Disposition: attachment; filename=\"{filename}\"\r\n
<end>
"""
        post_response_bytes = post_response.encode()

        file.close()
        response += post_response_bytes

    else:
        pass
    print("sending response to client")
    print(request)
    print(response)
    client_socket.sendall(response)



if __name__ == '__main__':
    SERVER = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    SERVER.bind((server_ip, server_port))
    SERVER.listen(5)
    print(f"Server with IP {server_ip} on port {server_port} is now running")

    while True:
        client_socket, client_add = SERVER.accept()
        print(f"connected to {client_add}")
    
        thread = threading.Thread(target=proccess_request,args=(client_socket,))
        # response = proccess_request(request)    # byte form
        # client_socket.sendall(response)
        thread.start()

