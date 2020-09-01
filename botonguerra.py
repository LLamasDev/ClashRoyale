from db import *

def guerra(chatId):
    usuario = sacarTag(chatId)

    if usuario != 'None':
        try:
            usuarioInfoJson = enlace(usuario,'info')
            clan = str(usuarioInfoJson['clan']['tag'])
            clan = clan.replace('#', '', 1)
            usuarioClanJson = enlace(clan,'currentRiverRace')
            tamano = len(usuarioClanJson)

            if tamano == 1:
                return 'No en guerra'
            else:
                respuesta = 'Beta, no muestra a tiempo real la información de los puntos por ahora.\n'
                numero = 0
                listaFinal = []

                while True:
                    try:
                        fameT = 0
                        repairPointsT = 0

                        name = str(usuarioClanJson['clans'][numero]['name'])
                        badgeId = str(usuarioClanJson['clans'][numero]['badgeId'])
                        fame = usuarioClanJson['clans'][numero]['fame']
                        repairPoints = usuarioClanJson['clans'][numero]['repairPoints']
                        
                        fameT += fame
                        repairPointsT += repairPoints

                        lista = [name,badgeId,fame,repairPoints]

                        listaFinal.append(lista)
                        
                        numero += 1
                    except:
                        break

                listaFinal.sort(key=lambda x: (-x[2], -x[3]))
                
                numeros = 1
                
                for clanGuerra in listaFinal:
                    respuesta += str(numeros) + ' - Nombre: ' + str(clanGuerra[0]) + '\nPuntuación del clan: ' + str(clanGuerra[1]) + '\nPuntos: ' + str(clanGuerra[2]) + '\nPuntos de reparación: ' + str(clanGuerra[3]) + '\n\n'

                    numeros += 1

                return respuesta
        except:
            return 'Sin clan'
    else:
        return 'Usuario no registrado.\nTiene que introducir tu tag en el comando, ejemplo:\n/registro 2Y0J28QY'