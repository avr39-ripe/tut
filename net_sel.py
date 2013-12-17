#!/usr/bin/env python

import select
import socket
import Queue

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)

server_address = ('', 2607)
server.bind(server_address)
server.listen(5)

inputs = [ server ]
outputs = [ ]
message_queues = {}

while inputs:
    readable, writable, exceptional = select.select(inputs, outputs, [ ] )

    for s in readable:
        if s == server:
            connection, client_address = s.accept()
            print "New client from %s:%d connected!" % client_address
            connection.setblocking(0)
            inputs.append(connection)
            message_queues[connection] = Queue.Queue()
        else:
            data = s.recv(1024)
            if data:
                print "Received %s from client %s:%d" % ((data.strip(),) + client_address)
                if s not in outputs:
                    outputs.append(s)
                message_queues[s].put(data)
            else:
                print "Client %s:%d disconnected!" % client_address
                if s in outputs:
                    outputs.remove(s)
                inputs.remove(s)
                s.close()
                del message_queues[s]
    for s in writable:
        try:
            next_message = message_queues[s].get_nowait()
        except Queue.Empty:
            print "Nothing more to send to %s:%s" % s.getpeername()
            outputs.remove(s)
        else:
            print "Sending %s to %s:%s" % ((next_message.strip(), ) + s.getpeername())
            s.send(next_message)
        