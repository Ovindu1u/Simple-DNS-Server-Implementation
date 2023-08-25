# Simple-DNS-Server-Implementation

THIS IS A MOCK IMPLEMENTAION IN PYTHON, WOULD NOT INTERFACE WITH A REAL DNS COMMUNICATION

Features

* extremely simlpe
* supports only A and CNAME records
* simlpe file and record handling commands
* no invalid request handling

### Usage Examlpes

Staring the Server (Server):

```
>load records.json
>add A examlpe.com 10.1.1.10
>start
```
Inititating a Query (Client):

```
>query A examlpe.com
Ip: 10.1.1.10
```
Other commands include:

    help: shows the help promt
    stop: stops server
    show: List the records loaded to memory
    remove <ID>: removes the record corresponding to the ID in the show command
    save <file> <Option>: save records in memory to file, use --force or -f to overwrite
    clear: clears terminal
    quit: quits program

    



