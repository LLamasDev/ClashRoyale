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
        con = pymysql.connect("SERVER", "USER", "PASSWORD", "DATA BASE")
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
    elif query.data == 'ataca':
        bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=ataca(chatId), reply_markup=botones())
    elif query.data == 'guerras':
        bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=guerra(chatId), reply_markup=botones())

def botones():
    keyboard = [[InlineKeyboardButton("Perfil", callback_data='perfil')], [InlineKeyboardButton("Trofeos", callback_data='trofeos'), InlineKeyboardButton("Cofres", callback_data='cofres')], [InlineKeyboardButton("Falta por atacar", callback_data='ataca'), InlineKeyboardButton("Guerras", callback_data='guerras')]]
    
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

            respuesta = "Trofeos 🏆\n\t\t+ Temporada actual:\n\t\t\t\t- Trofeos: " + currentSeasonT + "\n\t\t\t\t- Récord de trofeos: " + currentSeasonBT + "\n\t\t+ Temporada pasada:\n\t\t\t\t- Trofeos: " + previousSeasonT + "\n\t\t\t\t- Récord de trofeos: " + previousSeasonBT + "\n\t\t+ Mejor temporada:\n\t\t\t\t- Récord de trofeos: " + bestSeasonT

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
            respuesta = "Siguientes cofres:"
            diccionario = {}
            numero = 1

            cofre00 = str(usuarioCofresJson["items"][0]["name"])
            cofre01 = str(usuarioCofresJson["items"][1]["name"])
            cofre02 = str(usuarioCofresJson["items"][2]["name"])
            cofre03 = str(usuarioCofresJson["items"][3]["name"])
            cofre04 = str(usuarioCofresJson["items"][4]["name"])
            cofre05 = str(usuarioCofresJson["items"][5]["name"])
            cofre06 = str(usuarioCofresJson["items"][6]["name"])
            cofre07 = str(usuarioCofresJson["items"][7]["name"])
            cofre08 = str(usuarioCofresJson["items"][8]["name"])

            lista = [cofre00, cofre01, cofre02, cofre03, cofre04, cofre05, cofre06, cofre07, cofre08]

            for x in lista:
                diccionario[numero] = numero, x
                numero += 1

            try:
                cofreNumero09 = str(usuarioCofresJson["items"][9]["index"] + 1)
                cofre09 = str(usuarioCofresJson["items"][9]["name"])
                
                diccionario[numero] = cofreNumero09, cofre09
                numero += 1
            except:
                pass
            try:
                cofreNumero10 = str(usuarioCofresJson["items"][10]["index"] + 1)
                cofre10 = str(usuarioCofresJson["items"][10]["name"])
                
                diccionario[numero] = cofreNumero10, cofre10
                numero += 1
            except:
                pass
            try:
                cofreNumero11 = str(usuarioCofresJson["items"][11]["index"] + 1)
                cofre11 = str(usuarioCofresJson["items"][11]["name"])
                
                diccionario[numero] = cofreNumero11, cofre11
                numero += 1
            except:
                pass
            try:
                cofreNumero12 = str(usuarioCofresJson["items"][12]["index"] + 1)
                cofre12 = str(usuarioCofresJson["items"][12]["name"])
                
                diccionario[numero] = cofreNumero12, cofre12
                numero += 1
            except:
                pass
            try:
                cofreNumero13 = str(usuarioCofresJson["items"][13]["index"] + 1)
                cofre13 = str(usuarioCofresJson["items"][13]["name"])
                
                diccionario[numero] = cofreNumero13, cofre13
            except:
                pass

            for numeros,cofre in diccionario.items():
                if cofre[1] == "Silver Chest":
                    respuesta += "\n" + str(cofre[0]) + " para un cofre de plata"
                elif cofre[1] == "Golden Chest":
                    respuesta += "\n" + str(cofre[0]) + " para un cofre de oro"
                elif cofre[1] == "Giant Chest":
                    respuesta += "\n" + str(cofre[0]) + " para un cofre gigante"
                elif cofre[1] == "Epic Chest":
                    respuesta += "\n" + str(cofre[0]) + " para un cofre épico"
                elif cofre[1] == "Magical Chest":
                    respuesta += "\n" + str(cofre[0]) + " para un cofre mágico"
                elif cofre[1] == "Legendary Chest":
                    respuesta += "\n" + str(cofre[0]) + " para un cofre legendario"
                elif cofre[1] == "Mega Lightning Chest":
                    respuesta += "\n" + str(cofre[0]) + " para un cofre megarelámpago"

            return respuesta
        except:
            return "API caída"
    else:
        return "Usuario no registrado.\nTiene que introducir tu tag en el comando, ejemplo:\n/register 2Y0J28QY"

def guerra(chatId):
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
                    state = "día de recolección"
                elif state == "warDay":
                    state = "guerra"

                if state == "guerra":
                    otroNombre0 = str(usuarioClanJson['clans'][0]['name'])
                    otroClanScore0 = str(usuarioClanJson['clans'][0]['clanScore'])
                    otroWins0 = int(usuarioClanJson['clans'][0]['wins'])
                    otroCrowns0 = int(usuarioClanJson['clans'][0]['crowns'])
                    otroParticipants0 = str(usuarioClanJson['clans'][0]['participants'])
                    otroBattlesPlayed0 = str(usuarioClanJson['clans'][0]['battlesPlayed'])

                    otroNombre1 = str(usuarioClanJson['clans'][1]['name'])
                    otroClanScore1 = str(usuarioClanJson['clans'][1]['clanScore'])
                    otroWins1 = int(usuarioClanJson['clans'][1]['wins'])
                    otroCrowns1 = int(usuarioClanJson['clans'][1]['crowns'])
                    otroParticipants1 = str(usuarioClanJson['clans'][1]['participants'])
                    otroBattlesPlayed1 = str(usuarioClanJson['clans'][1]['battlesPlayed'])
                    
                    otroNombre2 = str(usuarioClanJson['clans'][2]['name'])
                    otroClanScore2 = str(usuarioClanJson['clans'][2]['clanScore'])
                    otroWins2 = int(usuarioClanJson['clans'][2]['wins'])
                    otroCrowns2 = int(usuarioClanJson['clans'][2]['crowns'])
                    otroParticipants2 = str(usuarioClanJson['clans'][2]['participants'])
                    otroBattlesPlayed2 = str(usuarioClanJson['clans'][2]['battlesPlayed'])
                    
                    otroNombre3 = str(usuarioClanJson['clans'][3]['name'])
                    otroClanScore3 = str(usuarioClanJson['clans'][3]['clanScore'])
                    otroWins3 = int(usuarioClanJson['clans'][3]['wins'])
                    otroCrowns3 = int(usuarioClanJson['clans'][3]['crowns'])
                    otroParticipants3 = str(usuarioClanJson['clans'][3]['participants'])
                    otroBattlesPlayed3 = str(usuarioClanJson['clans'][3]['battlesPlayed'])
                    
                    otroNombre4 = str(usuarioClanJson['clans'][4]['name'])
                    otroClanScore4 = str(usuarioClanJson['clans'][4]['clanScore'])
                    otroWins4 = int(usuarioClanJson['clans'][4]['wins'])
                    otroCrowns4 = int(usuarioClanJson['clans'][4]['crowns'])
                    otroParticipants4 = str(usuarioClanJson['clans'][4]['participants'])
                    otroBattlesPlayed4 = str(usuarioClanJson['clans'][4]['battlesPlayed'])

                    lista = [[otroNombre0,otroClanScore0,otroWins0,otroCrowns0,otroParticipants0,otroBattlesPlayed0],[otroNombre1,otroClanScore1,otroWins1,otroCrowns1,otroParticipants1,otroBattlesPlayed1],[otroNombre2,otroClanScore2,otroWins2,otroCrowns2,otroParticipants2,otroBattlesPlayed2],[otroNombre3,otroClanScore3,otroWins3,otroCrowns3,otroParticipants3,otroBattlesPlayed3],[otroNombre4,otroClanScore4,otroWins4,otroCrowns4,otroParticipants4,otroBattlesPlayed4]]
                    lista.sort(key=lambda x: (-x[2], -x[3]))

                    respuesta = name + " en " + state + ".\n1 - " + lista[0][0] + "\nPuntuación: " + lista[0][1] + "\nVictorias: " + str(lista[0][2]) + "\nCoronas: " + str(lista[0][3]) + "\nParticipantes: " + lista[0][4] + "\nBatallas jugadas: " + lista[0][5] + "\n\n2 - " + lista[1][0] + "\nPuntuación: " + lista[1][1] + "\nVictorias: " + str(lista[1][2]) + "\nCoronas: " + str(lista[1][3]) + "\nParticipantes: " + lista[1][4] + "\nBatallas jugadas: " + lista[1][5] + "\n\n3 - " + lista[2][0] + "\nPuntuación: " + lista[2][1] + "\nVictorias: " + str(lista[2][2]) + "\nCoronas: " + str(lista[2][3]) + "\nParticipantes: " + lista[2][4] + "\nBatallas jugadas: " + lista[2][5] + "\n\n4 - " + lista[3][0] + "\nPuntuación: " + lista[3][1] + "\nVictorias: " + str(lista[3][2]) + "\nCoronas: " + str(lista[3][3]) + "\nParticipantes: " + lista[3][4] + "\nBatallas jugadas: " + lista[3][5] + "\n\n5 - " + lista[4][0] + "\nPuntuación: " + lista[4][1] + "\nVictorias: " + str(lista[4][2]) + "\nCoronas: " + str(lista[4][3]) + "\nParticipantes: " + lista[4][4] + "\nBatallas jugadas: " + lista[4][5]
                    
                    return respuesta
                else:
                    respuesta = name + " en " + state + ".\nPuntuación del clan: " + clanScore + "\nParticipantes: " + participants + "\nBatallas jugadas: " + battlesPlayed + "\nVictorias: " + wins + "\nCoronas: " + crowns

                    return respuesta
        except:
            return "Sin clan"
    else:
        return "Usuario no registrado.\nTiene que introducir tu tag en el comando, ejemplo:\n/register 2Y0J28QY"

def ataca(chatId):
    usuario = sacarTag(chatId)

    if usuario != "None":
        usuarioInfoJson = enlace(usuario,"info")
        clan = str(usuarioInfoJson['clan']['tag'])
        clan = clan.replace('#', '', 1)
        nameClan = str(usuarioInfoJson['clan']['name'])
        usuarioAtacaJson = enlace(clan,"clan")
        state = str(usuarioAtacaJson['state'])

        if state != "notInWar":
            try:
                diccionario = {}
                dentro = True
                numero = 0
                
                if state == "collectionDay":
                    state = "día de recolección"
                elif state == "warDay":
                    state = "guerra"

                respuesta = nameClan + " en " + state + ".\nAtaques que faltan:"

                while dentro == True:
                    try:
                        numberOfBattles = int(usuarioAtacaJson["participants"][numero]["numberOfBattles"])
                        battlesPlayed = int(usuarioAtacaJson["participants"][numero]["battlesPlayed"])

                        resultado = numberOfBattles - battlesPlayed

                        if resultado > 0:
                            name = str(usuarioAtacaJson["participants"][numero]["name"])

                            diccionario[name] = resultado

                        numero += 1
                    except:
                        dentro = False

                for nombre,falta in diccionario.items():
                    respuesta += "\n" + nombre + " le faltan " + str(falta)

                return respuesta
            except:
                return "API caída"
        else:
            return "No en guerra"
    else:
        return "Usuario no registrado.\nTiene que introducir tu tag en el comando, ejemplo:\n/register 2Y0J28QY"

if __name__ == '__main__':
    main()