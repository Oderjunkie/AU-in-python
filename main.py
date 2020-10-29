from binascii import unhexlify
from converting import *
import threading
import socket
import struct
import spigot
import create
import random
import debug
import parse

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
        '139.162.111.196'
    ]
}

#area = 'ASIA'
#ipout = MATCHMAKERS[area]
#ipout = ipout[random.randint(0,len(ipout)-1)]
ipout = '192.168.100.16'
print(ipout)
ipaddr = '192.168.100.139'
port = 22023
sockin = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sockout = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
getnonce = None
setnonce = None
sockin.bind((ipaddr, port))
parseerrors = 0
server = create.Server(sockin)
def startserver():
    global port
    global ipout
    global ipaddr
    global server
    global sockin
    global sockout
    global parseerrors
    while True:
        datain, addrin = sockin.recvfrom(4096)
        if not datain:
            continue
        #dataout, addrout = sockout.recvfrom(4096)
        intin, intout = '{}', '{}'
        f = open('420log.log', 'a')
        try:
            intin = parse.packet(datain, 'client')
            f.write('[C] <<== {}\r\n'.format(str(intin)))
            print('[C] <<== {}'.format(str(intin)))
            pack = server.packet(intin, addrin)
            #intout = parse.packet(pack, 'server')
            #f.write('[S] ==>> [{}]\n'.format(pack.hex()))
            #print(intin)
        except Exception:
            parseerrors += 1
            f.write('[C] <<== [{}]\r\n'.format(datain.hex()))
        #try:
        #    intout = parse.packet(dataout, 'server')
        #    f.write('[S] ==>> {}\r\n'.format(str(intout)))
        #    if intout['type']=='redirect':
        #        ipout, port = intout['data']
        #except Exception:
        #    parseerrors += 1
        #    f.write('[S] ==>> [{}]\r\n'.format(dataout.hex()))
        f.close()
        #sockin.sendto(dataout, addrin)
        #out = parse.packet(data)
        #getnonce = out['nonce']
        #setnonce = create.packet(getnonce, out, sock, database)
def InterruptableEvent():
    e = threading.Event()

    def patched_wait():
        while not e.is_set():
            e._wait(3)

    e._wait = e.wait
    e.wait = patched_wait
    return e
#startserver()
process = threading.Thread(target=startserver, args=())
process.daemon = True
process.start()
e = InterruptableEvent()
while True:
    try:
        e.wait()
    except KeyboardInterrupt:
        break
