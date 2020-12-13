from db import *

def atacaFuncion(alias,chatId,usuario):
    try:
        usuarioInfoJson = enlace(usuario,'info')
        clan = str(usuarioInfoJson['clan']['tag'])
        clan = clan.replace('#', '', 1)
        nameClan = str(usuarioInfoJson['clan']['name'])
        usuarioClanJson = enlace(clan,'currentRiverRace')
        usuariosMiembrosClanJson = enlace(clan,'clan')
        tamano = len(usuarioClanJson)
        clanMiembro = enlace(clan,'clanMiembros')
        clanMiembros = str(clanMiembro['members'])
        respuestaF = ''
        respuesta30 = ''
        numeroClan = 0
        todosLosMiembros = []

        while True:
            try:
                tag = str(usuariosMiembrosClanJson['items'][numeroClan]['tag'])
                tag = tag.replace('#', '', 1)
                todosLosMiembros.append(tag)

                numeroClan += 1
            except:
                break

        if tamano == 1:
            return 'No en guerra'
        else:
            numero = 0
            miembrosDelClan = []
            miembros0Puntos = []
            miembros30Puntos = []

            while True:
                try:
                    tag = str(usuarioClanJson['clan']['participants'][numero]['tag'])
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
                        lista = [tag,name,fame,repairPoints]
                        miembros0Puntos.append(lista)
                    elif float(fame) < fame30 and fame != '0':
                        lista = [tag,name,fame,repairPoints]
                        miembros30Puntos.append(lista)

                    numero += 1
                except:
                    break

            if len(miembros0Puntos) == 0:
                respuestaF = '\nTodos tienen más de 0 puntos.'
            else:
                respuestaF = '\nAtaques que faltan:\n' + respuestaF

            if len(miembros30Puntos) == 0:
                respuesta30 = '\nTodos llegan al 30% (' + str(round(fame30, 2)) + ') de ' + fameClan + ' puntos que tiene el clan ahora mismo.'
            else:
                respuesta30 = '\nNo llegan al 30% (' + str(round(fame30, 2)) + ') de ' + fameClan + ' puntos que tiene el clan ahora mismo:\n'

            if int(fameClan) == 0:
                respuesta = 'Clan sin jugar la guerra.'
            else:
                for x in miembros0Puntos:
                    for i in todosLosMiembros:
                        if x[0] == i:
                            respuestaF += '\t\t ' + x[1] + ', puntos: ' + x[2] + ', puntos reparación: ' + x[3] + '\n'

                miembros30Puntos.sort(key=lambda x: (x[2], x[3]), reverse=True)
                
                for x in miembros30Puntos:
                    for i in todosLosMiembros:
                        if x[0] == i:
                            respuesta30 += '\t\t ' + x[1] + ', puntos: ' + x[2] + ', puntos reparación: ' + x[3] + '\n'

                respuesta = nameClan + ' en guerra:' + respuestaF + respuesta30
                
            return respuesta
    except Exception as e:
        print(e)
        return 'Sin clan'