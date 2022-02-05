from message_handler import *
from message_process import *
import requests
from utils.setting_processing import *
from utils.neighbor_processing import *
from user_interaction import ask_for_user_choice
from user_interaction import ask_for_request_file
from user_interaction import ask_for_download_host
from user_interaction import ask_user_for_push
from user_interaction import print_available_hosts
from user_interaction import print_found_hosts
import socket


def ping_all_neighbors():
    neighbors = parse_neighbors()

    counter_verified = 0
    not_reachable_hosts = []

    for neighbor in neighbors:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            s.connect((neighbor[0], int(neighbor[1])))
        except Exception as ex:
            not_reachable_hosts.append((neighbor[0], neighbor[1]))
            s.close()
            continue

        ping_message = build_ping_header()

        message_id = None
        ##########################################################
        # TODO 2.6.4: extract the message_id from the ping message
        ##########################################################

        s.send(ping_message)
        data = s.recv(2048)

        if handle_pong(data):
            if get_message_id(data) != message_id:
                not_reachable_hosts.append((neighbor[0], neighbor[1]))
                s.close()
                continue
            else:
                counter_verified += 1
        else:
            not_reachable_hosts.append((neighbor[0], neighbor[1]))

        s.close()

#   print output for the user
    print_available_hosts(counter_verified, neighbors, not_reachable_hosts)


def handle_results(host_ip):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host_ip, int(parse_port_client())))

    s.listen(5)
    s.settimeout(5)

    found_hosts = []

    while True:
        try:
            con, address = s.accept()
            message = con.recv(2048)

            number_hits = message[23]

            host_addr = str(message[26]) + "." +\
                        str(message[27]) + "." +\
                        str(message[28]) + "." +\
                        str(message[29])

            host_port = int.from_bytes(message[24].to_bytes(1, 'big') + message[25].to_bytes(1, 'big'), 'big')

            payload = get_payload(message)

            servent_identifier = int.from_bytes(payload[len(payload) - 16:], byteorder='big')
            file_index = int.from_bytes(payload[11:15], byteorder='big')

            found_hosts.append((number_hits, host_addr, host_port, servent_identifier, file_index))

        except Exception as ex:
            print("\nNo further results incoming ...\n")
            break

    s.close()

    print_found_hosts(found_hosts)

    return found_hosts



#######################################################################
# TODO 4.8: Place the obtain_file_via_push method at the right position
#           in the download_file method and return its output
########################################################################

def download_file(host_ip, host_port, host_identifier, file_index, file):
    url = ""

    ###################################################################
    # TODO 2.6.10: edit the url where the GET-request should be sent to
    ###################################################################

    try:

        r = requests.get(url, params={}, timeout=5)

        #########################################################################################################
        # TODO 2.6.12: edit the condition of the if-statement so that an exception will be thrown if the request was NOT succesful
        #########################################################################################################
        if r.status_code != -1:
            raise Exception

    except Exception as ex:
        print("\n There was an error while file transfer, e.g. firewall! \n")
        return False

    try:

        open(parse_output_dir() + '/' + file, 'wb').write(r.content)

        print("\nThe file has been succesfully downloaded!\n")
        return True

    except Exception as ex:
        print("\nThere was an I/O error on your machine\n")
        return False


def obtain_file_via_push(host_identifier, file, file_index):
    if ask_user_for_push() == 'no':
        return False

    my_addr = parse_ip_addr_in_array()
    message_header = build_push_header()
    message_body = int(host_identifier).to_bytes(16, 'big') +\
                       int(file_index).to_bytes(4, 'big') + \
                       int(my_addr[0]).to_bytes(1, 'big') + \
                       int(my_addr[1]).to_bytes(1, 'big') + \
                       int(my_addr[2]).to_bytes(1, 'big') + \
                       int(my_addr[3]).to_bytes(1, 'big') + \
                       int(parse_port_client()).to_bytes(2, 'big')

    ############################################
    # TODO 4.10.: initialize message correctly
    ############################################
    message = ''

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((parse_ip_addr(), 6346))

    s.send(message)
    s.close()

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((parse_ip_addr(), int(parse_port_client())))
        s.listen(5)
        s.settimeout(5)

        con, address = s.accept()
        message_recv = con.recv(2048).decode()

    except Exception as ex:
        print("We did not receive a message or there was an error with the transfer")
        return False

    open(parse_output_dir() + '/' + file, 'w').write(message_recv)

    print("\n Download succesful! \n")

    return True


def main():

    host_ip = parse_ip_addr()
    port = 6346

    ping_all_neighbors()

    choice = ask_for_user_choice()

#   user chose to send another ping message to his neighbors
    if choice == 1:
        ping_all_neighbors()

#   user chose to send a query
    else:

#       user is asked for the file he wants to request
        searched_file = ask_for_request_file()

        if searched_file is None:
            return

        query = build_query_header(payload_length=2 + len(searched_file)) + int(0).to_bytes(2, 'big') + searched_file.encode()

        send_message(host_ip, port, query)

        found_hosts = handle_results(host_ip)

        if len(found_hosts) == 0:
            print("\nThere were no results for your request")
            return

#       user is asked for the host where he wants to download the file
        host_index = ask_for_download_host(found_hosts)

#       the file will be downloaded from the host and returns if the download was successful or not
        success = download_file(found_hosts[host_index - 1][1], found_hosts[host_index - 1][2],
                                found_hosts[host_index - 1][3], found_hosts[host_index - 1][4], searched_file)


if __name__ == '__main__':
    main()