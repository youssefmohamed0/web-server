import socket as sk
import time
import os

ip = sk.gethostbyname(sk.gethostname())

port = 9999



def send_request(request_bytes):
    sock = sk.socket(sk.AF_INET,sk.SOCK_STREAM)
    sock.connect((ip,port))
    sock.sendall(request_bytes) #after sending a request a response is expected

    response = b""

 
    while b'<end>' not in response:
        response += sock.recv(1024)


    response = response.rstrip(b"world")

    return response


def upload_file(filename,file_path):
    file = open(file_path,"rb")
    file_bytes = file.read()

    request = (
        f'POST /upload HTTP/1.1\r\n'
        f'Host: {ip}\r\n'
        f'Content-Length: {len(file_bytes)}\r\n'
        f'Content-Type: application/octet-stream\r\n'
        f'Content-Disposition: attachment; filename="{filename}"\r\n'
        f'\r\n'
    )
    request_bytes = request.encode() + file_bytes

    host_response = send_request(request_bytes)

    headers, body = host_response.split(b'\r\n\r\n', 1)

    if b"200 OK" in headers:
        print('File uploaded successfully.')
    else:
        print('Failed to upload file.')




def download_file(filename):


    request = (
        f'GET /{filename} HTTP/1.1\r\n'
        f'Host: {ip}\r\n'
        f'\r\n'
    )
    host_response = send_request(request.encode())

    headers, body = host_response.split(b'\r\n\r\n', 1)

    if b"200 OK" in headers:
        if os.path.exists(filename):
            os.remove(filename)
        file = open(filename,"wb")
        file.write(body)
        file.close()
        print('File downloaded successfully.')
    else:
        print('Failed to download file.')


while True:
    print("1) Send image")
    print("2) Recieve image")
    
    flag = 1
    while flag:
        num = input("\nChoose an option: ")

        if num == '1' or num == '2':
            flag = 0
        else:
            print("Error! Choose from previous numbers.")

    if num == '1':
        filename = input("Enter file name: ")
        file_path = input("Enter file path: ")
        upload_file(filename, file_path)
    if num == '2':
        filename = input("Enter file name: ")
        download_file(filename)
    