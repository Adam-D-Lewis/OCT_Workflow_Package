#!/usr/bin/env python

import socket

HOST = "localhost"
PORT = 65500

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

sock.send(bytearray("Hello\n", encoding='ascii'))
sock.close()
print("Socket closed")