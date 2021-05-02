import pymysql
from enlaceapi import *
from botonperfil import *

def clanInfo(chatId):
    usuario = sacarTag(chatId)

    if usuario != 'None':
        try:
            usuarioInfoJson = enlace(usuario,'info')
            clan = str(usuarioInfoJson['clan']['tag'])
            clan = clan.replace('#', '', 1)
            usuarioClanJson = enlace(clan, 'clanMiembros')

            name = str(usuarioClanJson['name'])
            description = str(usuarioClanJson['description'])
            clanScore = str(usuarioClanJson['clanScore'])
            clanWarTrophies = str(usuarioClanJson['clanWarTrophies'])
            location = str(usuarioClanJson['location']['name'])
            requiredTrophies = str(usuarioClanJson['requiredTrophies'])
            donationsPerWeek = str(usuarioClanJson['donationsPerWeek'])
            members = str(usuarioClanJson['members'])

            respuesta = 'Clan: ' + name + '#' + clan + '\nDescripción:\n' + description + '\nLocalización: ' + location + '\nMiembros: ' + members + '\nDonaciones por semana: ' + donationsPerWeek + '\nPuntuación del clan: ' + clanScore + '\nTrofeos del clan en guerra: ' + clanWarTrophies + '\nRequerimientos de trofeos para entrar al clan: ' + requiredTrophies

            return respuesta
        except:
            return 'Sin clan'
    else:
        return 'Usuario no registrado.\nTiene que introducir tu tag en el comando, ejemplo:\n/registro UJU9LGRU'