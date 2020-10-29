from converting import iptobyte
def packet(getnonce, pack, sock, database):
    type = pack['type']
    if type=='joingame':
        ip = database[pack['data']]
        iptobyte(ip)+b'\x07V'
