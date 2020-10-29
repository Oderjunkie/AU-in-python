from reliparse import reliparse
from unreliparse import unreliparse
import spigot
def packet(data, clientserv):
    spig = spigot.Spigot()
    spig.feed(data)
    opcode = spig.drip('byte')
    if opcode==0:
        # Unreliable packet.
        return unreliparse(spig, clientserv)
    elif opcode==1:
        # Reliable packet.
        return reliparse(spig, clientserv)
    elif opcode==8:
        # "Hello" packet.
        nonce, hazel, client, name = spig.wet('>@<!4s')
        return {'type':'hello','nonce':nonce,'data':(hazel,client,name)}
    elif opcode==9:
        # "Disconnect" packet.
        spig.dry()
        return {'type':'disconnect','nonce':None}
    elif opcode==10:
        # "Acknowledgement" packet.
        nonce = spig.drip('uint16', '>')
        spig.drip('byte')==255
        return {'type':'acknowledgement','nonce':None, 'data':nonce}
    elif opcode==12:
        # "Ping" packet.
        nonce = spig.drip('uint16')
        return {'type':'ping','nonce':nonce}
    else:
        assert False # Invalid packet
        
