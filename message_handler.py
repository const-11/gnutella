from message_process import *
from utils.setting_processing import *
from utils.neighbor_processing import *
import os
import socket


def handle_ping(connection, message_id):
    pong_header = build_pong_header(message_id=message_id)

    my_addr = parse_ip_addr_in_array()

    pong_body = int(6346).to_bytes(2, 'big') +\
                int(my_addr[0]).to_bytes(1, 'big') + \
                int(my_addr[1]).to_bytes(1, 'big') +\
                int(my_addr[2]).to_bytes(1, 'big') + \
                int(my_addr[3]).to_bytes(1, 'big') + \
                int(number_of_files()).to_bytes(4, 'big') + \
                int(size_of_dir()).to_bytes(4, 'big')

    connection.send(pong_header + pong_body)


def handle_pong(data):
    if get_payload_type(data) != 1:
        return False

    return True


def handle_bye(address):
    print("Host with IP: " + str(address[0]) + " is no longer reachable!")


def handle_push(data, address, neighbors):
    payload = get_payload(data)

#   decide if the push was meant for myself
    servent_identifier = int.from_bytes(payload[0:16], byteorder='big')

    if servent_identifier == int(parse_identifier()):
        file_index = int.from_bytes(payload[16:20], byteorder='big')

        host_ip = str(payload[20]) + "." + \
                    str(payload[21]) + "." + \
                    str(payload[22]) + "." + \
                    str(payload[23])

        host_port = int.from_bytes(payload[24].to_bytes(1, 'big') + payload[25].to_bytes(1, 'big'), 'big')
        try:
            with open(parse_directory() + "/" + os.listdir(parse_directory())[file_index], 'r') as file:
                data = file.read().encode()

            send_message(host_ip, int(host_port), data)

        except Exception as ex:
            print(ex)
            return

    else:
        for neighbor in neighbors:
            if address[0] != neighbor[0]:
                try:

                    new_header = build_push_header(get_message_id(data), get_ttl(data) - 1, get_hops(data) + 1)

                    send_message(neighbor[0], int(neighbor[1]), new_header + get_payload(data))

                except Exception as ex:
                    print("Could not connect to neighbor")
                    continue


def handle_query(data, address, neighbors):

    searched_file = get_query_search_criteria(data).decode()

    hits = 0
    file_index = -1
    file_size = -1

    counter = 0

    for file in os.listdir(parse_directory()):
        if searched_file == file:
            hits += 1
            file_index = counter

        counter += 1

#    when there was at least one hit
    if hits > 0:

        my_addr = parse_ip_addr_in_array()

        new_message = int(hits).to_bytes(1, 'big') + \
                       int(8000).to_bytes(2, 'big') + \
                       int(my_addr[0]).to_bytes(1, 'big') + \
                       int(my_addr[1]).to_bytes(1, 'big') + \
                       int(my_addr[2]).to_bytes(1, 'big') + \
                       int(my_addr[3]).to_bytes(1, 'big') + \
                       int(0).to_bytes(4, 'big') + \
                       int(file_index).to_bytes(4, 'big') + \
                       int(size_of_file(parse_directory() + "/" + searched_file)).to_bytes(4, 'big') + \
                       searched_file.encode() + b'0x00' + \
                       int(parse_identifier()).to_bytes(16, 'big')

        new_header = build_query_hit_header(message_id=get_message_id(data), payload_length=len(new_message))

        send_message(address[0], 6346, new_header + new_message)

        return

#   when there was no hit at all
    for neighbor in neighbors:
        if address[0] != neighbor[0]:
            try:
                new_header = build_query_header(get_message_id(data), get_ttl(data) - 1, get_hops(data) + 1, len(get_payload(data)))

                send_message(neighbor[0], int(neighbor[1]), new_header + get_payload(data))

            except Exception as ex:
                print(ex)
                continue
#        print("Query was sent to neighbor")


def handle_query_hit(data, routing):
    message_id = get_message_id(data)
    next_hop = routing.get(message_id)

    if next_hop is None:
        print("We do not have a next hop!")
        return

    if next_hop[0] == parse_ip_addr():
        send_message(next_hop[0], int(parse_port_client()), data)
    else:

        new_header = build_query_hit_header(get_message_id(data), get_ttl(data) - 1, get_hops(data) + 1, len(get_payload(data)))
        send_message(next_hop[0], 6346, new_header + get_payload(data))

    return None
