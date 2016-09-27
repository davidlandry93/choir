import socket
from time import sleep

IP = '127.0.0.1'
PORT = 1986

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, PORT))

s.send(bytearray([0x54, 0x01]))
sleep(0.5)
s.send(bytearray([0x54, 0x00]))
s.send(bytearray([0x56, 0x01]))
sleep(0.5)
s.send(bytearray([0x56, 0x00]))
s.send(bytearray([0x58, 0x01]))
sleep(0.5)
s.send(bytearray([0x58, 0x00]))
s.send(bytearray([0x59, 0x01]))
sleep(0.5)
s.send(bytearray([0x59, 0x00]))
s.send(bytearray([0x5B, 0x01]))
sleep(0.5)
s.send(bytearray([0x5B, 0x00]))
s.send(bytearray([0x5D, 0x01]))
sleep(0.5)
s.send(bytearray([0x5D, 0x00]))
s.send(bytearray([0x5F, 0x01]))
sleep(0.5)
s.send(bytearray([0x5F, 0x00]))
s.send(bytearray([0x60, 0x01]))
sleep(0.5)
s.send(bytearray([0x60, 0x00]))

s.send(bytearray([0xFF, 0xFF]))
