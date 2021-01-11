import socket
import socketserver

from setting import *

def listen_inner_network(port):

#     PORT = int(str(port))
    PORT = int(port)

    with socket.socket(socket.AF_INET , socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        s.bind((HOST , PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr )
            data = conn.recv(16)
            print(type(repr(data)))

            print('Connected by', addr )
            data = conn.recv(int(repr(data)[2:-1]))

    print('Received', repr(data))
    return repr(data)

if __name__ == "__main__":
	listen_inner_network(SERVER_PORT)
