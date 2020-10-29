import struct
from converting import unpack, bytetocodev1, bytetocodev2
class Spigot:
    def __init__(self):
        self.bytearr = []
    def feed(self, newarr=b''):
        if not self.bytearr:
            self.bytearr = bytearray(newarr)
            return None
        else:
            return self.bytearr.pop(0)
    def dry(self):
        self.bytearr = bytearray(b'')
    def drip_help(self, form):
        if form[-1] in 'xcbB?':
            return struct.unpack(form, bytes([self.feed()]))[0]
        if form[-1] in 'hH':
            return struct.unpack(form, bytes([self.feed(),self.feed()]))[0]
        if form[-1] in 'iIlLf':
            return struct.unpack(form, bytes([self.feed(),self.feed(),self.feed(),self.feed()]))[0]
        if form[-1] in 'qQd':
            return struct.unpack(form, bytes([self.feed(),self.feed(),self.feed(),self.feed(),self.feed(),self.feed(),self.feed(),self.feed()]))[0]
    def drip(self, type, endian='<'):
        form = endian
        #print(type)
        if type not in ['string', 'packed', 'codev1', 'codev2', 'code']:
            if type=='boolean': form += '?'                         #   Boolean
            if type in ['int8']: form += 'b'                        #   1
            if type in ['byte', 'uint8']: form += 'B'               #   u1
            if type in ['short', 'int16']: form += 'h'              #   2
            if type in ['ushort', 'uint16']: form += 'H'            #   u2
            if type in ['int', 'int32']: form += 'i'                #   4
            if type in ['uint', 'uint32']: form += 'I'              #   u4
            if type=='long': form += 'q'                            #   8
            if type=='ulong': form += 'Q'                           #   u8
            if type in ['float', 'float32']: form += 'f'            #   4
            if type=='double': form += 'd'                          #   8
            return self.drip_help(form)
        else:
            if type=='string':
                len = self.feed()
                str = b''
                while len>0:
                    str += bytes([self.feed()])
                    len -= 1
                return str.decode()
            if type=='packed':
                return unpack(self)
            if type=='codev1':
                return bytetocodev1(bytes([self.feed(), self.feed(), self.feed(), self.feed()]))
            if type=='codev2':
                return bytetocodev2(bytes([self.feed(), self.feed(), self.feed(), self.feed()]))
            if type=='code':
                code = [self.feed(), self.feed(), self.feed(), self.feed()]
                if 0x20<code[0]<0x70 and\
                   0x20<code[1]<0x70 and\
                   0x20<code[2]<0x70 and\
                   0x20<code[3]<0x70:
                    return bytetocodev1(bytes(code))
                return bytetocodev2(bytes(code))
    def wet(self, cusform):
        out = []
        form = cusform
        endian = '@'
        if cusform[0] in '<>':
            endian = cusform[0]
            form = cusform[1:]
        for char in form:
            #print('a: ', char)
            if char=='x': self.feed()
            elif char=='?': out.append(self.drip('boolean', endian))
            elif char=='1': out.append(self.drip('int8', endian))
            elif char=='!': out.append(self.drip('uint8', endian))
            elif char=='2': out.append(self.drip('int16', endian))
            elif char=='@': out.append(self.drip('uint16', endian))
            elif char=='4': out.append(self.drip('int32', endian))
            elif char=='$': out.append(self.drip('uint32', endian))
            elif char=='8': out.append(self.drip('long', endian))
            elif char=='*': out.append(self.drip('ulong', endian))
            elif char=='4': out.append(self.drip('uint16', endian))
            elif char=='f': out.append(self.drip('float', endian))
            elif char=='d': out.append(self.drip('double', endian))
            elif char=='s': out.append(self.drip('string'))
            elif char=='p': out.append(self.drip('packed'))
            elif char=='c': out.append(self.drip('code'))
            elif char=='v': out.append(self.drip('codev2'))
            elif char=='V': out.append(self.drip('codev1'))
        return out
