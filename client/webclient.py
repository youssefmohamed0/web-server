import socket as sk
import time

# myip.is
ip = "192.168.1.8"  # if connecting to a server on a diffrent lan u need to use public ip

port = 9999

sock = sk.socket(sk.AF_INET,sk.SOCK_STREAM)

sock.connect((ip,port))
# connect is used only by the client


while True:
    option = input("do you want get or post: ")

    if option == "get":
        sock.sendall("GET".encode())

        file_name = sock.recv(1024).decode()   # recieves response
        file_size = sock.recv(1024).decode()
        print(file_name)
        print(file_size)


        file_bytes = b""


        data = sock.recv(int(file_size))

        file_bytes+=data


        file = open(file_name,"wb")
        file.write(file_bytes)
        file.close()