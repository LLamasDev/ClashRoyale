from db import *

def donaciones(chatId):
    usuario = sacarTag(chatId)

    if usuario != 'None':
        try:
            usuarioInfoJson = enlace(usuario,'info')
            clan = str(usuarioInfoJson['clan']['tag'])
            clan = clan.replace('#', '', 1)
            clanUsu = str(usuarioInfoJson['clan']['name'])
            usuarioClanJson = enlace(clan,'clan')
            respuesta = 'Donaciones en ' + clanUsu + ':'
            listaFinal = []
            numero = 0

            while True:
                try:
                    name = str(usuarioClanJson['items'][numero]['name'])
                    tag = str(usuarioClanJson['items'][numero]['tag'])
                    tag = tag.replace('#', '', 1)
                    posibleNombre = sacarUsuarioConTag(tag)

                    if posibleNombre != None:
                        name += ' (@' + posibleNombre + ')'

                    donations = usuarioClanJson['items'][numero]['donations']
                    donationsReceived = usuarioClanJson['items'][numero]['donationsReceived']

                    lista = [name,donations,donationsReceived]
                    listaFinal.append(lista)
                    numero += 1
                except:
                    break
            
            listaFinal.sort(key=lambda x: (-x[1], -x[2]))
            
            for miembro in listaFinal:
                respuesta += '\n' + str(miembro[0]) + ' ha donado ' + str(miembro[1]) + ' y le han donado ' + str(miembro[2]) + '.'

            return respuesta
        except:
            return 'Sin clan'
    else:
        return 'Usuario no registrado.\nTiene que introducir tu tag en el comando, ejemplo:\n/registro 2Y0J28QY'