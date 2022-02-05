

def parse_neighbors():
    file = open('neighbor.txt', 'r', encoding='utf-8')
    content = file.read()

    list_hosts = content.split('\n')

    neighbors = []

    for x in list_hosts:
        address = x[:x.find(":")]
        port = x[x.find(":") + 1:]

        if address == '' or port == '':
            continue

        neighbors.append((address, port))

    return neighbors


def parse_directory():
    file = open('settings.txt', 'r', encoding='utf-8')
    content = file.read()

    directory = content.split('directory:')[1].strip()
    directory = directory.split("\n")[0].strip()

    directory = directory.replace("\n", "")
    return directory.strip()


def parse_ip_addr():
    file = open('settings.txt', 'r', encoding='utf-8')
    content = file.read()

    directory = content.split('ip_addr:')[1].strip()
    directory = directory.split("\n")[0].strip()

    directory = directory.replace("\n", "")
    return directory.strip()