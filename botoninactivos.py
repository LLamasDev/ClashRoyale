from datetime import date
from db import *

def inactivos(chatId):
    usuario = sacarTag(chatId)

    if usuario != 'None':
        try:
            usuarioInfoJson = enlace(usuario,'info')
            clan = str(usuarioInfoJson['clan']['tag'])
            clan = clan.replace('#', '', 1)
            clanUsu = str(usuarioInfoJson['clan']['name'])
            usuarioClanJson = enlace(clan,'clan')
            respuesta = 'Inactivos (más de 7 días) en ' + clanUsu + '#' + clan + ':'
            numero = 0

            while True:
                try:
                    name = str(usuarioClanJson['items'][numero]['name'])
                    tag = str(usuarioClanJson['items'][numero]['tag'])
                    tag = tag.replace('#', '', 1)
                    posibleNombre = sacarUsuarioConTag(tag)

                    if posibleNombre != None:
                        name += ' (@' + posibleNombre + ')'

                    lastSeen = str(usuarioClanJson['items'][numero]['lastSeen'])

                    fecha = lastSeen.split('T')[0]
                    ano = fecha[0:4]
                    mes = fecha[4:6]
                    dia = fecha[6:8]

                    if mes[0] == '0':
                        mes = mes.replace('0', '', 1)

                    if dia[0] == '0':
                        dia = dia.replace('0', '', 1)

                    afk = date.today() - date(int(ano), int(mes), int(dia))

                    if str(afk) == '0:00:00':
                        afk = '0 d'

                    afk = str(afk).split(' ')[0]

                    if int(afk) > 7:
                        afk = afk.split(' ')[0]
                        respuesta += '\n' + name + ' no juega desde hace ' + str(afk) + ' días.'

                    numero += 1
                except:
                    break
                
            if len(respuesta) == 44:
                respuesta = 'Sin inactivos (más de 7 días) en ' + clanUsu + '.'

                return respuesta
            else:
                return respuesta
        except:
            return 'Sin clan'
    else:
        return 'Usuario no registrado.\nTiene que introducir tu tag en el comando, ejemplo:\n/registro 2Y0J28QY'