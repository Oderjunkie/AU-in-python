from reliparse import reliparse
#from unreliparse import unreliparse
import spigot
def packet(data):
    spig = spigot.Spigot()
    spig.feed(data)
    opcode = spig.drip('byte')
    if opcode==0:
        # Unreliable packet.
        return unreliparse(spig)
    elif opcode==1:
        # Reliable packet.
        return reliparse(spig)
    elif opcode==8:
        # "Hello" packet.
        nonce  = spig.drip('uint16')
        hazel  = spig.drip('byte')
        client = spig.drip('int32')
        name   = spig.drip('string')
        return {'type':'hello','nonce':nonce,'data':(hazel,client,name)}
    elif opcode==9:
        # "Disconnect" packet.
        spig.dry()
        return {'type':'disconnect','nonce':None}
    elif opcode==10:
        # "Acknowledgement" packet.
        nonce = spig.drip('uint16')
        assert spig.drip('byte')==255
        return {'type':'acknowledgement','nonce':None, 'data':nonce}
    elif opcode==12:
        # "Ping" packet.
        nonce = spig.drip('uint16')
        return {'type':'ping','nonce':nonce}
