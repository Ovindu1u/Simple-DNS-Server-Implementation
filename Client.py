#Ovindu Undugoda
#BSCP_CS_61_103

import socket
import os

def args_check(args, min, max):
    if len(args) >= min and len(args) <= max:
        return False
    print("Incorrect Usage, type 'help'")
    return True

def print_help(args):
    if args_check(args, 0, 0):
        return

    command_help = {"help": ((), "displays this prompt"),
                    "query": (("type", "query"), "initiates a DNS query"),
                    "clear": ((), "clears terminal"),
                    "quit": ((), "quits program")}
    
    for command in command_help:
        data = command_help[command]
        result = command
        for args in data[0]:
            result = result + f" <{args}>"
        result = result + ": " + data[1]
        print(result)

def wait_reply():
    while True:
        try:
            response, _ = client.recvfrom(1024)
            return response.decode()
        except TimeoutError:
            return 'TIMEOUT'
        except:
            pass


def start_query(args):
    if args_check(args, 2, 2):
        return
    query = f"{args[0]}:{args[1]}".encode()
    client.sendto(query, SERVER)
    response = wait_reply()
    if response == 'NA':
        print("Record does not exist!")
    elif response == 'TIMEOUT':
        print("Server timed out!")
    else:
        response = response.split(':')
        if response[0] == "A":
            print(f"Ip: {response[1]}")
        else:
            print(f"Host: {response[1]}")

def clear_terminal(args):
    if args_check(args, 0, 0):
        return
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Type 'help' for further information")

def quit_program(args):
    if args_check(args, 0, 0):
        return
    quit()

def proccess_commands(command):
    command = command.strip().split(" ")
    if len(command) < 1:
        return
    args = command[1 : len(command)]
    command = command[0]

    match command:
        case "help":
            print_help(args)
        case "query":
            start_query(args)
        case "clear":
            clear_terminal(args)
        case "quit":
            quit_program(args)
        case _:
            print("Unkown command, type 'help'")


SERVER = ('localhost', 45000)

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

client.bind(('localhost', 0))

client.settimeout(3)

print("Type 'help' for further information")

while True:
    command = input("> ")
    proccess_commands(command)
