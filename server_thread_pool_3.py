from socket import *
import socket
import time
import sys
import logging
from concurrent.futures import ThreadPoolExecutor
from http import HttpServer

httpserver = HttpServer()

def ProcessTheClient(connection, address):
    rcv = ""
    while True:
        try:
            data = connection.recv(32)
            if data:
                # Convert input from socket (bytes) to string to detect \r\n
                d = data.decode()
                rcv = rcv + d
                if rcv[-2:] == '\r\n':
                    # End of command, process string
                    logging.warning("data dari client: {}".format(rcv))
                    hasil = httpserver.proses(rcv)
                    # Result will be bytes
                    # To concatenate with string, encode string
                    hasil = hasil + "\r\n\r\n".encode()
                    logging.warning("balas ke client: {}".format(hasil))
                    # Result is in bytes
                    connection.sendall(hasil)
                    rcv = ""
                    connection.close()
                    return
            else:
                break
        except OSError as e:
            pass
    connection.close()
    return

def Server(portnumber=8889):
    the_clients = []
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    my_socket.bind(('0.0.0.0', portnumber))
    my_socket.listen(1)

    with ThreadPoolExecutor(20) as executor:
        while True:
            connection, client_address = my_socket.accept()
            # logging.warning("connection from {}".format(client_address))
            p = executor.submit(ProcessTheClient, connection, client_address)
            the_clients.append(p)
            # Display the number of active threads
            jumlah = ['x' for i in the_clients if i.running()]
            print(jumlah)

def main():
    portnumber = 8001
    try:
        portnumber = int(sys.argv[1])
    except:
        pass
    svr = Server(portnumber)

if __name__ == "__main__":
    main()
