from db import *

def cartas(chatId):
    usuario = sacarTag(chatId)

    if usuario != 'None':
        try:
            usuarioInfoJson = enlace(usuario,'info')
            numero = 0
            oro = 0
            comunOro = 0
            comunContador = 0
            especialOro = 0
            especialContador = 0
            epicaOro = 0
            epicaContador = 0
            legendariaOro = 0
            legendariaContador = 0
            cartasContador = 0

            while True:
                try:
                    level = int(usuarioInfoJson['cards'][numero]['level'])
                    maxLevel = int(usuarioInfoJson['cards'][numero]['maxLevel'])

                    resultado = maxLevel - level
                    diccionario = {'comun': (5,20,50,150,400,1000,2000,4000,8000,20000,50000,100000), 'especial': (50,150,400,1000,2000,4000,8000,20000,50000,100000), 'epica': (400,2000,4000,8000,20000,50000,100000), 'legendaria': (5000,20000,50000,100000)}

                    if resultado > 0:
                        if maxLevel == 5:
                            for i in range(resultado, 0, -1):
                                oro += diccionario['legendaria'][-i]
                                legendariaOro += diccionario['legendaria'][-i]
                                legendariaContador += 1
                        elif maxLevel == 8:
                            for i in range(resultado, 0, -1):
                                oro += diccionario['epica'][-i]
                                epicaOro += diccionario['epica'][-i]
                                epicaContador += 1
                        elif maxLevel == 11:
                            for i in range(resultado, 0, -1):
                                oro += diccionario['especial'][-i]
                                especialOro += diccionario['especial'][-i]
                                especialContador += 1
                        elif maxLevel == 13:
                            for i in range(resultado, 0, -1):
                                oro += diccionario['comun'][-i]
                                comunOro += diccionario['comun'][-i]
                                comunContador += 1

                    numero += 1
                except:
                    break

            cartasContador = comunContador + especialContador + epicaContador + legendariaContador
            respuesta = 'Oro necesario para subir al máximo:\nTe faltan ' + str(comunContador) + ' niveles de cartas comunes: ' + str(comunOro) + ' de oro.\nTe faltan ' + str(especialContador) + ' niveles de cartas especiales: ' + str(especialOro) + ' de oro.\nTe faltan ' + str(epicaContador) + ' niveles de cartas épicas: ' + str(epicaOro) + ' de oro.\nTe faltan ' + str(legendariaContador) + ' niveles de cartas legendarias: ' + str(legendariaOro) + ' de oro.\nTe faltan ' + str(cartasContador) + ' niveles en total: ' + str(oro) + ' de oro.'

            return respuesta
        except:
            return 'API caída'
    else:
        return 'Usuario no registrado.\nTiene que introducir tu tag en el comando, ejemplo:\n/registro 2Y0J28QY'