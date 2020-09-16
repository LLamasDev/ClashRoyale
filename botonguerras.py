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
            numero0 = 0
            numero1 = 0

            while True:
                try:
                    clanName = str(usuarioClanJson['items'][numero0]['standings'][numero1]['clan']['name'])

                    if clanName == clanUsu:
                        numero2 = 0

                        while True:
                            try:
                                name = str(usuarioClanJson['items'][numero0]['standings'][numero1]['clan']['participants'][numero2]['name'])
                                tag = str(usuarioClanJson['items'][numero0]['standings'][numero1]['clan']['participants'][numero2]['tag'])
                                tag = tag.replace('#', '', 1)
                                posibleNombre = sacarUsuarioConTag(tag)

                                if posibleNombre != None:
                                    name += ' (@' + posibleNombre + ')'

                                fame = str(usuarioClanJson['items'][numero0]['standings'][numero1]['clan']['participants'][numero2]['fame'])
                                repairPoints = str(usuarioClanJson['items'][numero0]['standings'][numero1]['clan']['participants'][numero2]['repairPoints'])

                                lista = [name,fame,repairPoints]
                                listaFin.append(lista)
                                numero2 += 1
                            except:
                                break

                        numero0 += 1
                    else:
                        numero1 += 1
                except:
                    break

            fame = 0
            repairPoints = 0
            contiene = False

            for x in listaFin:
                for i in listaParticipantes:
                    if x[0] == i[0]:
                        contiene = True

                if contiene == False:
                    lista = [x[0],fame,repairPoints]
                    listaParticipantes.append(lista)

            for x in listaFin:
                for i in listaParticipantes:
                    if x[0] == i[0]:
                        i[1] += int(x[1])
                        i[2] += int(x[2])

            listaParticipantes.sort(key=lambda x: (-x[1], -x[2]))
            numeroC = 1

            respuesta += str(numero0) + ' guerras de ' + clanUsu + ':'
            
            for miembro in listaParticipantes:
                respuesta += '\n' + str(numeroC) + ' - ' + str(miembro[0]) + ' ha ganado ' + str(miembro[1]) + ' puntos y ' + str(miembro[2]) + ' puntos de reparación.'
                numeroC += 1
            
            return respuesta
        except:
            return 'Sin clan'
    else:
        return 'Usuario no registrado.\nTiene que introducir tu tag en el comando, ejemplo:\n/registro 2Y0J28QY'