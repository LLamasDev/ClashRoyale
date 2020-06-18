#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import requests
import urllib.request
import json
import pymysql
from datetime import date
from googletrans import Translator
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

headers = {
    'authorization': 'Bearer KEY',
    'Accept': 'application/json'
}

def main():
    updater = Updater('TOKEN', use_context=True)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('register', register, pass_args=True))
    updater.dispatcher.add_handler(CallbackQueryHandler(boton))
    updater.start_polling()
    updater.idle()

def conexionBDD():
    try:
        con = pymysql.connect('SERVER', 'USER', 'PASSWORD', 'DATA BASE')
    except pymysql.err.OperationalError:
        print('No hay conexión a la base de datos')
        exit()

    return con,con.cursor()

def buscarContacto(chatId):
    con,cursor = conexionBDD()
    cursor.execute('SELECT count(*) FROM usuario WHERE id = %s', chatId)
    contador = cursor.fetchone()[0]
    cursor.close()

    return contador

def sacarTag(chatId):
    con,cursor = conexionBDD()
    cursor.execute('SELECT tag FROM usuario WHERE id = %s', chatId)
    respuesta = cursor.fetchall()[0][0]
    cursor.close()

    return respuesta

def sacarAlias(chatId,alias):
    con,cursor = conexionBDD()
    cursor.execute('SELECT alias FROM usuario WHERE id = %s', chatId)
    respuesta = cursor.fetchall()[0][0]
    con.close()

    if alias != respuesta:
        cambioAlias(chatId,alias)

def saberIdioma(chatId):
    con,cursor = conexionBDD()
    cursor.execute('SELECT idioma FROM usuario WHERE id = %s', chatId)
    respuesta = cursor.fetchall()[0][0]
    cursor.close()

    return respuesta

def altaContactos(chatId,alias):
    con,cursor = conexionBDD()
    cursor.execute('INSERT INTO usuario (id,alias) VALUES (%s, %s)', (chatId,alias))
    con.commit()
    con.close()

def cambioAlias(chatId,alias):
    con,cursor = conexionBDD()
    cursor.execute('UPDATE usuario SET alias = %s WHERE id = %s', (alias,chatId))
    con.commit()
    con.close()

def traducir(chatId,texto):
    idioma = saberIdioma(chatId)
    translator = Translator()
    respuesta = translator.translate(texto, src='es', dest=idioma)

    return respuesta

def boton(update,context):
    query = update.callback_query
    bot = context.bot
    chatId = query.message.chat_id

    if query.data == 'perfil':
        texto = traducir(chatId,perfil(chatId))
        bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=texto.text, reply_markup=botones(chatId))
    elif query.data == 'cofres':
        texto = traducir(chatId,cofres(chatId))
        bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=texto.text, reply_markup=botones(chatId))
    elif query.data == 'cartas':
        texto = traducir(chatId,cartas(chatId))
        bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=texto.text, reply_markup=botones(chatId))
    elif query.data == 'guerras':
        texto = traducir(chatId,guerras(chatId))
        bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=texto.text, reply_markup=botones(chatId))
    elif query.data == 'ataca':
        texto = traducir(chatId,ataca(chatId))
        bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=texto.text, reply_markup=botones(chatId))
    elif query.data == 'guerra':
        texto = traducir(chatId,guerra(chatId))
        bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=texto.text, reply_markup=botones(chatId))
    elif query.data == 'inactivos':
        texto = traducir(chatId,inactivos(chatId))
        bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=texto.text, reply_markup=botones(chatId))
    elif query.data == 'clan':
        texto = traducir(chatId,clan(chatId))
        bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text='\t 🏆 \t ' + texto.text, reply_markup=botones(chatId))

def botones(chatId):
    idioma = saberIdioma(chatId)

    if idioma == 'es':
        keyboard = [[InlineKeyboardButton('Información del perfil', callback_data='perfil'), InlineKeyboardButton('Siguientes cofres', callback_data='cofres')], [InlineKeyboardButton('Oro para las cartas', callback_data='cartas'), InlineKeyboardButton('Actividad en guerras', callback_data='guerras')], [InlineKeyboardButton('Sin atacar en guerra', callback_data='ataca'), InlineKeyboardButton('Ranking en la guerra', callback_data='guerra')], [InlineKeyboardButton('Inactivos del clan', callback_data='inactivos'), InlineKeyboardButton('Miembros del clan', callback_data='clan')]]
    elif idioma == 'en':
        keyboard = [[InlineKeyboardButton('Profile info', callback_data='perfil'), InlineKeyboardButton('Next chests', callback_data='cofres')], [InlineKeyboardButton('Gold for card', callback_data='cartas'), InlineKeyboardButton('Activity in wars', callback_data='guerras')], [InlineKeyboardButton('Hasn\'t attacked in war', callback_data='ataca'), InlineKeyboardButton('Ranking in the war', callback_data='guerra')], [InlineKeyboardButton('Inactive in the clan', callback_data='inactivos'), InlineKeyboardButton('Clan members', callback_data='clan')]]

    return InlineKeyboardMarkup(keyboard)

def start(update, context):
    tipo = update.message.chat.type
    chatId = update.message.from_user.id

    if tipo == 'private':
        alias = update.message.from_user.username
        nuevoUsu = buscarContacto(chatId)

        if nuevoUsu == 0:
            altaContactos(chatId,alias)
        else:
            sacarAlias(chatId,alias)

        textoI = traducir(chatId,'Elige una opción:')
        update.message.reply_text(textoI.text, reply_markup=botones(chatId))
    else:
        texto0I = traducir(chatId,'Privado')
        texto1I = traducir(chatId,'El funcionamiento del bot es por privado')
        keyboard = [[InlineKeyboardButton(texto0I.text + ' 🤖', url = 't.me/ClashRoyaleAPIBot')]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text(texto1I.text, reply_markup=reply_markup)

def register(update, context):
    tipo = update.message.chat.type
    chatId = update.message.from_user.id
    
    if tipo == 'private':
        usuDice = ' '.join(context.args)
        con,cursor = conexionBDD()

        try:
            primeraLetra = usuDice[0]

            if primeraLetra == '#':
                usuDice = usuDice.replace('#', '', 1)

            usuarioInfoJson = enlace(usuDice,'info')
            nombre = str(usuarioInfoJson['name'])
            sql = 'UPDATE usuario SET tag = %s WHERE id = %s'
            datos = (usuDice,chatId)
            cursor.execute(sql, datos)
            con.commit()
            con.close()

            textoI = traducir(chatId,'Registrado con el nombre de usuario: ')
            update.message.reply_text(textoI.text + nombre + ' #' + usuDice)
        except:
            textoI = traducir(chatId,'Usuario no encontrado.\nTiene que introducir tu tag en el comando, ejemplo:')
            update.message.reply_text(textoI.text + '\n/register 2Y0J28QY')
    else:
        texto0I = traducir(chatId,'Privado')
        texto1I = traducir(chatId,'El funcionamiento del bot es por privado')
        keyboard = [[InlineKeyboardButton(texto0I.text + ' 🤖', url = 't.me/ClashRoyaleAPIBot')]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text(texto1I.text, reply_markup=reply_markup)

def es(update, context):
    tipo = update.message.chat.type
    
    if tipo == 'private':
        try:
            chatId = update.message.from_user.id
            con,cursor = conexionBDD()
            cursor.execute('UPDATE usuario SET idioma = "es" WHERE id = %s', chatId)
            con.commit()
            con.close()

            update.message.reply_text('Idioma cambiado a español.')
        except:
            update.message.reply_text('Usuario no encontrado.\nTiene que introducir tu tag en el comando, ejemplo:\n/register 2Y0J28QY')
    else:
        keyboard = [[InlineKeyboardButton('Privado 🤖', url = 't.me/ClashRoyaleAPIBot')]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text('El funcionamiento del bot es por privado', reply_markup=reply_markup)

def en(update, context):
    tipo = update.message.chat.type
    
    if tipo == 'private':
        try:
            chatId = update.message.from_user.id
            con,cursor = conexionBDD()
            cursor.execute('UPDATE usuario SET idioma = "en" WHERE id = %s', chatId)
            con.commit()
            con.close()

            update.message.reply_text('(BETA) Language changed to English.\nThe following translation is not exact, it is automatic and contains errors.')
        except:
            update.message.reply_text('User not found.\nYou have to enter your tag in the command, example:\n/register 2Y0J28QY')
    else:
        keyboard = [[InlineKeyboardButton('Private 🤖', url = 't.me/ClashRoyaleAPIBot')]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text('The operation of the bot is by private', reply_markup=reply_markup)

def enlace(usuario,peticion):
    if peticion == 'info':
        usuarioInfo = requests.get('https://api.clashroyale.com/v1/players/%23' + str(usuario), headers=headers)
        usuarioInfoJson = usuarioInfo.json()

        return usuarioInfoJson
    elif peticion == 'cofres':
        usuarioCofres = requests.get('https://api.clashroyale.com/v1/players/%23' + str(usuario) + '/upcomingchests', headers=headers)
        usuarioCofresJson = usuarioCofres.json()

        return usuarioCofresJson
    elif peticion == 'clanWar':
        usuarioClan = requests.get('https://api.clashroyale.com/v1/clans/%23' + str(usuario) + '/currentwar', headers=headers)
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
        return 'Usuario no registrado.\nTiene que introducir tu tag en el comando, ejemplo:\n/register 2Y0J28QY'

def cofres(chatId):
    usuario = sacarTag(chatId)

    if usuario != 'None':
        try:
            usuarioCofresJson = enlace(usuario,'cofres')
            idioma = saberIdioma(chatId)
            respuesta = 'Siguientes cofres:'
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

            for numeros,cofre in diccionario.items():
                if cofre[1] == 'Silver Chest':
                    if idioma == 'es':
                        respuesta += '\n' + str(cofre[0]) + ' para un cofre de plata.'
                    elif idioma == 'en':
                        respuesta += '\n' + str(cofre[0]) + ' for a silver chest.'
                elif cofre[1] == 'Golden Chest':
                    if idioma == 'es':
                        respuesta += '\n' + str(cofre[0]) + ' para un cofre de oro.'
                    elif idioma == 'en':
                        respuesta += '\n' + str(cofre[0]) + ' for a golden Chest.'
                elif cofre[1] == 'Giant Chest':
                    if idioma == 'es':
                        respuesta += '\n' + str(cofre[0]) + ' para un cofre gigante.'
                    elif idioma == 'en':
                        respuesta += '\n' + str(cofre[0]) + ' for a giant chest.'
                elif cofre[1] == 'Epic Chest':
                    if idioma == 'es':
                        respuesta += '\n' + str(cofre[0]) + ' para un cofre épico.'
                    elif idioma == 'en':
                        respuesta += '\n' + str(cofre[0]) + ' for an epic chest.'
                elif cofre[1] == 'Magical Chest':
                    if idioma == 'es':
                        respuesta += '\n' + str(cofre[0]) + ' para un cofre mágico.'
                    elif idioma == 'en':
                        respuesta += '\n' + str(cofre[0]) + ' for a magical chest.'
                elif cofre[1] == 'Legendary Chest':
                    if idioma == 'es':
                        respuesta += '\n' + str(cofre[0]) + ' para un cofre legendario.'
                    elif idioma == 'en':
                        respuesta += '\n' + str(cofre[0]) + ' for a legendary chest.'
                elif cofre[1] == 'Mega Lightning Chest':
                    if idioma == 'es':
                        respuesta += '\n' + str(cofre[0]) + ' para un cofre megarelámpago.'
                    elif idioma == 'en':
                        respuesta += '\n' + str(cofre[0]) + ' for a mega lightning chest.'

            return respuesta
        except:
            return 'API caída'
    else:
        return 'Usuario no registrado.\nTiene que introducir tu tag en el comando, ejemplo:\n/register 2Y0J28QY'

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
            respuesta = 'Oro necesario para subir al máximo.\nTe faltan ' + str(comunContador) + ' niveles de cartas comunes: ' + str(comunOro) + ' de oro.\nTe faltan ' + str(especialContador) + ' niveles de cartas especiales: ' + str(especialOro) + ' de oro.\nTe faltan ' + str(epicaContador) + ' niveles de cartas épicas: ' + str(epicaOro) + ' de oro.\nTe faltan ' + str(legendariaContador) + ' niveles de cartas legendarias: ' + str(legendariaOro) + ' de oro.\nTe faltan ' + str(cartasContador) + ' niveles en total: ' + str(oro) + ' de oro.'

            return respuesta
        except:
            return 'API caída'
    else:
        return 'Usuario no registrado.\nTiene que introducir tu tag en el comando, ejemplo:\n/register 2Y0J28QY'

def guerras(chatId):
    usuario = sacarTag(chatId)

    if usuario != 'None':
        try:
            usuarioInfoJson = enlace(usuario,'info')
            clan = str(usuarioInfoJson['clan']['tag'])
            clan = clan.replace('#', '', 1)
            clanUsu = str(usuarioInfoJson['clan']['name'])
            usuarioClanJson = enlace(clan,'clanWarLog')

            respuesta = 'El orden sería por victorias y en caso de empate se ordena por participaciones.\nParticipación en las últimas 10 guerras de ' + clanUsu + ':'
            listaParticipantes = []
            listaFin = []
            numero0 = 0

            while numero0 < 10:
                try:
                    numero1 = 0

                    while True:
                        try:
                            name = str(usuarioClanJson['items'][numero0]['participants'][numero1]['name'])
                            numberOfBattles = str(usuarioClanJson['items'][numero0]['participants'][numero1]['numberOfBattles'])
                            battlesPlayed = str(usuarioClanJson['items'][numero0]['participants'][numero1]['battlesPlayed'])
                            wins = str(usuarioClanJson['items'][numero0]['participants'][numero1]['wins'])
                            collectionDayBattlesPlayed = str(usuarioClanJson['items'][numero0]['participants'][numero1]['collectionDayBattlesPlayed'])

                            lista = [name,numberOfBattles,battlesPlayed,wins,collectionDayBattlesPlayed]
                            listaFin.append(lista)
                            numero1 += 1
                        except:
                            break

                    numero0 += 1
                except:
                    break
            
            name = ''
            numberOfBattles = 0
            battlesPlayed = 0
            wins = 0
            collectionDayBattlesPlayed = 0
            contiene = False

            for x in listaFin:
                for i in listaParticipantes:
                    if x[0] == i[0]:
                        contiene = True

                if contiene == False:
                    lista = [x[0],numberOfBattles,battlesPlayed,wins,collectionDayBattlesPlayed]
                    listaParticipantes.append(lista)

            for x in listaFin:
                for i in listaParticipantes:
                    if x[0] == i[0]:
                        i[1] += int(x[1])
                        i[2] += int(x[2])
                        i[3] += int(x[3])
                        i[4] += int(x[4])

            listaParticipantes.sort(key=lambda x: (-x[3], -x[1]))
            numero2 = 1
            
            for miembro in listaParticipantes:
                respuesta += '\n' + str(numero2) + ' - ' + str(miembro[0]) + ' ha participado en ' + str(miembro[1]) + ', ha jugado ' + str(miembro[2]) + ', ha ganado ' + str(miembro[3]) + ', partidas de recolección ' + str(miembro[4]) + '.'
                numero2 += 1

            return respuesta
        except:
            return 'Sin clan'
    else:
        return 'Usuario no registrado.\nTiene que introducir tu tag en el comando, ejemplo:\n/register 2Y0J28QY'

def ataca(chatId):
    usuario = sacarTag(chatId)

    if usuario != 'None':
        try:
            usuarioInfoJson = enlace(usuario,'info')
            clan = str(usuarioInfoJson['clan']['tag'])
            clan = clan.replace('#', '', 1)
            nameClan = str(usuarioInfoJson['clan']['name'])
            usuarioAtacaJson = enlace(clan,'clanWar')
            state = str(usuarioAtacaJson['state'])

            if state != 'notInWar':
                try:
                    diccionario = {}
                    numero = 0

                    if state == 'collectionDay':
                        state = 'día de recolección'
                    elif state == 'warDay':
                        state = 'guerra'

                    respuesta = nameClan + ' en ' + state + '.\nAtaques que faltan:'

                    while True:
                        try:
                            numberOfBattles = int(usuarioAtacaJson['participants'][numero]['numberOfBattles'])
                            battlesPlayed = int(usuarioAtacaJson['participants'][numero]['battlesPlayed'])

                            resultado = numberOfBattles - battlesPlayed

                            if resultado > 0:
                                name = str(usuarioAtacaJson['participants'][numero]['name'])

                                diccionario[name] = resultado

                            numero += 1
                        except:
                            break

                    for nombre,falta in diccionario.items():
                        respuesta += '\n' + nombre + ' le faltan ' + str(falta)

                    return respuesta
                except:
                    return 'API caída'
            else:
                return 'No en guerra'
        except:
            return 'Sin clan'
    else:
        return 'Usuario no registrado.\nTiene que introducir tu tag en el comando, ejemplo:\n/register 2Y0J28QY'

def guerra(chatId):
    usuario = sacarTag(chatId)

    if usuario != 'None':
        try:
            usuarioInfoJson = enlace(usuario,'info')
            clan = str(usuarioInfoJson['clan']['tag'])
            clan = clan.replace('#', '', 1)
            usuarioClanJson = enlace(clan,'clanWar')
            state = str(usuarioClanJson['state'])

            if state == 'notInWar':
                return 'No en guerra'
            else:
                name = str(usuarioClanJson['clan']['name'])
                clanScore = str(usuarioClanJson['clan']['clanScore'])
                participants = str(usuarioClanJson['clan']['participants'])
                battlesPlayed = str(usuarioClanJson['clan']['battlesPlayed'])
                wins = str(usuarioClanJson['clan']['wins'])
                crowns = str(usuarioClanJson['clan']['crowns'])

                if state == 'collectionDay':
                    state = 'día de recolección'
                elif state == 'warDay':
                    state = 'guerra'

                respuesta = name + ' en ' + state + '.'

                if state == 'guerra':
                    listaFinal = []
                    numero = 0

                    while True:
                        try:
                            otroNombre = str(usuarioClanJson['clans'][numero]['name'])
                            otroClanScore = str(usuarioClanJson['clans'][numero]['clanScore'])
                            otroWins = int(usuarioClanJson['clans'][numero]['wins'])
                            otroCrowns = int(usuarioClanJson['clans'][numero]['crowns'])
                            otroParticipants = str(usuarioClanJson['clans'][numero]['participants'])
                            otroBattlesPlayed = str(usuarioClanJson['clans'][numero]['battlesPlayed'])

                            lista = [otroNombre,otroClanScore,otroWins,otroCrowns,otroParticipants,otroBattlesPlayed]
                            listaFinal.append(lista)
                            numero += 1
                        except:
                            break

                    listaFinal.sort(key=lambda x: (-x[2], -x[3]))

                    numeros = 1
                    for clanGuerra in listaFinal:
                        respuesta += '\n\n' + str(numeros) + ' - ' + clanGuerra[0] + '\nPuntuación: ' + clanGuerra[1] + '\nVictorias: ' + str(clanGuerra[2]) + '\nCoronas: ' + str(clanGuerra[3]) + '\nParticipantes: ' + clanGuerra[4] + '\nBatallas jugadas: ' + clanGuerra[5]

                        numeros += 1
                    return respuesta
                else:
                    respuesta += '\nPuntuación del clan: ' + clanScore + '\nParticipantes: ' + participants + '\nBatallas jugadas: ' + battlesPlayed + '\nVictorias: ' + wins + '\nCoronas: ' + crowns
                    
                    return respuesta
        except:
            return 'Sin clan'
    else:
        return 'Usuario no registrado.\nTiene que introducir tu tag en el comando, ejemplo:\n/register 2Y0J28QY'

def inactivos(chatId):
    usuario = sacarTag(chatId)

    if usuario != 'None':
        try:
            usuarioInfoJson = enlace(usuario,'info')
            clan = str(usuarioInfoJson['clan']['tag'])
            clan = clan.replace('#', '', 1)
            clanUsu = str(usuarioInfoJson['clan']['name'])
            usuarioClanJson = enlace(clan,'clan')
            respuesta = 'Inactivos (más de 7 días) en ' + clanUsu + ':'
            numero = 0

            while True:
                try:
                    name = str(usuarioClanJson['items'][numero]['name'])
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

            return respuesta
        except:
            return 'Sin clan'
    else:
        return 'Usuario no registrado.\nTiene que introducir tu tag en el comando, ejemplo:\n/register 2Y0J28QY'

def clan(chatId):
    usuario = sacarTag(chatId)

    if usuario != 'None':
        try:
            usuarioInfoJson = enlace(usuario,'info')
            clan = str(usuarioInfoJson['clan']['tag'])
            clan = clan.replace('#', '', 1)
            clanUsu = str(usuarioInfoJson['clan']['name'])
            usuarioClanJson = enlace(clan,'clan')

            respuesta = '- Miembros de ' + clanUsu + ':'
            numero = 0

            while True:
                try:
                    name = str(usuarioClanJson['items'][numero]['name'])
                    trophies = str(usuarioClanJson['items'][numero]['trophies'])

                    respuesta += '\n' + trophies + ' - ' + name
                    numero += 1
                except:
                    break

            return respuesta
        except:
            return 'Sin clan'
    else:
        return 'Usuario no registrado.\nTiene que introducir tu tag en el comando, ejemplo:\n/register 2Y0J28QY'

if __name__ == '__main__':
    main()