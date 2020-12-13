from db import *

def guerras(chatId):
    usuario = sacarTag(chatId)

    if usuario != 'None':
        try:
            usuarioInfoJson = enlace(usuario,'info')
            clan = str(usuarioInfoJson['clan']['tag'])
            clan = clan.replace('#', '', 1)
            clanUsu = str(usuarioInfoJson['clan']['name'])
            usuarioClanJson = enlace(clan,'riverRaceLog')
            respuesta = 'Participación en las últimas '
            listaParticipantes = []
            listaFin = []
            participanteN = 0
            numero = 0

            while participanteN < 5:
                while True:
                    try:
                        name = str(usuarioClanJson['items'][0]['standings'][participanteN]['clan']['participants'][numero]['name'])
                        tag = str(usuarioClanJson['items'][0]['standings'][participanteN]['clan']['participants'][numero]['tag'])
                        tag = tag.replace('#', '', 1)
                        posibleNombre = sacarUsuarioConTag(tag)

                        if posibleNombre != None:
                            name += ' (@' + posibleNombre + ')'

                        fame = str(usuarioClanJson['items'][0]['standings'][participanteN]['clan']['participants'][numero]['fame'])
                        repairPoints = str(usuarioClanJson['items'][0]['standings'][participanteN]['clan']['participants'][numero]['repairPoints'])

                        if int(fame) > 0:
                            lista = [name,fame,repairPoints]
                            listaFin.append(lista)

                        numero += 1
                    except:
                        break

                participanteN += 1

            contiene = False

            for x in listaFin:
                for i in listaParticipantes:
                    if x[0] == i[0]:
                        contiene = True

                if contiene == False:
                    lista = [x[0],0,0]
                    listaParticipantes.append(lista)

            for x in listaFin:
                for i in listaParticipantes:
                    if x[0] == i[0]:
                        i[1] += int(x[1])
                        i[2] += int(x[2])

            listaParticipantes.sort(key=lambda x: (-x[1], -x[2]))
            numeroC = 1

            respuesta += str(participanteN) + ' guerras de ' + clanUsu + ' (top 50 de ' + str(len(listaFin)) + '):'
            
            for miembro in listaParticipantes:
                if numeroC == 51:
                    break
                else:
                    respuesta += '\n' + str(numeroC) + ' - ' + str(miembro[0]) + ' ha ganado ' + str(miembro[1]) + ' puntos y ' + str(miembro[2]) + ' puntos de reparación.'
                    numeroC += 1
                    
            return respuesta
        except Exception as e:
            return 'Sin clan'
    else:
        return 'Usuario no registrado.\nTiene que introducir tu tag en el comando, ejemplo:\n/registro 2Y0J28QY'