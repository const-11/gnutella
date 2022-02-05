import socket
import os
from _thread import *
from message_process import *
from message_handler import *
from utils.setting_processing import *
from utils.neighbor_processing import *


routing = {}


def process_message(connection, address, neighbors):

    data = connection.recv(2048)

    message_id = get_message_id(data)
    payload_type = get_payload_type(data)

    if get_ttl(data) == 0:
        return

    ############################################################
    # TODO 2.5.8.: enter the correct number in the if-statements
    ############################################################

    if int(payload_type) == -1:
        handle_ping(connection, message_id)

    elif int(payload_type) == -1:
        handle_pong(data)

    elif int(payload_type) == -1:
        handle_bye(address=address)

    elif int(payload_type) == -1:

        if routing.get(message_id) is not None:
            return

        routing[message_id] = address
        handle_push(data=data, address=address, neighbors=neighbors)

    elif int(payload_type) == -1:

        if routing.get(message_id) is not None:
            return

        routing[message_id] = address
        handle_query(data=data, address=address, neighbors=neighbors)

    elif int(payload_type) == -1:
        handle_query_hit(data=data, routing=routing)

    connection.close()


def main():
    s = socket.socket()
    host = parse_ip_addr()
    port = 6346

    neighbors = parse_neighbors()

    try:

        ####################################################################################
        # TODO 2.5.2.: bind socket on port 6346 and the hosts´s ip address and start listening on
        ####################################################################################

        print('Socket is listening on ' + host + ":6346 ...")
    except socket.error as e:
        print(str(e))

    while True:
        connection, address = s.accept()
        print('Connected to: ' + address[0] + ':' + str(address[1]))
        start_new_thread(process_message, (connection, address, neighbors))


if __name__ == '__main__':
    main()