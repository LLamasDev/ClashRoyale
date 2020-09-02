from db import *

def atacaFuncion(alias,chatId,usuario):
    try:
        usuarioInfoJson = enlace(usuario,'info')
        clan = str(usuarioInfoJson['clan']['tag'])
        clan = clan.replace('#', '', 1)
        nameClan = str(usuarioInfoJson['clan']['name'])
        usuarioClanJson = enlace(clan,'currentRiverRace')
        tamano = len(usuarioClanJson)
        clanMiembro = enlace(clan,'clanMiembros')
        clanMiembros = str(clanMiembro['members'])
        respuesta = 'Ataques que faltan en ' + nameClan + ':\n'
        respuesta20 = ''

        if tamano == 1:
            return 'No en guerra'
        else:
            numero = 0

            while True:
                try:
                    name = str(usuarioClanJson['clan']['participants'][numero]['name'])
                    fame = str(usuarioClanJson['clan']['participants'][numero]['fame'])
                    fameClan = str(usuarioClanJson['clan']['fame'])
                    repairPoints = str(usuarioClanJson['clan']['participants'][numero]['repairPoints'])
                    tag = str(usuarioClanJson['clan']['participants'][numero]['tag'])
                    tag = tag.replace('#', '', 1)
                    posibleNombre = sacarUsuarioConTag(tag)
                    fame20 = (float(fameClan)*0.2)/float(clanMiembros)
                    
                    if posibleNombre != None:
                        name += ' (@' + posibleNombre + ')'
                    
                    if fame == '0':
                        respuesta += name + ', puntos: ' + fame + ', puntos reparación: ' + repairPoints + '\n'
                    elif float(fame) < fame20 and fame != '0':
                        respuesta20 += name + ', puntos: ' + fame + ', puntos reparación: ' + repairPoints + '\n'

                    numero += 1
                except:
                    break

            if len(respuesta20) == 0:
                respuesta = respuesta + '\nLos ' + clanMiembros + ' miembros llegan al 20% (' + str(round(fame20, 2)) + ') de ' + fameClan + ' puntos.'
            else:
                respuesta = respuesta + '\nDe ' + clanMiembros + ' miembros, los que no llegan al 20% (' + str(round(fame20, 2)) + ') de ' + fameClan + ' puntos:\n' + respuesta20


            return respuesta
    except:
        return 'Sin clan'