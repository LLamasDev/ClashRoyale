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

def sacarTag(chatId):
    con,cursor = conexionBDD()
    sql = "SELECT tag FROM usuario WHERE id = %s"
    datos = (chatId)
    cursor.execute(sql, datos)

    for tag in cursor:
        respuesta = tag[0]

    cursor.close()

    return respuesta

def altaContactos(chatId,alias):
    con,cursor = conexionBDD()
    sql = "INSERT INTO usuario (id,alias) VALUES (%s, %s)"
    datos = (chatId,alias)
    cursor.execute(sql, datos)
    con.commit()
    con.close()

def boton(update, context):
    query = update.callback_query
    bot = context.bot
    chatId = query.message.chat_id

    if query.data == 'perfil':
        bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=perfil(chatId), reply_markup=botones())
    elif query.data == 'cartas':
        bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=cartas(chatId), reply_markup=botones())
    elif query.data == 'cofres':
        bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=cofres(chatId), reply_markup=botones())
    elif query.data == 'ataca':
        bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=ataca(chatId), reply_markup=botones())
    elif query.data == 'guerras':
        bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=guerra(chatId), reply_markup=botones())

def botones():
    keyboard = [[InlineKeyboardButton("Perfil", callback_data='perfil')], [InlineKeyboardButton("Cartas", callback_data='cartas'), InlineKeyboardButton("Cofres", callback_data='cofres')], [InlineKeyboardButton("Falta por atacar", callback_data='ataca'), InlineKeyboardButton("Guerras", callback_data='guerras')]]
    
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
            warDayWins = str(usuarioInfoJson['warDayWins'])
            challengeMaxWins = str(usuarioInfoJson['challengeMaxWins'])

            try:
                clan = str(usuarioInfoJson['clan']['name'])
                role = str(usuarioInfoJson['role'])

                if role == "member":
                    role = "Miembro"
                elif role == "coLeader":
                    role = "Colíder"
                elif role == "leader":
                    role = "Líder"
                    
                clan = role + " en " + clan
            except:
                clan = "Sin clan"

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

            donations = str(usuarioInfoJson['donations'])
            donationsReceived = str(usuarioInfoJson['donationsReceived'])
            respuesta = "Nombre: " + nombre + "\nArena: " + arena + "\nVictorias en guerra de clanes: " + warDayWins + "\nRécord en victorias en desafíos: " + challengeMaxWins + "\n" + clan + "\nDonaciones realizadas: " + donations + "\nDonaciones recibidas: " + donationsReceived + "\n\nTrofeos 🏆\n\t\t+ Temporada actual:\n\t\t\t\t- Trofeos: " + currentSeasonT + "\n\t\t\t\t- Récord de trofeos: " + currentSeasonBT + "\n\t\t+ Temporada pasada:\n\t\t\t\t- Trofeos: " + previousSeasonT + "\n\t\t\t\t- Récord de trofeos: " + previousSeasonBT + "\n\t\t+ Mejor temporada:\n\t\t\t\t- Récord de trofeos: " + bestSeasonT
            
            return respuesta
        except:
            return "API caída"
    else:
        return "Usuario no registrado.\nTiene que introducir tu tag en el comando, ejemplo:\n/register 2Y0J28QY"

def cartas(chatId):
    usuario = sacarTag(chatId)

    if usuario != "None":
        try:
            usuarioInfoJson = enlace(usuario,"info")
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
            dentro = True

            while dentro == True:
                try:
                    level = int(usuarioInfoJson['cards'][numero]['level'])
                    maxLevel = int(usuarioInfoJson['cards'][numero]['maxLevel'])

                    resultado = maxLevel - level
                    diccionario = {"comun": (5,20,50,150,400,1000,2000,4000,8000,20000,50000,100000), "especial": (50,150,400,1000,2000,4000,8000,20000,50000,100000), "epica": (400,2000,4000,8000,20000,50000,100000), "legendaria": (5000,20000,50000,100000)}

                    if resultado > 0:
                        if maxLevel == 5:
                            for i in range(resultado, 0, -1):
                                oro += diccionario["legendaria"][-i]
                                legendariaOro += diccionario["legendaria"][-i]
                                legendariaContador += 1
                        elif maxLevel == 8:
                            for i in range(resultado, 0, -1):
                                oro += diccionario["epica"][-i]
                                epicaOro += diccionario["epica"][-i]
                                epicaContador += 1
                        elif maxLevel == 11:
                            for i in range(resultado, 0, -1):
                                oro += diccionario["especial"][-i]
                                especialOro += diccionario["especial"][-i]
                                especialContador += 1
                        elif maxLevel == 13:
                            for i in range(resultado, 0, -1):
                                oro += diccionario["comun"][-i]
                                comunOro += diccionario["comun"][-i]
                                comunContador += 1

                    numero += 1
                except:
                    dentro = False

            cartasContador = comunContador + especialContador + epicaContador + legendariaContador
            respuesta = "Oro necesario para subir al máximo.\nTe faltan " + str(comunContador) + " niveles de cartas comunes: " + str(comunOro) + " de oro\nTe faltan " + str(especialContador) + " niveles de cartas especiales: " + str(especialOro) + " de oro\nTe faltan " + str(epicaContador) + " niveles de cartas épicas: " + str(epicaOro) + " de oro\nTe faltan " + str(legendariaContador) + " niveles de cartas legendarias: " + str(legendariaOro) + " de oro\nTe faltan " + str(cartasContador) + " niveles en total: " + str(oro) + " de oro"

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
            numero = 0
            dentro = True

            while dentro == True:
                try:
                    cofreNumero = int(usuarioCofresJson["items"][numero]["index"] + 1)
                    cofre = str(usuarioCofresJson["items"][numero]["name"])

                    diccionario[numero] = cofreNumero, cofre
                    numero += 1
                except:
                    dentro = False
                    
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
                numero = 0
                dentro = True
                
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

                respuesta = name + " en " + state + "."

                if state == "guerra":
                    listaFinal = []
                    numero = 0
                    dentro = True

                    while dentro == True:
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
                            dentro = False

                    listaFinal.sort(key=lambda x: (-x[2], -x[3]))

                    numeros = 1
                    for clanGuerra in listaFinal:
                        respuesta += "\n\n" + str(numeros) + " - " + clanGuerra[0] + "\nPuntuación: " + clanGuerra[1] + "\nVictorias: " + str(clanGuerra[2]) + "\nCoronas: " + str(clanGuerra[3]) + "\nParticipantes: " + clanGuerra[4] + "\nBatallas jugadas: " + clanGuerra[5]

                        numeros += 1
                    return respuesta
                else:
                    respuesta += "\nPuntuación del clan: " + clanScore + "\nParticipantes: " + participants + "\nBatallas jugadas: " + battlesPlayed + "\nVictorias: " + wins + "\nCoronas: " + crowns
                    
                    return respuesta
        except:
            return "Sin clan"
    else:
        return "Usuario no registrado.\nTiene que introducir tu tag en el comando, ejemplo:\n/register 2Y0J28QY"

if __name__ == '__main__':
    main()