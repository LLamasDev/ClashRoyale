from db import *

def cofres(chatId):
    usuario = sacarTag(chatId)

    if usuario != 'None':
        try:
            usuarioCofresJson = enlace(usuario,'cofres')
            idioma = saberIdioma(chatId)
            diccionario = {}
            numero = 0

            while True:
                try:
                    cofreNumero = int(usuarioCofresJson['items'][numero]['index'] + 1)
                    cofre = str(usuarioCofresJson['items'][numero]['name'])

                    diccionario[numero] = cofreNumero, cofre
                    numero += 1
                except:
                    break

            if idioma == 'es':
                respuesta = 'Siguientes cofres:'
            else:
                respuesta = 'Next chests:'

            for numeros,cofre in diccionario.items():
                if cofre[1] == 'Silver Chest':
                    if idioma == 'es':
                        respuesta += '\n' + str(cofre[0]) + ' para un cofre de plata.'
                    else:
                        respuesta += '\n' + str(cofre[0]) + ' for a silver chest.'
                elif cofre[1] == 'Golden Chest':
                    if idioma == 'es':
                        respuesta += '\n' + str(cofre[0]) + ' para un cofre de oro.'
                    else:
                        respuesta += '\n' + str(cofre[0]) + ' for a golden Chest.'
                elif cofre[1] == 'Giant Chest':
                    if idioma == 'es':
                        respuesta += '\n' + str(cofre[0]) + ' para un cofre gigante.'
                    else:
                        respuesta += '\n' + str(cofre[0]) + ' for a giant chest.'
                elif cofre[1] == 'Epic Chest':
                    if idioma == 'es':
                        respuesta += '\n' + str(cofre[0]) + ' para un cofre épico.'
                    else:
                        respuesta += '\n' + str(cofre[0]) + ' for an epic chest.'
                elif cofre[1] == 'Magical Chest':
                    if idioma == 'es':
                        respuesta += '\n' + str(cofre[0]) + ' para un cofre mágico.'
                    else:
                        respuesta += '\n' + str(cofre[0]) + ' for a magical chest.'
                elif cofre[1] == 'Legendary Chest':
                    if idioma == 'es':
                        respuesta += '\n' + str(cofre[0]) + ' para un cofre legendario.'
                    else:
                        respuesta += '\n' + str(cofre[0]) + ' for a legendary chest.'
                elif cofre[1] == 'Mega Lightning Chest':
                    if idioma == 'es':
                        respuesta += '\n' + str(cofre[0]) + ' para un cofre megarelámpago.'
                    else:
                        respuesta += '\n' + str(cofre[0]) + ' for a mega lightning chest.'
                        
            return respuesta
        except:
            return 'API caída'
    else:
        return 'Usuario no registrado.\nTiene que introducir tu tag en el comando, ejemplo:\n/registro 2Y0J28QY'