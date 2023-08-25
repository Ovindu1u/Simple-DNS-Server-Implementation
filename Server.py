import socket
import threading
import os
import json

#scroll to the end to see main loop

def respond(request, sender):
    global records_table
    request = request.decode().split(":")
    response = 'NA'
    for record in records_table:
        if record[1] == request[0] and record[2] == request[1]:
            response = f"{record[1]}:{record[3]}"
    server.sendto(response.encode(), sender)

def listen():
    global Listening
    global Stopped
    while not Stopped:
        if Listening:
            try:
                request, sender = server.recvfrom(1024)
                respond(request, sender)
            except:
                pass

def args_check(args, min, max):
    if len(args) >= min and len(args) <= max:
        return False
    print("Incorrect Usage, type 'help'")
    return True

def print_help(a):
    if args_check(a, 0):
        return
    
    command_help = {"help" : ((), "displays this prompt"),
                    "start": ((), "starts server"),
                    "stop" : ((), "stops server"),
                    "load" : (("path/file",), "loads dns records from file(JSON) to memory. OVERWRITES Memory!"),
                    "save" : (("path/file", "options"), "saves DNS records from memory to path/file(JSON). -f / --force OVERWRITES File!"),
                    "show" : ((), "show DNS records in memory"),
                    "add"  : (("type", "query", "response",), "add new DNS record to memory"),
                    "remove" : (("id",), "removes DNS record of given ID from memory"),
                    "clear" : ((), "clears terminal"),
                    "quit" : ((), "quits program"),}
    
    for command in command_help:
        data = command_help[command]
        result = command
        for args in data[0]:
            result = result + f" <{args}>"
        result = result + ": " + data[1]
        print(result)

def start_server(args):
    global Listening
    if args_check(args, 0, 0):
        return
    
    if Listening:
        print("Server is already running!")
    else:
        Listening = True
        print("Server started!")

def stop_server(args):
    if args_check(args, 0, 0):
        return

    global Listening
    if Listening:
        Listening = False
        print("Server stopped!")
    else:
        print("Server is already stopped!")

def load_file(args):
    if args_check(args, 1, 1):
        return
    
    global records_table
    path = args[0]
    try:
        with open(path, "r") as file:
            records = json.load(file)
            for i, record in enumerate(records):
                record.insert(0, str(i))
        records_table = records
        print(len(records), " records have been loaded in memory!")
    except Exception as e:
        print("Error occred while loading records: ", e)

def save_file(args):
    if args_check(args, 1, 2):
        return
    
    path = args[0]
    if len(args) == 2:
        overwrite = args[1] == "-f" or args[1] == "--force"
    else:
        overwrite = False

    if os.path.isfile(path) and not overwrite:
        print("File already exists, use -f or --force to overwrite")
        return
    try:
        with open(path, "w") as file:
            data = [record[1 : len(record)] for record in records_table]
            data = json.dumps(data).replace("],", "],\n").replace("[[", "[\n [").replace("]]", "]\n]").replace("[\"", "   [\"")
            file.write(data)
            print(len(records_table), " saved to ", os.path.abspath(path))
    except Exception as e:
        print("Error occured when saving: ", e)

def show_records(args):
    if args_check(args, 0, 0):
        return
    
    global records_table
    records = records_table
    columns = ("ID", "Type", "Query", "Response")
    min_spacing = [6, 8, 7, 0]

    if records_table == []:
        print("No records saved in memory, use 'load' to get records from file!")
        return
    
    columns_ordered = [[record[i] for record in records] for i in range(len(columns))]
    max_length = [len(max(column, key=len)) for column in columns_ordered]
    spacing = [(j + 4) if j + 4 > i else i for i, j in zip(min_spacing, max_length)]
    records.insert(0, columns)
    for record in records:
        result = "".join(f"{data:<{space}}" for data, space in zip(record, spacing))
        print(result)
    records.remove(columns)

def add_record(args):
    if args_check(args, 3, 3):
        return
    record_type = args[0]
    query = args[1]
    response = args[2]
    global records_table

    next_index = int(records_table[len(records_table)-1][0]) + 1
    records_table.append([str(next_index), record_type, query, response])

def remove_record(args):
    if args_check(args, 1, 1):
        return
    global records_table
    index = args[0]
    records_table = [record for record in records_table if record[0] != index]

def clear_terminal(args):
    if args_check(args, 0, 0):
        return
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Type 'help' for further information")

def quit_program(args):
    if args_check(args, 0, 0):
        return
    global Stopped
    Stopped = True
    listenthread.join(1)
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
        case "start":
            start_server(args)
        case "stop":
            stop_server(args)
        case "load":
            load_file(args)
        case "save":
            save_file(args)
        case "show":
            show_records(args)
        case "add":
            add_record(args)
        case "remove":
            remove_record(args)
        case "clear":
            clear_terminal(args)
        case "quit":
            quit_program(args)
        case _:
            print("Unkown command, type 'help'")


records_table = []

PORT = 45000

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(('localhost', PORT))
server.settimeout(1)

Listening = False
Stopped = False

listenthread = threading.Thread(target=listen)

listenthread.start()

print("Type 'help' for further information")

while True:
    command = input("> ")
    proccess_commands(command)
    