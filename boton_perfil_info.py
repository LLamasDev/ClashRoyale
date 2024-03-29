from db import *

def perfil(chatId):
    usuario = sacarTag(chatId)

    if usuario != 'None':
        try:
            usuarioInfoJson = enlace(usuario,'info')
            nombre = str(usuarioInfoJson['name'])
            nivel = str(usuarioInfoJson['expLevel'])
            arena = str(usuarioInfoJson['arena']['name'])
            wins = str(usuarioInfoJson['wins'])
            losses = str(usuarioInfoJson['losses'])
            threeCrownWins = str(usuarioInfoJson['threeCrownWins'])
            warDayWins = str(usuarioInfoJson['warDayWins'])
            challengeMaxWins = str(usuarioInfoJson['challengeMaxWins'])
            totalDonations = str(usuarioInfoJson['totalDonations'])

            try:
                clan = str(usuarioInfoJson['clan']['name'])
                tag = str(usuarioInfoJson['clan']['tag'])
                role = str(usuarioInfoJson['role'])

                if role == 'member':
                    role = 'Miembro'
                elif role == 'elder':
                    role = 'Veterano'
                elif role == 'coLeader':
                    role = 'Colíder'
                elif role == 'leader':
                    role = 'Líder'

                clan = role + ' en ' + clan + tag
            except:
                clan = 'Sin clan'

            try:
                currentSeasonT = str(usuarioInfoJson['leagueStatistics']['currentSeason']['trophies'])
                currentSeasonBT = str(usuarioInfoJson['leagueStatistics']['currentSeason']['bestTrophies'])
            except:
                currentSeasonT = 'No ha jugado esta temporada.'
                currentSeasonBT = 'No ha jugado esta temporada.'
            try:
                previousSeasonID = str(usuarioInfoJson['leagueStatistics']['previousSeason']['id'])
                previousSeasonT = str(usuarioInfoJson['leagueStatistics']['previousSeason']['trophies'])
                previousSeasonBT = str(usuarioInfoJson['leagueStatistics']['previousSeason']['bestTrophies'])
            except:
                previousSeasonID = 'pasada'
                previousSeasonT = 'No ha jugado la temporada anterior.'
                previousSeasonBT = 'No ha jugado la temporada anterior.'

            try:
                bestSeasonID = str(usuarioInfoJson['leagueStatistics']['bestSeason']['id'])
                bestSeasonT = str(usuarioInfoJson['leagueStatistics']['bestSeason']['trophies'])
            except:
                bestSeasonID = ''
                bestSeasonT = 'Primera temporada.'

            respuesta = 'Nombre: ' + nombre + ', nivel ' + nivel + '.\nArena: ' + arena + '\nVictorias totales: ' + wins + '\nDerrotas totales: ' + losses + '\nTres coronas totales: ' + threeCrownWins + '\nVictorias en guerras: ' + warDayWins + '\nRécord en victorias en desafíos: ' + challengeMaxWins + '\n' + clan + '\nDonaciones totales: ' + totalDonations + '\n\nTrofeos:\n\t\t+ Temporada actual:\n\t\t\t\t- Trofeos: ' + currentSeasonT + '\n\t\t\t\t- Récord de trofeos: ' + currentSeasonBT + '\n\t\t+ Temporada ' + previousSeasonID + ' (última temporada jugada):\n\t\t\t\t- Trofeos: ' + previousSeasonT + '\n\t\t\t\t- Récord de trofeos: ' + previousSeasonBT + '\n\t\t+ Mejor temporada (' + bestSeasonID + '):\n\t\t\t\t- Récord de trofeos: ' + bestSeasonT

            return respuesta
        except:
            return 'API caída'
    else:
        return 'Usuario no registrado.\nTiene que introducir tu tag en el comando, ejemplo:\n/registro 2Y0J28QY'
