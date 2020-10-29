import struct
def iptobyte(ip):
    byte = ip.split('.')
    return struct.pack('BBBB', int(byte[0]), int(byte[1]), int(byte[2]), int(byte[3]))

def bytetoip(encoded):
    unpack = struct.unpack('BBBB', encoded)
    unpack = [str(i) for i in unpack]
    return '.'.join(unpack)

def bytetocodev1(byte):
    return byte.decode('UTF-8')

def codev1tobyte(string):
    return string.encode('UTF-8')

def codev2tobyte(string):
    byte = string.encode('UTF-8')
    table = [0x19,0x15,0x13,0x0A,0x18,0x0B,0x0C,0x0D,0x16,0x0F,0x10,0x06,0x18,0x17,0x12,0x07,0x00,0x03,0x09,0x04,0x0E,0x14,0x01,0x02,0x05,0x11]
    A = table[byte[0]-65]
    B = table[byte[1]-65]
    C = table[byte[2]-65]
    D = table[byte[3]-65]
    E = table[byte[4]-65]
    F = table[byte[5]-65]
                    #one = ( A + 26 * B ) & 0x3FF
    one = ( A + 26 * B )
    two = ( C + 26 * ( D + 26 * ( E + 26 * F ) ) )
                    #print(one)
                    #res = ( one | ( ( two << 10 ) & 0x3FFFFC00 ) | 0x80000000 )
    res = ( one | ( two << 10 ) | 0x80000000 )
    return struct.pack('I', res)

def bytetocodev2(byte):
    res = struct.unpack('I', byte)[0]
    res ^= 0x80000000
                    # res = one | ( two << 10 )
                    # res = EETT TTTT TTTT TTTT TTTT TTOO OOOO OOOO
    two = res & 0x3FFFFC00
    two >>= 10
    one = res & 0x3FF
    A = one % 26
    C = two % 26    # WE GOT 2 VARIABLES!
    B = one - A
    B /= 26         # WHICH GETS THE NEXT ONE
    Comb = two - C
    Comb /= 26
                    # Comb = D + 26 * ( E + 26 * F )
    D = Comb % 26
    Comb2 = Comb - D
    Comb2 /= 26
                    # Comb2 = E + 26 * F
    E = Comb2 % 26
    F = Comb2 - E
    F /= 26
                    # A B C D E and F have been calculated.
    table = [0x19,0x15,0x13,0x0A,0x18,0x0B,0x0C,0x0D,0x16,0x0F,0x10,0x06,0x18,0x17,0x12,0x07,0x00,0x03,0x09,0x04,0x0E,0x14,0x01,0x02,0x05,0x11]
    charA = table.index(A)+65
    charB = table.index(B)+65
    charC = table.index(C)+65
    charD = table.index(D)+65
    charE = table.index(E)+65
    charF = table.index(F)+65
    chars = bytes([charA, charB, charC, charD, charE, charF])
    return chars.decode()

def pack(val):
    buffer = b''
    while val>0:
        b = val & 0xFF
        if val >= 0x80:
            b |= 0x80
        buffer += bytes([b])
        val >>= 7
    return buffer

def unpack(spigot):
    reading = True
    shift = 0
    out = 0
    while reading:
        b = spigot.feed()
        if b>=0x80:
            reading = True
            b ^= 0x80
        else:
            reading = False
        out |= b << shift
        shift += 7
    return out
