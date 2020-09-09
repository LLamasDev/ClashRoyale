from db import *

def guerras(chatId):
    usuario = sacarTag(chatId)

    if usuario != 'None':
        try:
            return 'Función sin desarrollar, esperando que pase las dos primeras guerras.'
        except:
            return 'Sin clan'
    else:
        return 'Usuario no registrado.\nTiene que introducir tu tag en el comando, ejemplo:\n/registro 2Y0J28QY'