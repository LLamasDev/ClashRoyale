from db import *

def clan(chatId):
    usuario = sacarTag(chatId)

    if usuario != 'None':
        try:
            usuarioInfoJson = enlace(usuario,'info')
            clan = str(usuarioInfoJson['clan']['tag'])
            clan = clan.replace('#', '', 1)
            clanUsu = str(usuarioInfoJson['clan']['name'])
            usuarioClanJson = enlace(clan,'clan')
            respuesta = 'Miembros de ' + clanUsu + '#' + clan + ':'
            numero = 0

            while True:
                try:
                    name = str(usuarioClanJson['items'][numero]['name'])
                    tag = str(usuarioClanJson['items'][numero]['tag'])
                    tag = tag.replace('#', '', 1)
                    posibleNombre = sacarUsuarioConTag(tag)

                    if posibleNombre != None:
                        name += ' (@' + posibleNombre + ')'

                    trophies = str(usuarioClanJson['items'][numero]['trophies'])

                    respuesta += '\n ' + trophies + ' - ' + name
                    numero += 1
                except:
                    break
                
            return respuesta
        except:
            return 'Sin clan'
    else:
        return 'Usuario no registrado.\nTiene que introducir tu tag en el comando, ejemplo:\n/registro 2Y0J28QY'