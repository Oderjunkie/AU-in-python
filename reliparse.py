def reliparse(spig):
    nonce, length, opcode = spig.wet('@@1')
    if opcode==0:
        # "Host Game"
        length = spig.drip('packed')
        version, maxPlay, language, mapId, plSpMod, crLiMod,\
        imLiMod, kiCool, common, long, short, emerg, impCount,\
        killDist, disc, voting, isDefault = spig.wet('!!$!ffff!!!4!!44?')
        emergency, confirmEjects, visualTasks,\
        anonymusVoting, taskBarUpdates = [20, True, True, False, 0]
        if version>1:
            emergency = spig.wet('!')
            if version>2:
                confirmEjects, visualTasks = spig.wet('??')
                if version>3:
                    anonymusVoting, taskBarUpdates = spig.wet('?!')
        return {'type':'hostgame', 'nonce':nonce, 'data':(version, maxPlay, language, mapId, plSpMod, crLiMod, imLiMod,\
                                                          kiCool, common, long, short, emerg, impCount, killDist,\
                                                          disc, voting, isDefault, emergency, confirmEjects,\
                                                          visualTasks, anonymusVoting, taskBarUpdates)}
    elif opcode==1:
        # "Join Game"
        code, mapown = spig.wet('c!')
        return {'type':'joingame', 'nonce':nonce, 'data':code}
    elif opcode==16:
        #length = spig.drip('packed')
        version = spig.drip('byte')
        maxPlay = spig.drip('byte')
        language = spig.drip('uint32')
        mapId = spig.drip('byte')
        plSpMod = spig.drip('float32')
        crLiMod = spig.drip('float32')
        imLiMod = spig.drip('float32')
        kiCool = spig.drip('float32')
        common = spig.drip('byte')
        long = spig.drip('byte')
        short = spig.drip('byte')
        emerg = spig.drip('int32')
        impCount = spig.drip('byte')
        killDist = spig.drip('byte')
        disc = spig.drip('int32')
        voting = spig.drip('int32')
        isDefault = spig.drip('boolean')
        emergency = 20
        confirmEjects = True
        visualTasks = True
        anonymusVoting = False
        taskBarUpdates = 0
        if version>1:
            emergency = spig.drip('byte')
            if version>2:
                confirmEjects = spig.drip('boolean')
                visualTasks = spig.drip('boolean')
                if version>3:
                    anonymusVoting = spig.drip('boolean')
                    taskBarUpdates = spig.drip('byte')
        return {'type':'getgamelist', 'nonce':nonce, 'data':(version, maxPlay, language, mapId, plSpMod, crLiMod, imLiMod,\
                                                          kiCool, common, long, short, emerg, impCount, killDist,\
                                                          disc, voting, isDefault, emergency, confirmEjects,\
                                                          visualTasks, anonymusVoting, taskBarUpdates)}
