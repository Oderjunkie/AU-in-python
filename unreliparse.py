def unreliparse(spig, clientserv):
    length, opcode = spig.wet('2!')
    if opcode==14:
        if clientserv=='server':
            return {'type':'masterserverlist'}
    assert False # Still don't support [MOST] unreliable packets...
