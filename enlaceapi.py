import json
import requests
from data import *

def enlace(usuario,peticion):
    if peticion == 'info':
        usuarioInfo = requests.get('https://api.clashroyale.com/v1/players/%23' + str(usuario), headers=headers)
        usuarioInfoJson = usuarioInfo.json()

        return usuarioInfoJson
    elif peticion == 'cofres':
        usuarioCofres = requests.get('https://api.clashroyale.com/v1/players/%23' + str(usuario) + '/upcomingchests', headers=headers)
        usuarioCofresJson = usuarioCofres.json()

        return usuarioCofresJson
    elif peticion == 'clanWar': # OFF
        usuarioClan = requests.get('https://api.clashroyale.com/v1/clans/%23' + str(usuario) + '/currentwar', headers=headers)
        usuarioClanJson = usuarioClan.json()

        return usuarioClanJson
    elif peticion == 'currentRiverRace':
        usuarioClan = requests.get('https://api.clashroyale.com/v1/clans/%23' + str(usuario) + '/currentriverrace', headers=headers)
        usuarioClanJson = usuarioClan.json()

        return usuarioClanJson
    elif peticion == 'riverRaceLog':
        usuarioClan = requests.get('https://api.clashroyale.com/v1/clans/%23' + str(usuario) + '/riverracelog', headers=headers)
        usuarioClanJson = usuarioClan.json()

        return usuarioClanJson
    elif peticion == 'clanWarLog':
        usuarioClan = requests.get('https://api.clashroyale.com/v1/clans/%23' + str(usuario) + '/warlog', headers=headers)
        usuarioClanJson = usuarioClan.json()

        return usuarioClanJson
    elif peticion == 'clan':
        usuarioClan = requests.get('https://api.clashroyale.com/v1/clans/%23' + str(usuario) + '/members', headers=headers)
        usuarioClanJson = usuarioClan.json()

        return usuarioClanJson
    elif peticion == 'clanMiembros':
        usuarioClan = requests.get('https://api.clashroyale.com/v1/clans/%23' + str(usuario), headers=headers)
        usuarioClanJson = usuarioClan.json()

        return usuarioClanJson