import socket as sk
import time
import os

# myip.is
ip = sk.gethostbyname(sk.gethostname())

port = 9999

sock = sk.socket(sk.AF_INET,sk.SOCK_STREAM)

sock.connect((ip,port))
# connect is used only by the client


def send_request(request_bytes):
    sock = sk.socket(sk.AF_INET,sk.SOCK_STREAM)
    sock.connect((ip,port))
    sock.sendall(request_bytes) #after sending a request a response is expected

    response = b""

    while True:
        packet = sock.recv(1024)
        if not packet:
            break
        response +=packet

    sock.close()

    return response


def upload_file(filename,file_path):
    file = open(file_path,"rb")
    file_bytes = file.read()

    request = f"""
POST /upload HTTP/1.1\r\n
Host: {ip}\r\n
Content-Length: {len(file_bytes)}\r\n
Content-Type: application/socket-stream\r\n
Content-Disposition: attachment; filename=\"{filename}\"\r\n
\r\n
"""
    request_bytes = request.encode() + file_bytes

    host_response = send_request(request_bytes)

    headers, body = host_response.split(b'\r\n\r\n', 1)

    if b"200 OK" in headers:
        print('File downloaded successfully.')
    else:
        print('Failed to download file.')




def download_file(filename, save_path):
    file = open(os.path.join(save_path,filename),"wb")
    file_bytes = file.read()

    request = f"""
GET /{filename} HTTP/1.1\r\n
Host: {ip}\r\n
\r\n
""" 
    host_response = send_request(request.encode())

    headers, body = host_response.split(b'\r\n\r\n', 1)

    if b"200 OK" in headers:
        file = open(os.path.join(save_path,filename),"wb")
        file.write(body)
        file.close()
        print('File downloaded successfully.')
    else:
        print('Failed to download file.')


if __name__ == '__main__':
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
        save_path = input("Enter save path: ")
        download_file(filename, save_path)
    