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

                        fame = int(usuarioClanJson['items'][0]['standings'][participanteN]['clan']['participants'][numero]['fame'])
                        repairPoints = str(usuarioClanJson['items'][0]['standings'][participanteN]['clan']['participants'][numero]['repairPoints'])
                        decksUsed = int(usuarioClanJson['items'][0]['standings'][participanteN]['clan']['participants'][numero]['decksUsed'])

                        lista = [name,fame,decksUsed,repairPoints]
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
                    lista = [x[0],0,0,0]
                    listaParticipantes.append(lista)

            for x in listaFin:
                for i in listaParticipantes:
                    if x[0] == i[0]:
                        i[1] += int(x[1])
                        i[2] += int(x[2])
                        i[3] += int(x[3])

            listaParticipantes.sort(key=lambda x: (-x[1], -x[2]))
            numeroC = 1

            respuesta += str(participanteN) + ' guerras de ' + clanUsu + '#' + clan + ' (top 20 de ' + str(len(listaFin)) + ' participantes):'

            for miembro in listaParticipantes:
                if numeroC == 21:
                    break
                else:
                    respuesta += '\n' + str(numeroC) + ' - ' + str(miembro[0]) + ' ha ganado ' + str(miembro[1]) + ' puntos, ha usado ' + str(miembro[2]) + ' mazos y ' + str(miembro[3]) + ' puntos de reparación.'
                    numeroC += 1

            return respuesta
        except Exception as e:
            return 'Sin clan'
    else:
        return 'Usuario no registrado.\nTiene que introducir tu tag en el comando, ejemplo:\n/registro 2Y0J28QY'
