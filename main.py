import socket
import struct
import spigot
import debug
from converting import *
import parse
import create

MATCHMAKERS = {
    'NA' : [
        '50.116.1.42',
        '45.79.5.6',
        '104.237.135.186',
        '198.58.99.71',
        '45.79.40.75',
        '45.79.67.124',
        '198.58.115.57'
    ],
    'EU' : [
        '172.105.249.25',
        '172.105.251,170'
    ],
    'ASIA' : [
        '172.104.96.99',
        '139.162.111.196 '
    ]
}

ipout = MATCHMAKERS['ASIA'][0]
ipaddr = '192.168.100.139'
port = 22023
sockin = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sockout = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
getnonce = None
setnonce = None

sockin.bind((ipaddr, port))
while True:
    datain, addrin = sockin.recvfrom(4096)
    if not datain:
        break
    sockout.sendto(datain, (ipout, port))
    dataout, addrout = sockout.recvfrom(4096)
    f = open('log.log', 'a')
    f.write('[client] <- {}'.format(datain.hex()))
    f.write('[server] -> {}'.format(dataout.hex()))
    f.close()
    sockin.sendto(dataout, addrin)
    #out = parse.packet(data)
    #getnonce = out['nonce']
    #setnonce = create.packet(getnonce, out, sock, database)
