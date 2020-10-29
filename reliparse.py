from converting import bytetoip
def reliparse(spig, cliserv):
    nonce, length, opcode = spig.wet('>@<@!')
    if opcode==0:
        # "Host Game"
        length, version, maxPlay, language, mapId, plSpMod, crLiMod,\
        imLiMod, kiCool, common, long, short, [emerg,], impCount,\
        killDist, disc, voting, isDefault = spig.wet('p!!$!ffff!!!4!!44?')
        emergency, confirmEjects, visualTasks,\
        anonymusVoting, taskBarUpdates = [20, True, True, False, 0]
        if version>1:
            emergency = spig.wet('!')
            if version>2:
                confirmEjects, visualTasks = spig.wet('??')
                if version>3:
                    anonymusVoting, taskBarUpdates = spig.wet('?!')
        spig.dry()
        assert spig.feed()==None
        return {'type':'hostgame', 'nonce':nonce, 'data':(version, maxPlay, language, mapId, plSpMod, crLiMod, imLiMod,\
                                                          kiCool, common, long, short, emerg, impCount, killDist,\
                                                          disc, voting, isDefault, emergency, confirmEjects,\
                                                          visualTasks, anonymusVoting, taskBarUpdates)}
    elif opcode==1:
        # "Join Game"
        code, mapown = spig.wet('c!')
        assert spig.feed()==None
        return {'type':'joingame', 'nonce':nonce, 'data':code}
    elif opcode==16:
        # "Game List Request" HOW DOES THIS JANK FORMAT EVEN WORKKKKK
        if cliserv=='client':
            length, version, language, mapId, impCount = spig.wet('px!x$!xxxxxxxxxxxxxxxxxxxxxxx!xxxxxxxxxx')
            emergency, confirmEjects, visualTasks,\
            anonymusVoting, taskBarUpdates = [20, True, True, False, 0]
            if version>1:
                emergency = spig.wet('!')
                if version>2:
                    confirmEjects, visualTasks = spig.wet('??')
                    if version>3:
                        anonymusVoting, taskBarUpdates = spig.wet('?!')
            spig.dry()
            assert spig.feed()==None
            return {'type':'gamelistrequest', 'nonce':nonce, 'data':(language, mapId, impCount)}
        elif cliserv=='server':
            spig.wet('xxx')
            arr = []
            while spig.bytearr:
                arr.append(spig.wet('@xi@cs!p!!!'))
            return {'type':'gamelist', 'nonce':nonce, 'data':arr}
    elif opcode==13:
        # "Redirect"
        ip, port = spig.wet('i@')
        assert spig.feed()==None
        return {'type':'redirect', 'nonce':nonce, 'data':(ip, port)}
    else:
        print(opcode)
        assert False # what
