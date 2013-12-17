#!/usr/bin/env python

import select
import socket
import Queue
import re

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)

server_address = ('', 2607)
server.bind(server_address)
server.listen(5)

inputs = [ server ]
outputs = [ ]
message_bufs = {}
result_queue = {}

temp=10.1
delta=3
step=4.3

def getvar(**kwargs):
    if kwargs['varname'] in globals():
        return globals()[kwargs['varname']]

def setvar(**kwargs):
    if kwargs['varname'] in globals():
        globals()[kwargs['varname']] = kwargs['value']
        return globals()[kwargs['varname']]

cmds= { 'GET': getvar, 'SET': setvar }

while inputs:
    readable, writable, exceptional = select.select(inputs, outputs, [ ] )

    for s in readable:
        if s == server:
            connection, client_address = s.accept()
            print "New client from %s:%d connected!" % client_address
            connection.setblocking(0)
            inputs.append(connection)
            message_bufs[connection] = ''
            result_queue[connection] = Queue.Queue()
        else:
            data = s.recv(1024)
            if data:
                print "Received %s from client %s:%d" % ((data.strip(),) + client_address)
                if s not in outputs:
                    outputs.append(s)
                message_bufs[s] += data
                if message_bufs[s].find('\n') != -1:
                    next_message, message_bufs[s] = message_bufs[s].split('\n',1)
                    command, variable, value = re.search(r"\s*(\w+)\s+(\w+)(?:\s*=\s*([-+]?(?:[0-9]*\.[0-9]+|[0-9]+)))?",next_message).groups()
                    print command, variable, value
                    cmd_result = cmds[command](varname=variable, value=value)
                    result_queue[s].put_nowait(cmd_result)
                    print "TVAL" , cmd_result
                    
            else:
                print "Client %s:%d disconnected!" % client_address
                if s in outputs:
                    outputs.remove(s)
                inputs.remove(s)
                s.close()
                del message_bufs[s]
                del result_queue[s]
    for s in writable:
        try:
            message = result_queue[s].get_nowait()
            print "Sending %s to %s:%s" % ((message, ) + s.getpeername())
            s.send(str(message)+'\n')
        except Queue.Empty:
            print "Nothing more to send to %s:%s" % s.getpeername()
            outputs.remove(s)
            