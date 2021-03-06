def printlobbysettings(packetint):
    #print(packetint['type'])
    packet = packetint['data']
    #(version, maxplayers, lang, mapid, playerspeedmod, crewlightmod, implightmod, killcooldown, commontasks, shorttasks, emergencies,\
    #                                       impcount, killdist, disctime, votetime, isdefault, emergencycooldown, confirmejects, visualtasks, anonymusvoting, taskbarupdates)
    print('Version: v{}'.format(packet[0]))
    print('Max players: {}'.format(packet[1]))
    print('Language: {}'.format(packet[2]))
    print('Map ID: {}'.format(packet[3]))
    print('Player speed: {}x'.format(packet[4]))
    print('Crew vision: {}x'.format(packet[5]))
    print('Imposter vision: {}x'.format(packet[6]))
    print('Kill cooldown: {}s'.format(packet[7]))
    print('Common tasks: {}'.format(packet[8]))
    print('Long tasks: {}'.format(packet[9]))
    print('Short tasks: {}'.format(packet[10]))
    print('Emergencies: {}'.format(packet[11]))
    print('Imposter count: {}'.format(packet[12]))
    print('Kill distance: {}'.format(packet[13]))
    print('Discussion time: {}'.format(packet[14]))
    print('Voting time: {}'.format(packet[15]))
    print('Is default: {}'.format(packet[16]))
    print('Emergency cooldown: {}'.format(packet[17]))
    print('Confirm ejects: {}'.format(packet[18]))
    print('Visual tasks: {}'.format(packet[19]))
    print('Anonymus voting: {}'.format(packet[20]))
    print('Taskbar updates: {}'.format(['Always', 'In Meetings', 'Never'][packet[21]]))
