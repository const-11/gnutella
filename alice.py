import socket
import os
from _thread import *
from message_process import *
from message_handler import *
from utils import *


routing = {}


def multi_threaded_client(connection, address, neighbors):

    data = connection.recv(2048)
    print(data)

    message_id = get_message_id(data)
    payload_type = get_payload_type(data)

    if int(payload_type) == 0:
        handle_ping(connection, message_id)
    elif int(payload_type) == 1:
        handle_pong(data)
    elif int(payload_type) == 2:
        handle_bye(address=address)
    elif int(payload_type) == 64:
        handle_push()
    elif int(payload_type) == 128:
        routing[message_id] = address
        handle_query(data=data, address=address, neighbors=neighbors)
    elif int(payload_type) == 129:
        handle_query_hit(data=data, routing=routing)

    print(routing)

    connection.close()


def main():
    s = socket.socket()
    host = '127.0.0.1'
    port = 6346

    neighbors = parse_neighbors()

    try:
        s.bind((host, port))
    except socket.error as e:
        print(str(e))

    print('Socket is listening..')
    s.listen(5)

    while True:
        connection, address = s.accept()
        print('Connected to: ' + address[0] + ':' + str(address[1]))
        start_new_thread(multi_threaded_client, (connection, address, neighbors))


if __name__ == '__main__':
    main()