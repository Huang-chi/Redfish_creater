import socket
import sys, time
import socketserver

from setting import *

def socket_connect(message):
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST,SERVER_PORT))
        RxData = message.encode('utf-8')
        size = sys.getsizeof(RxData)
        print(size)
        print(RxData)
        if RxData:
            s.sendall(str(size).encode('utf-8'))
            time.sleep(0.5)
            s.sendall(RxData)
        s.close()

if __name__ == "__main__":
	socket_connect("asdas")
