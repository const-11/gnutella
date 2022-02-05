from random import randint
import socket


def get_message_id(message):
    return message[:16]


def get_payload_type(message):
    return message[16]


def get_ttl(message):
    return message[17]


def get_hops(message):
    return message[18]


def get_payload_length(message):
    return message[19:23]


def get_payload(message):
    return message[23:]


def get_query_search_criteria(message):
    return message[25:]


def build_ping_header(message_id=None, ttl: int = None, hops: int = None):
    if message_id is not None:
        header = message_id
    else:
        header = randint(0, 1000000).to_bytes(16, 'big')

    header += int(0).to_bytes(1, 'big')

    if ttl is not None:
        header += int(ttl).to_bytes(1, 'big')
    else:
        header += int(4).to_bytes(1, 'big')

    if hops is not None:
        header += int(hops).to_bytes(1, 'big')
    else:
        header += int(0).to_bytes(1, 'big')

    header += int(0).to_bytes(4, 'big')

    return header


def build_pong_header(message_id=None, ttl: int = None, hops: int = None):

    if message_id is not None:
        header = message_id
    else:
        header = randint(0, 1000000).to_bytes(16, 'big')

    header += int(1).to_bytes(1, 'big')

    if ttl is not None:
        header += int(ttl).to_bytes(1, 'big')
    else:
        header += int(4).to_bytes(1, 'big')

    if hops is not None:
        header += int(hops).to_bytes(1, 'big')
    else:
        header += int(0).to_bytes(1, 'big')

    header += int(14).to_bytes(4, 'big')

    return header


def build_bye_header():
    return randint(0, 1000000).to_bytes(16, 'big') + int(2).to_bytes(1, 'big') + int(4).to_bytes(1, 'big') + int(0).to_bytes(1, 'big') + int(0).to_bytes(4, 'big')


def build_query_header(message_id=None, ttl: int = None, hops: int = None, payload_length: int = None):
    if message_id is not None:
        header = message_id
    else:
        header = randint(0, 1000000).to_bytes(16, 'big')

    header += int(128).to_bytes(1, 'big')

    if ttl is not None:
        header += int(ttl).to_bytes(1, 'big')
    else:
        header += int(4).to_bytes(1, 'big')

    if hops is not None:
        header += int(hops).to_bytes(1, 'big')
    else:
        header += int(0).to_bytes(1, 'big')

    if payload_length is not None:
        header += int(payload_length).to_bytes(4, 'big')
    else:
        header += int(50).to_bytes(4, 'big')

    return header


def build_query_hit_header(message_id=None, ttl: int = None, hops: int = None, payload_length: int = None):
    if message_id is not None:
        header = message_id
    else:
        header = randint(0, 1000000).to_bytes(16, 'big')

    header += int(129).to_bytes(1, 'big')

    if ttl is not None:
        header += int(ttl).to_bytes(1, 'big')
    else:
        header += int(4).to_bytes(1, 'big')

    if hops is not None:
        header += int(hops).to_bytes(1, 'big')
    else:
        header += int(0).to_bytes(1, 'big')

    if payload_length is not None:
        header += int(payload_length).to_bytes(4, 'big')
    else:
        header += int(50).to_bytes(4, 'big')

    return header


def build_push_header(message_id=None, ttl: int = None, hops: int = None):
    if message_id is not None:
        header = message_id
    else:
        header = randint(0, 1000000).to_bytes(16, 'big')

    header += int(64).to_bytes(1, 'big')

    if ttl is not None:
        header += int(ttl).to_bytes(1, 'big')
    else:
        header += int(4).to_bytes(1, 'big')

    if hops is not None:
        header += int(hops).to_bytes(1, 'big')
    else:
        header += int(0).to_bytes(1, 'big')

    header += int(26).to_bytes(4, 'big')

    return header


def send_message(host_ip: str, host_port: int, data):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.connect((host_ip, host_port))

        s.send(data)

        s.close()
    except Exception as ex:
        print("There was an error while sending data to " + host_ip + ":" + str(host_port))
