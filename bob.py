import socket  # for socket
from random import randint
from message_process import *


def generate_random_number():
    message_id = hex(randint(0, 1000000))
    message_id = message_id.replace('0x', '')
    counter = len(message_id)
    for i in range(0, 15 - counter):
        message_id = message_id + '0'

    return message_id


def main():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 6346

    host_ip = '127.0.0.1'

    s.connect((host_ip, port))

    header = build_query_header()
    header += int(5).to_bytes(2, 'big')
    header += 'test.txt'.encode()

    s.send(header)
    s.close()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('127.0.0.1', 12345))
    s.listen(5)

    con, address = s.accept()

    message = con.recv(2048)
    print(message)

    print("the socket has successfully sent to Alice")


if __name__ == '__main__':
    main()