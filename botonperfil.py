from db import *

def perfil(chatId):
    usuario = sacarTag(chatId)

    if usuario != 'None':
        try:
            usuarioInfoJson = enlace(usuario,'info')
            nombre = str(usuarioInfoJson['name'])
            arena = str(usuarioInfoJson['arena']['name'])
            warDayWins = str(usuarioInfoJson['warDayWins'])
            challengeMaxWins = str(usuarioInfoJson['challengeMaxWins'])

            try:
                clan = str(usuarioInfoJson['clan']['name'])
                role = str(usuarioInfoJson['role'])

                if role == 'member':
                    role = 'Miembro'
                elif role == 'coLeader':
                    role = 'Colíder'
                elif role == 'leader':
                    role = 'Líder'
                    
                clan = role + ' en ' + clan
            except:
                clan = 'Sin clan'

            try:
                currentSeasonT = str(usuarioInfoJson['leagueStatistics']['currentSeason']['trophies'])
                currentSeasonBT = str(usuarioInfoJson['leagueStatistics']['currentSeason']['bestTrophies'])
            except:
                currentSeasonT = 'No ha jugado esta temporada'
                currentSeasonBT = 'No ha jugado esta temporada'

            try:
                previousSeasonT = str(usuarioInfoJson['leagueStatistics']['previousSeason']['trophies'])
                previousSeasonBT = str(usuarioInfoJson['leagueStatistics']['previousSeason']['bestTrophies'])
            except:
                previousSeasonT = 'No ha jugado la temporada anterior'
                previousSeasonBT = 'No ha jugado la temporada anterior'
                
            try:
                bestSeasonT = str(usuarioInfoJson['leagueStatistics']['bestSeason']['trophies'])
            except:
                bestSeasonT = 'Primera temporada'

            donations = str(usuarioInfoJson['donations'])
            donationsReceived = str(usuarioInfoJson['donationsReceived'])
            respuesta = 'Nombre: ' + nombre + '\nArena: ' + arena + '\nVictorias en guerra de clanes: ' + warDayWins + '\nRécord en victorias en desafíos: ' + challengeMaxWins + '\n' + clan + '\nDonaciones realizadas: ' + donations + '\nDonaciones recibidas: ' + donationsReceived + '\n\nTrofeos:\n\t\t+ Temporada actual:\n\t\t\t\t- Trofeos: ' + currentSeasonT + '\n\t\t\t\t- Récord de trofeos: ' + currentSeasonBT + '\n\t\t+ Temporada pasada:\n\t\t\t\t- Trofeos: ' + previousSeasonT + '\n\t\t\t\t- Récord de trofeos: ' + previousSeasonBT + '\n\t\t+ Mejor temporada:\n\t\t\t\t- Récord de trofeos: ' + bestSeasonT
            
            return respuesta
        except:
            return 'API caída'
    else:
        return 'Usuario no registrado.\nTiene que introducir tu tag en el comando, ejemplo:\n/registro 2Y0J28QY'