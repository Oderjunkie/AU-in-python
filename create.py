from converting import iptobyte, codev2tobyte, pack
from binascii import unhexlify
import struct
class Server:
    def __init__(self, sock):
        self.sock = sock
        self.getnonce = None
        self.sentnonce = None
        self.games = {}
        self.addr = '192.168.100.16'
        self.name = ''
        self.lastID = 0
    def send(self, packet, addrin):
        #print('AAAAA')
        self.sock.sendto(packet, addrin)
        print('[S] ==>> [{}]'.format(packet.hex()))
    def packet(self, pack, addrin):
        type = pack['type']
        #print(type)
        if type=='ping':
            self.send(b'\x0a'+struct.pack('>H', pack['nonce'])+b'\xff', addrin)
            self.getnonce = pack['nonce']
            # We need to respond to this FAST, like so fast I won't
            # even risk putting it in another if statement, or put a
            # comment before it.
        elif type in 'hello disconnect acknowledgement'.split():
            # No processing!!!
            if type=='hello':
                self.getnonce = pack['nonce']
                self.name = pack['data'][2]
                packet = b'\x0a'+struct.pack('>H', self.getnonce)+b'\xff'
                #print(packet)
                self.send(packet, addrin)
            if type=='disconnect':
                self.getnonce = None
                self.sentnonce = None
                self.name = ''
            if type=='acknowledgement':
                assert pack['data']==sentnonce
        else:
            # It's a reliable packet.
            if type=='hostgame':
                self.getnonce = pack['nonce']
                self.send(codev2tobyte('REDSUS'), addrin)
                self.send(b'\x0a'+struct.pack('>H', self.getnonce)+b'\xff', addrin)
                self.send(codev2tobyte('REDSUS'), addrin)
                self.send(b'\x0a'+struct.pack('>H', self.getnonce)+b'\xff', addrin)
                self.games['REDSUS'] = {'addr':(self.addr, 22023),'ID':self.lastID,'players':[self.lastID]}
                self.lastID += 1
                return codev2tobyte('REDSUS')
            elif type=='joingame':
                self.getnonce = pack['nonce']
                code = pack['data']
                packet = codev2tobyte(code)
                packet += unhexlify(self.lastID)+b'\x00\x00\x00'
                packet += unhexlify(self.games[code]['ID'])+b'\x00\x00\x00'
                packet += pack(len(self.games[code]['players']))
                for player in self.games[code]['players']:
                    packet += pack(player)
                self.send(packet)
                self.send(b'\x0a'+struct.pack('>H', self.getnonce)+b'\xff', addrin)
                self.lastID += 1
                return packet
