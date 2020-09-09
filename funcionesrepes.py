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
        respuestaF = ''
        respuesta30 = ''

        if tamano == 1:
            return 'No en guerra'
        else:
            numero = 0
            contadorF = 0
            contador30 = 0

            while True:
                try:
                    name = str(usuarioClanJson['clan']['participants'][numero]['name'])
                    fame = str(usuarioClanJson['clan']['participants'][numero]['fame'])
                    fameClan = str(usuarioClanJson['clan']['fame'])
                    repairPoints = str(usuarioClanJson['clan']['participants'][numero]['repairPoints'])
                    tag = str(usuarioClanJson['clan']['participants'][numero]['tag'])
                    tag = tag.replace('#', '', 1)
                    posibleNombre = sacarUsuarioConTag(tag)
                    fame30 = (float(fameClan)*0.3)/float(clanMiembros)
                    
                    if posibleNombre != None:
                        name += ' (@' + posibleNombre + ')'
                    
                    if fame == '0':
                        respuestaF += '\t\t ' + name + ', puntos: ' + fame + ', puntos reparación: ' + repairPoints + '\n'
                        contadorF += 1
                    elif float(fame) < fame30 and fame != '0':
                        respuesta30 += '\t\t ' + name + ', puntos: ' + fame + ', puntos reparación: ' + repairPoints + '\n'
                        contador30 += 1

                    numero += 1
                except:
                    break

            if contadorF == 0:
                respuestaF = '\nTodos tienen más de 0 puntos.'
            else:
                respuestaF = '\n' + str(contadorF) + ' ataques que faltan:\n' + respuestaF

            if contador30 == 0:
                respuesta30 = '\nTodos llegan al 30% (' + str(round(fame30, 2)) + ') de ' + fameClan + ' puntos que tiene el clan ahora mismo.'
            else:
                respuesta30 = '\n' + str(contador30) + ' no llegan al 30% (' + str(round(fame30, 2)) + ') de ' + fameClan + ' puntos que tiene el clan ahora mismo:\n' + respuesta30

            if int(fameClan) == 0:
                respuesta = 'Clan sin jugar la guerra.'
            else:
                respuesta = nameClan + ' en guerra:' + respuestaF + respuesta30

            return respuesta
    except:
        return 'Sin clan'