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
            miembrosSinJugar = []
            miembrosJugando = []

            while True:
                try:
                    tag = str(usuarioClanJson['clan']['participants'][numero]['tag'])
                    name = str(usuarioClanJson['clan']['participants'][numero]['name'])
                    fame = str(usuarioClanJson['clan']['participants'][numero]['fame'])
                    fameClan = str(usuarioClanJson['clan']['fame'])
                    repairPoints = str(usuarioClanJson['clan']['participants'][numero]['repairPoints'])
                    boatAttacks = str(usuarioClanJson['clan']['participants'][numero]['boatAttacks'])
                    decksUsed = int(usuarioClanJson['clan']['participants'][numero]['decksUsed'])
                    decksUsedToday = int(usuarioClanJson['clan']['participants'][numero]['decksUsedToday'])
                    tag = str(usuarioClanJson['clan']['participants'][numero]['tag'])
                    tag = tag.replace('#', '', 1)
                    posibleNombre = sacarUsuarioConTag(tag)

                    if posibleNombre != None:
                        name += ' (@' + posibleNombre + ')'

                    lista = [tag,name,decksUsedToday,decksUsed,fame,repairPoints,boatAttacks]

                    if decksUsedToday == 0 or decksUsedToday == 1 or decksUsedToday == 2 or decksUsedToday == 3:
                        miembrosSinJugar.append(lista)
                    else:
                        miembrosJugando.append(lista)

                    numero += 1
                except:
                    break

            if len(miembrosSinJugar) == 0:
                respuestaF = '\nTodos han jugado hoy.'
            else:
                respuestaF = '\nAtaques que faltan:\n'
                miembrosSinJugar.sort(key=lambda x: (-x[2], -x[3]), reverse=True)

                for x in miembrosSinJugar:
                    for i in todosLosMiembros:
                        if x[0] == i:
                            respuestaF += x[1] + ' mazos usados hoy: ' + str(x[2]) + ', mazos usados: ' + str(x[3]) + ', puntos: ' + x[4] + '\n'

            respuesta = nameClan + ' en guerra:' + respuestaF

            return respuesta
    except Exception as e:
        print(e)
        return 'Sin clan'
