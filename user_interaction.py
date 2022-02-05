import os
from utils.setting_processing import parse_directory


def ask_for_user_choice():
    while True:
        print('Which message do you want to send?')
        print("1) Ping")
        print("2) Query")
        number = input('Enter a number: ')
        try:
            number = int(number)

            if number < 1 or number > 2:
                raise Exception
            else:
                return number

        except Exception as ex:
            print('\n! Please enter a valid number !\n')


def ask_for_request_file():
    searched_file = input('Requested file: ')

    for file in os.listdir(parse_directory()):
        if searched_file == file:
            print("\nFile is already on your local machine! \n")
            return None

    return searched_file


def ask_for_download_host(found_hosts):
    while True:

        print("\nWhere do you want to download the file from?")

        for counter in range(0, len(found_hosts)):
            print(str(counter + 1) + ") " + str(found_hosts[counter][1]) + ":" + str(found_hosts[counter][2]))
        try:
            number = input("Your choice: ")
            number = int(number)

            if number < 1 or number > len(found_hosts):
                raise Exception
            else:
                return number

        except Exception as ex:
            print("\n! Please enter a valid number !\n")


def print_available_hosts(counter_verified, neighbors, not_reachable_hosts):
    print("\n" + str(counter_verified) + "/" + str(len(neighbors)) + " neighbors could be succesfully verified!\n")

    if len(not_reachable_hosts) > 0:
        print("Following host(s) are not reachable:")
        for host in not_reachable_hosts:
            print("- " + str(host))


def print_found_hosts(found_hosts):
    if len(found_hosts) == 0:
        print("We did not received any results!")
        return found_hosts

    print("We received results from following hosts: ")
    for x in found_hosts:
        print("- (Hits: " + str(x[0]) + ", IP: " + str(x[1]) + ", Port: " + str(x[2]) + ", Identifier: " + str(x[3]))


def ask_user_for_push():
    while True:
        try:
            print("\nDo you want to obtain the file via PUSH message?")
            answer = input("yes/no: ")
            if answer == 'no' or answer == 'yes':
                return answer

            raise Exception

        except Exception as ex:
            print("Please enter\'yes\' or \'no\'")