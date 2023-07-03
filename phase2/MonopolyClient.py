from socket import *
from threading import *

def client(port):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect(('127.0.0.1', port))

    
    tmp = ""
    part = sock.recv(1024)
    while part and part != '':
        tmp += part.decode()
        print("Client Conncted to the server")
        client_input = input()
        tmp = ""
        try:
            sock.send(client_input.encode())
            part = sock.recv(1024)
            print()
            print(part.decode()[0:-1])
            print()
            break
        except:
            print("Your connection is closed.")
            return
    tmp = ""
    part = sock.recv(1024)
    while part and part != '':
        tmp = part.decode()
        if(tmp[-1]=='2'):
            print(tmp[0:-1])
            print()
            inp = input()
            sock.send(inp.encode())
        else:
            print(tmp[0:-1])
        part = sock.recv(1024)
    sock.close()
