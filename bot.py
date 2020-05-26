#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import requests
import urllib.request
import json
import pymysql
import unidecode
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

headers = {
    'authorization': 'Bearer KEY',
    'Accept': 'application/json'
}

def main():
    updater = Updater("TOKEN", use_context=True)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('register', register, pass_args=True))
    updater.dispatcher.add_handler(CallbackQueryHandler(boton))
    updater.start_polling()
    updater.idle()

def conexionBDD():
    try:
        con = pymysql.connect("localhost", "user", "password", "data base")
    except pymysql.err.OperationalError:
        print("No hay conexión a la base de datos")
        exit()

    return con,con.cursor()

def buscarContacto(chatId):
    con,cursor = conexionBDD()
    sql = "SELECT count(*) FROM usuario WHERE id = %s"
    datos = (chatId)
    cursor.execute(sql, datos)
    contador = cursor.fetchone()[0]
    cursor.close()

    return contador

def altaContactos(chatId,alias):
    con,cursor = conexionBDD()
    sql = "INSERT INTO usuario (id,alias) VALUES (%s, %s)"
    datos = (chatId,alias)
    cursor.execute(sql, datos)
    con.commit()
    con.close()

def register(update, context):
    tipo = update.message.chat.type
    
    if tipo == "private":
        chatId = update.message.from_user.id
        usuDice = " ".join(context.args)
        con,cursor = conexionBDD()

        try:
            primeraLetra = usuDice[0]

            if primeraLetra == "#":
                usuDice = usuDice.replace('#', '', 1)

            usuarioInfoJson = enlace(usuDice,"info")
            nombre = str(usuarioInfoJson['name'])
            sql = "UPDATE usuario SET tag = %s WHERE id = %s"
            datos = (usuDice,chatId)
            cursor.execute(sql, datos)
            con.commit()
            con.close()

            update.message.reply_text("Registrado con el nombre de usuario: " + nombre + " #" + usuDice)
        except:
            update.message.reply_text("Usuario no encontrado.\nTiene que introducir tu tag en el comando, ejemplo:\n/register 2Y0J28QY")
    else:
        keyboard = [[InlineKeyboardButton("Privado 🤖", url = 't.me/ClashRoyaleAPIBot')]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text("El funcionamiento del bot es por privado", reply_markup=reply_markup)

def sacarTag(chatId):
    con,cursor = conexionBDD()
    sql = "SELECT tag FROM usuario WHERE id = %s"
    datos = (chatId)
    cursor.execute(sql, datos)

    for tag in cursor:
        respuesta = tag[0]

    cursor.close()

    return respuesta

def boton(update, context):
    query = update.callback_query
    bot = context.bot
    chatId = query.message.chat_id

    if query.data == 'perfil':
        bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=perfil(chatId), reply_markup=botones())
    elif query.data == 'trofeos':
        bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=trofeos(chatId), reply_markup=botones())
    elif query.data == 'cofres':
        bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=cofres(chatId), reply_markup=botones())
    elif query.data == 'guerras':
        bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=clan(chatId), reply_markup=botones())

def botones():
    keyboard = [[InlineKeyboardButton("Perfil", callback_data='perfil'), InlineKeyboardButton("Trofeos", callback_data='trofeos')], [InlineKeyboardButton("Cofres", callback_data='cofres'), InlineKeyboardButton("Guerras", callback_data='guerras')]]
    
    return InlineKeyboardMarkup(keyboard)

def start(update, context):
    tipo = update.message.chat.type

    if tipo == "private":
        chatId = update.message.from_user.id
        alias = update.message.from_user.username
        nuevoUsu = buscarContacto(chatId)

        if nuevoUsu == 0:
            altaContactos(chatId,alias)

        update.message.reply_text('Elige una opción:', reply_markup=botones())
    else:
        keyboard = [[InlineKeyboardButton("Privado 🤖", url = 't.me/ClashRoyaleAPIBot')]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text("El funcionamiento del bot es por privado", reply_markup=reply_markup)

def enlace(usuario,peticion):
    if peticion == "info":
        usuarioInfo = requests.get('https://api.clashroyale.com/v1/players/%23' + str(usuario), headers=headers)
        usuarioInfoJson = usuarioInfo.json()

        return usuarioInfoJson
    elif peticion == "cofres":
        usuarioCofres = requests.get('https://api.clashroyale.com/v1/players/%23' + str(usuario) + "/upcomingchests", headers=headers)
        usuarioCofresJson = usuarioCofres.json()

        return usuarioCofresJson
    elif peticion == "clan":
        usuarioClan = requests.get('https://api.clashroyale.com/v1/clans/%23' + str(usuario) + "/currentwar", headers=headers)
        usuarioClanJson = usuarioClan.json()

        return usuarioClanJson

def perfil(chatId):
    usuario = sacarTag(chatId)

    if usuario != "None":
        try:
            usuarioInfoJson = enlace(usuario,"info")
            nombre = str(usuarioInfoJson['name'])
            arena = str(usuarioInfoJson['arena']['name'])

            try:
                currentSeasonT = str(usuarioInfoJson["leagueStatistics"]["currentSeason"]["trophies"])
                currentSeasonBT = str(usuarioInfoJson["leagueStatistics"]["currentSeason"]["bestTrophies"])
            except:
                currentSeasonT = "No ha jugado esta temporada"
                currentSeasonBT = "No ha jugado esta temporada"

            warDayWins = str(usuarioInfoJson['warDayWins'])
            challengeMaxWins = str(usuarioInfoJson['challengeMaxWins'])

            try:
                clan = str(usuarioInfoJson['clan']['name'])
            except:
                clan = "Sin clan"
                
            donations = str(usuarioInfoJson['donations'])
            donationsReceived = str(usuarioInfoJson['donationsReceived'])
            respuesta = "Nombre: " + nombre + "\nArena: " + arena + "\nTrofeos en la temporada actual: " + currentSeasonT + "\nRécord de trofeos en la temporada actual: " + currentSeasonBT + "\nVictorias en guerra de clanes: " + warDayWins + "\nRécord en victorias en desafíos: " + challengeMaxWins + "\nClan: " + clan + "\nDonaciones realizadas: " + donations + "\nDonaciones recibidas: " + donationsReceived
            
            return respuesta
        except:
            return "API caída"
    else:
        return "Usuario no registrado.\nTiene que introducir tu tag en el comando, ejemplo:\n/register 2Y0J28QY"

def trofeos(chatId):
    usuario = sacarTag(chatId)

    if usuario != "None":
        try:
            usuarioInfoJson = enlace(usuario,"info")

            nombre = str(usuarioInfoJson['name'])

            try:
                currentSeasonT = str(usuarioInfoJson["leagueStatistics"]["currentSeason"]["trophies"])
                currentSeasonBT = str(usuarioInfoJson["leagueStatistics"]["currentSeason"]["bestTrophies"])
            except:
                currentSeasonT = "No ha jugado esta temporada"
                currentSeasonBT = "No ha jugado esta temporada"

            try:
                previousSeasonT = str(usuarioInfoJson["leagueStatistics"]["previousSeason"]["trophies"])
                previousSeasonBT = str(usuarioInfoJson["leagueStatistics"]["previousSeason"]["bestTrophies"])
            except:
                previousSeasonT = "No ha jugado la temporada anterior"
                previousSeasonBT = "No ha jugado la temporada anterior"
                
            try:
                bestSeasonT = str(usuarioInfoJson["leagueStatistics"]["bestSeason"]["trophies"])
            except:
                bestSeasonT = "Primera temporada"

            respuesta = "Nombre: " + nombre + "\nTrofeos 🏆\n\t\t+ Temporada actual:\n\t\t\t\t- Trofeos: " + currentSeasonT + "\n\t\t\t\t- Récord de trofeos: " + currentSeasonBT + "\n\t\t+ Temporada pasada:\n\t\t\t\t- Trofeos: " + previousSeasonT + "\n\t\t\t\t- Récord de trofeos: " + previousSeasonBT + "\n\t\t+ Mejor temporada:\n\t\t\t\t- Récord de trofeos: " + bestSeasonT

            return respuesta
        except:
            return "API caída"
    else:
        return "Usuario no registrado.\nTiene que introducir tu tag en el comando, ejemplo:\n/register 2Y0J28QY"

def cofres(chatId):
    usuario = sacarTag(chatId)

    if usuario != "None":
        try:
            usuarioCofresJson = enlace(usuario,"cofres")

            cofre00 = str(usuarioCofresJson["items"][0]["name"])
            cofre01 = str(usuarioCofresJson["items"][1]["name"])
            cofre02 = str(usuarioCofresJson["items"][2]["name"])
            cofre03 = str(usuarioCofresJson["items"][3]["name"])
            cofre04 = str(usuarioCofresJson["items"][4]["name"])
            cofre05 = str(usuarioCofresJson["items"][5]["name"])
            cofre06 = str(usuarioCofresJson["items"][6]["name"])
            cofre07 = str(usuarioCofresJson["items"][7]["name"])
            cofre08 = str(usuarioCofresJson["items"][8]["name"])
            try:
                cofreNumero09 = str(usuarioCofresJson["items"][9]["index"] + 1)
                cofre09 = str(usuarioCofresJson["items"][9]["name"])
            except:
                cofreNumero09 = ""
                cofre09 = ""
            try:
                cofreNumero10 = str(usuarioCofresJson["items"][10]["index"] + 1)
                cofre10 = str(usuarioCofresJson["items"][10]["name"])
            except:
                cofreNumero10 = ""
                cofre10 = ""
            try:
                cofreNumero11 = str(usuarioCofresJson["items"][11]["index"] + 1)
                cofre11 = str(usuarioCofresJson["items"][11]["name"])
            except:
                cofreNumero11 = ""
                cofre11 = ""
            try:
                cofreNumero12 = str(usuarioCofresJson["items"][12]["index"] + 1)
                cofre12 = str(usuarioCofresJson["items"][12]["name"])
            except:
                cofreNumero12 = ""
                cofre12 = ""
            try:
                cofreNumero13 = str(usuarioCofresJson["items"][13]["index"] + 1)
                cofre13 = str(usuarioCofresJson["items"][13]["name"])
            except:
                cofreNumero13 = ""
                cofre13 = ""

            lista = [cofre00, cofre01, cofre02, cofre03, cofre04, cofre05, cofre06, cofre07, cofre08, cofre09, cofre10, cofre11, cofre12, cofre13]

            numero = 0
            for cofre in lista:
                if cofre == "Silver Chest":
                    lista[numero] = "Cofre de plata"
                elif cofre == "Golden Chest":
                    lista[numero] = "Cofre de oro"
                elif cofre == "Giant Chest":
                    lista[numero] = "Cofre gigante"
                elif cofre == "Epic Chest":
                    lista[numero] = "Cofre épico"
                elif cofre == "Magical Chest":
                    lista[numero] = "Cofre mágico"
                elif cofre == "Legendary Chest":
                    lista[numero] = "Cofre legendario"
                elif cofre == "Mega Lightning Chest":
                    lista[numero] = "Cofre megarelámpago"

                numero += 1

            respuesta = "Siguientes cofres:\n 1: " + lista[0] + "\n 2: " + lista[1] + "\n 3: " + lista[2] + "\n 4: " + lista[3] + "\n 5: " + lista[4] + "\n 6: " + lista[5] + "\n 7: " + lista[6] + "\n 8: " + lista[7] + "\n9: " + lista[8] + "\n" + cofreNumero09 + ": " + lista[9] + "\n" + cofreNumero10 + ": " + lista[10] + "\n" + cofreNumero11 + ": " + lista[11] + "\n" + cofreNumero12 + ": " + lista[12] + "\n" + cofreNumero13 + ": " + lista[13]

            return respuesta
        except:
            return "API caída"
    else:
        return "Usuario no registrado.\nTiene que introducir tu tag en el comando, ejemplo:\n/register 2Y0J28QY"

def clan(chatId):
    usuario = sacarTag(chatId)

    if usuario != "None":
        try:
            usuarioInfoJson = enlace(usuario,"info")
            clan = str(usuarioInfoJson['clan']['tag'])
            clan = clan.replace('#', '', 1)
            usuarioClanJson = enlace(clan,"clan")
            state = str(usuarioClanJson['state'])

            if state == "notInWar":
                return "No en guerra"
            else:
                name = str(usuarioClanJson['clan']['name'])
                clanScore = str(usuarioClanJson['clan']['clanScore'])
                participants = str(usuarioClanJson['clan']['participants'])
                battlesPlayed = str(usuarioClanJson['clan']['battlesPlayed'])
                wins = str(usuarioClanJson['clan']['wins'])
                crowns = str(usuarioClanJson['clan']['crowns'])

                if state == "collectionDay":
                    state = "Día de recolección"
                elif state == "warDay":
                    state = "En guerra"

                if state == "En guerra":
                    otroNombre0 = str(usuarioClanJson['clans'][0]['name'])
                    otroClanScore0 = str(usuarioClanJson['clans'][0]['clanScore'])
                    otroParticipants0 = str(usuarioClanJson['clans'][0]['participants'])
                    otroBattlesPlayed0 = str(usuarioClanJson['clans'][0]['battlesPlayed'])
                    otroWins0 = str(usuarioClanJson['clans'][0]['wins'])
                    otroCrowns0 = str(usuarioClanJson['clans'][0]['crowns'])

                    otroNombre1 = str(usuarioClanJson['clans'][1]['name'])
                    otroClanScore1 = str(usuarioClanJson['clans'][1]['clanScore'])
                    otroParticipants1 = str(usuarioClanJson['clans'][1]['participants'])
                    otroBattlesPlayed1 = str(usuarioClanJson['clans'][1]['battlesPlayed'])
                    otroWins1 = str(usuarioClanJson['clans'][1]['wins'])
                    otroCrowns1 = str(usuarioClanJson['clans'][1]['crowns'])
                    
                    otroNombre2 = str(usuarioClanJson['clans'][2]['name'])
                    otroClanScore2 = str(usuarioClanJson['clans'][2]['clanScore'])
                    otroParticipants2 = str(usuarioClanJson['clans'][2]['participants'])
                    otroBattlesPlayed2 = str(usuarioClanJson['clans'][2]['battlesPlayed'])
                    otroWins2 = str(usuarioClanJson['clans'][2]['wins'])
                    otroCrowns2 = str(usuarioClanJson['clans'][2]['crowns'])
                    
                    otroNombre3 = str(usuarioClanJson['clans'][3]['name'])
                    otroClanScore3 = str(usuarioClanJson['clans'][3]['clanScore'])
                    otroParticipants3 = str(usuarioClanJson['clans'][3]['participants'])
                    otroBattlesPlayed3 = str(usuarioClanJson['clans'][3]['battlesPlayed'])
                    otroWins3 = str(usuarioClanJson['clans'][3]['wins'])
                    otroCrowns3 = str(usuarioClanJson['clans'][3]['crowns'])
                    
                    respuesta = "Situación: " + state + "\nNombre: " + otroNombre0 + "\nPuntuación: " + otroClanScore0 + "\nParticipantes: " + otroParticipants0 + "\nBatallas jugadas: " + otroBattlesPlayed0 + "\nVictorias: " + otroWins0 + "\nCoronas: " + otroCrowns0 + "\n\nNombre: " + otroNombre1 + "\nPuntuación: " + otroClanScore1 + "\nParticipantes: " + otroParticipants1 + "\nBatallas jugadas: " + otroBattlesPlayed1 + "\nVictorias: " + otroWins1 + "\nCoronas: " + otroCrowns1 + "\n\nNombre: " + otroNombre2 + "\nPuntuación: " + otroClanScore2 + "\nParticipantes: " + otroParticipants2 + "\nBatallas jugadas: " + otroBattlesPlayed2 + "\nVictorias: " + otroWins2 + "\nCoronas: " + otroCrowns2 + "\n\nNombre: " + otroNombre3 + "\nPuntuación: " + otroClanScore3 + "\nParticipantes: " + otroParticipants3 + "\nBatallas jugadas: " + otroBattlesPlayed3 + "\nVictorias: " + otroWins3 + "\nCoronas: " + otroCrowns3

                    return respuesta
                else:
                    respuesta = "Situación: " + state + "\nNombre: " + name + "\nPuntuación del clan: " + clanScore + "\nParticipantes: " + participants + "\nBatallas jugadas: " + battlesPlayed + "\nVictorias: " + wins + "\nCoronas: " + crowns

                    return respuesta
        except:
            return "Sin clan"
    else:
        return "Usuario no registrado.\nTiene que introducir tu tag en el comando, ejemplo:\n/register 2Y0J28QY"

if __name__ == '__main__':
    main()