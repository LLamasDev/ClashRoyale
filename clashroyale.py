#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
import requests
import urllib.request
from datetime import date
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from botondonaciones import *
from funcionesrepes import *
from botoninactivos import *
from botonguerras import *
from botonperfil import *
from botoncofres import *
from botonguerra import *
from translate import *
from botonclan import *
from enlaceapi import *
from botonoro import *
from data import *
from db import *

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    updater = Updater(TOKEN, use_context=True)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('registro', register, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('sinatacarenguerra', ataca))
    updater.dispatcher.add_handler(CommandHandler('topdecks', topDecks))
    updater.dispatcher.add_handler(CommandHandler('lang', lang, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('idiomasDisponibles', supportedLanguages))
    updater.dispatcher.add_handler(CommandHandler('auto', auto))
    updater.dispatcher.add_handler(CommandHandler('es', es))
    updater.dispatcher.add_handler(CommandHandler('en', en))
    updater.dispatcher.add_handler(CommandHandler('all', all))
    updater.dispatcher.add_handler(CommandHandler('yo', yo))
    updater.dispatcher.add_handler(CommandHandler('info', info))
    updater.dispatcher.add_handler(CallbackQueryHandler(boton))
    updater.start_polling()
    updater.idle()

def all(update,context):
    chatId = update.message.from_user.id

    usoUsu(chatId)

    if chatId == miID:
        con,cursor = conexionBDD()
        cursor.execute('SELECT count(*) FROM usuario')
        contadorTotal = cursor.fetchone()[0]
        cursor.execute('SELECT count(*) FROM clanes')
        contadorGrupos = cursor.fetchone()[0]
        cursor.execute('SELECT sum(usoHoy) FROM usuario')
        contadorUsoHoy = cursor.fetchone()[0]
        cursor.execute('SELECT sum(usoTotal) FROM usuario')
        contadorUsoTotal = cursor.fetchone()[0]
        cursor.execute('SELECT idioma, COUNT(*) FROM usuario GROUP BY idioma ORDER BY COUNT(*) DESC')
        contadorIdiomas = ''

        for idioma in cursor:
            contadorIdiomas += '\t - ' + str(traducirIdioma(idioma[0])) + ': ' + str(idioma[1]) + '\n'

        cursor.close()

        consulta = 'Estadísticas @ClashRoyaleAPIBot:\n\t - Usuarios que han usado el bot: ' + str(contadorTotal) + '\n\t - Grupos que han usado el bot: ' + str(contadorGrupos) + '\n\nComandos usados:\n\t - Hoy: ' + str(contadorUsoHoy) + '\n\t - Total: ' + str(contadorUsoTotal) + '\n\nIdiomas en uso:\n' + contadorIdiomas

        update.message.reply_text(consulta)

def yo(update,context):
    chatId = update.message.from_user.id

    usoUsu(chatId)

    if chatId == miID:
        consulta = estadisticas()

        update.message.reply_text(consulta)

def boton(update,context):
    query = update.callback_query
    bot = context.bot
    chatId = query.message.chat_id

    if query.data == 'perfil':
        usoUsu(chatId)
        texto = traducir(chatId,perfil(chatId))
        bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=texto, reply_markup=botones(chatId))
    elif query.data == 'cofres':
        usoUsu(chatId)
        texto = traducir(chatId,cofres(chatId))
        bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=texto, reply_markup=botones(chatId))
    elif query.data == 'cartas':
        usoUsu(chatId)
        texto = traducir(chatId,cartas(chatId))
        bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=texto, reply_markup=botones(chatId))
    elif query.data == 'donaciones':
        usoUsu(chatId)
        texto = traducir(chatId,donaciones(chatId))
        bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=texto, reply_markup=botones(chatId))
    elif query.data == 'guerras':
        usoUsu(chatId)
        texto = traducir(chatId,guerras(chatId))
        bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=texto, reply_markup=botones(chatId))
    elif query.data == 'guerra':
        usoUsu(chatId)
        texto = traducir(chatId,guerra(chatId))
        bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=texto, reply_markup=botones(chatId))
    elif query.data == 'inactivos':
        usoUsu(chatId)
        texto = traducir(chatId,inactivos(chatId))
        bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=texto, reply_markup=botones(chatId))
    elif query.data == 'clan':
        usoUsu(chatId)
        texto = traducir(chatId,clan(chatId))
        bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text='\t 🏆 \t ' + texto, reply_markup=botones(chatId))

def botones(chatId):
    idioma = saberIdioma(chatId)

    if idioma == 'es':
        keyboard = [[InlineKeyboardButton('Información del perfil', callback_data='perfil'), InlineKeyboardButton('Siguientes cofres', callback_data='cofres')], [InlineKeyboardButton('Oro para las cartas', callback_data='cartas'), InlineKeyboardButton('Donaciones', callback_data='donaciones')], [InlineKeyboardButton('Actividad en guerras', callback_data='guerras'), InlineKeyboardButton('Ranking en la guerra', callback_data='guerra')], [InlineKeyboardButton('Inactivos del clan', callback_data='inactivos'), InlineKeyboardButton('Miembros del clan', callback_data='clan')]]
    elif idioma == 'en':
        keyboard = [[InlineKeyboardButton('Profile info', callback_data='perfil'), InlineKeyboardButton('Next chests', callback_data='cofres')], [InlineKeyboardButton('Gold for card', callback_data='cartas'), InlineKeyboardButton('Donations', callback_data='donaciones')], [InlineKeyboardButton('Activity in wars', callback_data='guerras'), InlineKeyboardButton('Ranking in the war', callback_data='guerra')], [InlineKeyboardButton('Inactive in the clan', callback_data='inactivos'), InlineKeyboardButton('Clan members', callback_data='clan')]]
    else:
        perfilI = traducir(chatId,'Información del perfil')
        cofresI = traducir(chatId,'Siguientes cofres')
        cartasI = traducir(chatId,'Oro para las cartas')
        donacionesI = traducir(chatId,'Donaciones')
        guerrasI = traducir(chatId,'Actividad en guerras')
        guerraI = traducir(chatId,'Ranking en la guerra')
        inactivosI = traducir(chatId,'Inactivos del clan')
        clanI = traducir(chatId,'Miembros del clan')
        keyboard = [[InlineKeyboardButton(perfilI, callback_data='perfil'), InlineKeyboardButton(cofresI, callback_data='cofres')], [InlineKeyboardButton(cartasI, callback_data='cartas'), InlineKeyboardButton(donacionesI, callback_data='donaciones')], [InlineKeyboardButton(guerrasI, callback_data='guerras'), InlineKeyboardButton(guerraI, callback_data='guerra')], [InlineKeyboardButton(inactivosI, callback_data='inactivos'), InlineKeyboardButton(clanI, callback_data='clan')]]

    return InlineKeyboardMarkup(keyboard)

def start(update, context):
    tipo = update.message.chat.type
    alias = update.message.from_user.username
    chatId = update.message.from_user.id
    nuevoUsu = buscarContacto(chatId)
    
    if nuevoUsu == 0:
        altaContactos(chatId,alias)

    usoUsu(chatId)

    if tipo == 'private':
        nuevoUsu = buscarContacto(chatId)

        if nuevoUsu == 0:
            altaContactos(chatId,alias)
        else:
            sacarAlias(chatId,alias)

        textoI = traducir(chatId,'Elige una opción:')
        update.message.reply_text(textoI, reply_markup=botones(chatId))
    else:
        chatIdChat = update.message.chat.id
        chatNombre = update.message.chat.title
        clanRegistro = saberSiTengoClanSpam(chatIdChat)
            
        if clanRegistro == 0:
            altaClan(chatIdChat,chatNombre)

        nombreBD = sacarNombreClan(chatIdChat)

        if nombreBD != chatNombre:
            cambioNombreClan(chatNombre,chatIdChat)
            
        texto0I = traducir(chatId,'Privado')
        texto1I = traducir(chatId,'El funcionamiento de este comando es por privado')
        keyboard = [[InlineKeyboardButton(texto0I + ' 🤖', url = 't.me/ClashRoyaleAPIBot')]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text(texto1I, reply_markup=reply_markup)

def register(update, context):
    tipo = update.message.chat.type
    alias = update.message.from_user.username
    chatId = update.message.from_user.id
    nuevoUsu = buscarContacto(chatId)
    
    if nuevoUsu == 0:
        altaContactos(chatId,alias)

    usoUsu(chatId)
    
    if tipo == 'private':
        usuDice = ' '.join(context.args)
        con,cursor = conexionBDD()

        try:
            primeraLetra = usuDice[0]

            if primeraLetra == '#':
                usuDice = usuDice.replace('#', '', 1)

            usuarioInfoJson = enlace(usuDice,'info')
            nombre = str(usuarioInfoJson['name'])
            cursor.execute('UPDATE usuario SET tag = %s WHERE id = %s', (usuDice,chatId))
            con.commit()
            con.close()

            textoI = traducir(chatId,'Registrado con el nombre de usuario: ')
            update.message.reply_text(textoI + nombre + ' #' + usuDice)
        except:
            textoI = traducir(chatId,'Usuario no encontrado.\nTiene que introducir tu tag en el comando, ejemplo:')
            update.message.reply_text(textoI + '\n/registro 2Y0J28QY')
    else:
        chatIdChat = update.message.chat.id
        chatNombre = update.message.chat.title
        clanRegistro = saberSiTengoClanSpam(chatIdChat)
            
        if clanRegistro == 0:
            altaClan(chatIdChat,chatNombre)

        nombreBD = sacarNombreClan(chatIdChat)

        if nombreBD != chatNombre:
            cambioNombreClan(chatNombre,chatIdChat)
            
        texto0I = traducir(chatId,'Privado')
        texto1I = traducir(chatId,'El funcionamiento de este comando es por privado')
        keyboard = [[InlineKeyboardButton(texto0I + ' 🤖', url = 't.me/ClashRoyaleAPIBot')]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text(texto1I, reply_markup=reply_markup)

def ataca(update, context):
    alias = update.message.from_user.username
    chatId = update.message.from_user.id
    tipo = update.message.chat.type
    nuevoUsu = buscarContacto(chatId)
    
    if nuevoUsu == 0:
        altaContactos(chatId,alias)

    usoUsu(chatId)
    usuario = sacarTag(chatId)

    if tipo != 'private':
        chatIdChat = update.message.chat.id
        chatNombre = update.message.chat.title
        clanRegistro = saberSiTengoClanSpam(chatIdChat)

        if clanRegistro == 0:
            altaClan(chatIdChat,chatNombre)

        nombreBD = sacarNombreClan(chatIdChat)

        if nombreBD != chatNombre:
            cambioNombreClan(chatNombre,chatIdChat)

        clanSpam = saberClanSpam(chatIdChat)

        if clanSpam == 'si':
            if usuario != 'None':
                textoFuncion = atacaFuncion(alias,chatId,usuario)
                textoI = traducir(chatId,textoFuncion)
                update.message.reply_text(textoI)

                cambioSpam(chatIdChat)
            else:
                texto0I = traducir(chatId,'Privado')
                texto1I = traducir(chatId,'Usuario no registrado, no puedo darte información de tu clan si no tengo tu información.\nTiene que introducir tu tag en el comando por privado, ejemplo:')
                keyboard = [[InlineKeyboardButton(texto0I + ' 🤖', url = 't.me/ClashRoyaleAPIBot')]]
                reply_markup = InlineKeyboardMarkup(keyboard)

                update.message.reply_text(texto1I + '\n/registro 2Y0J28QY', reply_markup=reply_markup)
        else:
            texto0I = traducir(chatId,'Privado')
            texto1I = traducir(chatId,'Hasta las 00:00 no se puede volver a usar el comando, para evitar mencionar más de una vez, si quieres ver los que faltan, usa el comando por privado.')
            keyboard = [[InlineKeyboardButton(texto0I + ' 🤖', url = 't.me/ClashRoyaleAPIBot')]]
            reply_markup = InlineKeyboardMarkup(keyboard)

            update.message.reply_text(texto1I, reply_markup=reply_markup)
    else:
        textoFuncion = atacaFuncion(alias,chatId,usuario)
        textoI = traducir(chatId,textoFuncion)
        update.message.reply_text(textoI)

def topDecks(update, context):
    alias = update.message.from_user.username
    chatId = update.message.from_user.id
    tipo = update.message.chat.type
    nuevoUsu = buscarContacto(chatId)
    
    if nuevoUsu == 0:
        altaContactos(chatId,alias)

    usoUsu(chatId)

    if tipo != 'private':
        chatIdChat = update.message.chat.id
        chatNombre = update.message.chat.title
        clanRegistro = saberSiTengoClanSpam(chatIdChat)

        if clanRegistro == 0:
            altaClan(chatIdChat,chatNombre)

        nombreBD = sacarNombreClan(chatIdChat)

        if nombreBD != chatNombre:
            cambioNombreClan(chatNombre,chatIdChat)

    respuesta = sacoTopDecks()

    update.message.reply_text(respuesta, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

def lang(update, context):
    tipo = update.message.chat.type
    alias = update.message.from_user.username
    chatId = update.message.from_user.id
    nuevoUsu = buscarContacto(chatId)
    
    if nuevoUsu == 0:
        altaContactos(chatId,alias)

    usoUsu(chatId)
    
    if tipo == 'private':
        try:
            usuDice = ' '.join(context.args)

            if len(usuDice) > 0:
                idiomas = traducirIdioma(usuDice)

                if idiomas != None:
                    con,cursor = conexionBDD()
                    cursor.execute('UPDATE usuario SET idioma = %s WHERE id = %s', (usuDice,chatId))
                    con.commit()
                    con.close()

                    idiomasI = traducir(chatId,idiomas)
                    texto = 'Idioma cambiado a ' + idiomasI + '. La siguiente traducción no es exacta, es automática y contiene errores.'
                    textoI = traducir(chatId,texto)
                    update.message.reply_text(textoI)
                else:
                    textoI = traducir(chatId,'Lenguaje no soportado.')
                    update.message.reply_text(textoI)
            else:
                idiomaUsu = update.message.from_user.language_code

                try:
                    idiomas = traducirIdioma(idiomaUsu)
                except:
                    idiomas = 'Idioma no soportado'

                if idiomas == 'Idioma no soportado':
                    texto0 = traducir(chatId,'Todos los idiomas, excepto el español, no son exactos, es una traducción automática y contiene errores.')
                    texto1 = traducir(chatId,'Como usar:')
                    texto2 = traducir(chatId,'abreviatura, por ejemplo')
                    texto3 = traducir(chatId,'Todas las abreviaturas de los lenguajes soportados:')
                    texto = texto0 + '\n' + texto1 + ' /lang ' + texto2 + ' /lang it\n' + texto3 + ' /idiomasDisponibles\n/es - Cambiar el idioma a español\n/en - Change the language to English.'
                else:
                    texto0 = traducir(chatId,'Todos los idiomas, excepto el español, no son exactos, es una traducción automática y contiene errores.')
                    texto1 = traducir(chatId,'Como usar:')
                    texto2 = traducir(chatId,'abreviatura, por ejemplo')
                    texto3 = traducir(chatId,'Todas las abreviaturas de los lenguajes soportados:')
                    texto = texto0 + '\n' + texto1 + ' /lang ' + texto2 + ' /lang it\n' + texto3 + ' /idiomasDisponibles\n/es - Cambiar el idioma a español\n/en - Change the language to English.\n/auto - Change the language to the default in your telegram account, in your case ' + idiomas + '.'

                update.message.reply_text(texto)
        except:
            textoI = traducir(chatId,'Usuario no encontrado.\nTiene que introducir tu tag en el comando, ejemplo:')
            update.message.reply_text(textoI + '\n/registro 2Y0J28QY')
    else:
        chatIdChat = update.message.chat.id
        chatNombre = update.message.chat.title
        clanRegistro = saberSiTengoClanSpam(chatIdChat)
            
        if clanRegistro == 0:
            altaClan(chatIdChat,chatNombre)

        nombreBD = sacarNombreClan(chatIdChat)

        if nombreBD != chatNombre:
            cambioNombreClan(chatNombre,chatIdChat)

        texto0I = traducir(chatId,'Privado')
        texto1I = traducir(chatId,'El funcionamiento de este comando es por privado')
        keyboard = [[InlineKeyboardButton(texto0I + ' 🤖', url = 't.me/ClashRoyaleAPIBot')]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text(texto1I, reply_markup=reply_markup)

def auto(update, context):
    tipo = update.message.chat.type
    alias = update.message.from_user.username
    chatId = update.message.from_user.id
    nuevoUsu = buscarContacto(chatId)
    
    if nuevoUsu == 0:
        altaContactos(chatId,alias)

    usoUsu(chatId)
    
    if tipo == 'private':
        try:
            idiomaUsu = update.message.from_user.language_code

            try:
                idiomas = traducirIdioma(idiomaUsu)
            except:
                idiomas = 'Idioma no soportado'

            if idiomas == 'Idioma no soportado':
                update.message.reply_text('Idioma no soportado.')
            else:
                con,cursor = conexionBDD()
                cursor.execute('UPDATE usuario SET idioma = %s WHERE id = %s', (idiomaUsu,chatId))
                con.commit()
                con.close()

                idiomasI = traducir(chatId,idiomas)
                texto = 'Idioma cambiado a ' + idiomasI + '. La siguiente traducción no es exacta, es automática y contiene errores.'
                textoI = traducir(chatId,texto)
                update.message.reply_text(textoI)
        except:
            textoI = traducir(chatId,'Usuario no encontrado.\nTiene que introducir tu tag en el comando, ejemplo:')
            update.message.reply_text(textoI + '\n/registro 2Y0J28QY')
    else:
        chatIdChat = update.message.chat.id
        chatNombre = update.message.chat.title
        clanRegistro = saberSiTengoClanSpam(chatIdChat)
            
        if clanRegistro == 0:
            altaClan(chatIdChat,chatNombre)

        nombreBD = sacarNombreClan(chatIdChat)

        if nombreBD != chatNombre:
            cambioNombreClan(chatNombre,chatIdChat)

        texto0I = traducir(chatId,'Privado')
        texto1I = traducir(chatId,'El funcionamiento de este comando es por privado')
        keyboard = [[InlineKeyboardButton(texto0I + ' 🤖', url = 't.me/ClashRoyaleAPIBot')]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text(texto1I, reply_markup=reply_markup)

def supportedLanguages(update, context):
    tipo = update.message.chat.type
    alias = update.message.from_user.username
    chatId = update.message.from_user.id
    nuevoUsu = buscarContacto(chatId)
    
    if nuevoUsu == 0:
        altaContactos(chatId,alias)

    usoUsu(chatId)
    
    if tipo == 'private':
        languages = {'es': 'español','ca': 'catalán','gl': 'gallego','en': 'inglés','af': 'afrikaans','sq': 'albanian','am': 'amharic','ar': 'arabic','hy': 'armenian','az': 'azerbaijani','eu': 'basque','be': 'belarusian','bn': 'bengali','bs': 'bosnian','bg': 'bulgarian','ceb': 'cebuano','ny': 'chichewa','zh-cn': 'chinese (simplified)','zh-tw': 'chinese (traditional)','co': 'corsican','hr': 'croatian','cs': 'czech','da': 'danish','nl': 'dutch','eo': 'esperanto','et': 'estonian','tl': 'filipino','fi': 'finnish','fr': 'french','fy': 'frisian','ka': 'georgian','de': 'german','el': 'greek','gu': 'gujarati','ht': 'haitian creole','ha': 'hausa','haw': 'hawaiian','iw': 'hebrew','hi': 'hindi','hmn': 'hmong','hu': 'hungarian','is': 'icelandic','ig': 'igbo','id': 'indonesian','ga': 'irish','it': 'italian','ja': 'japanese','jw': 'javanese','kn': 'kannada','kk': 'kazakh','km': 'khmer','ko': 'korean','ku': 'kurdish (kurmanji)','ky': 'kyrgyz','lo': 'lao','la': 'latin','lv': 'latvian','lt': 'lithuanian','lb': 'luxembourgish','mk': 'macedonian','mg': 'malagasy','ms': 'malay','ml': 'malayalam','mt': 'maltese','mi': 'maori','mr': 'marathi','mn': 'mongolian','my': 'myanmar (burmese)','ne': 'nepali','no': 'norwegian','ps': 'pashto','fa': 'persian','pl': 'polish','pt': 'portuguese','pa': 'punjabi','ro': 'romanian','ru': 'russian','sm': 'samoan','gd': 'scots gaelic','sr': 'serbian','st': 'sesotho','sn': 'shona','sd': 'sindhi','si': 'sinhala','sk': 'slovak','sl': 'slovenian','so': 'somali','su': 'sundanese','sw': 'swahili','sv': 'swedish','tg': 'tajik','ta': 'tamil','te': 'telugu','th': 'thai','tr': 'turkish','uk': 'ukrainian','ur': 'urdu','uz': 'uzbek','vi': 'vietnamese','cy': 'welsh','xh': 'xhosa','yi': 'yiddish','yo': 'yoruba','zu': 'zulu','fil': 'Filipino','he': 'Hebrew'}
        respuesta = ''

        for abreviatura,idioma in languages.items():
            respuesta += abreviatura + ': ' + idioma + '\n'

        update.message.reply_text(respuesta)
    else:
        chatIdChat = update.message.chat.id
        chatNombre = update.message.chat.title
        clanRegistro = saberSiTengoClanSpam(chatIdChat)
            
        if clanRegistro == 0:
            altaClan(chatIdChat,chatNombre)

        nombreBD = sacarNombreClan(chatIdChat)

        if nombreBD != chatNombre:
            cambioNombreClan(chatNombre,chatIdChat)
            
        keyboard = [[InlineKeyboardButton('Privado 🤖', url = 't.me/ClashRoyaleAPIBot')]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text('El funcionamiento de este comando es por privado', reply_markup=reply_markup)

def es(update, context):
    tipo = update.message.chat.type
    alias = update.message.from_user.username
    chatId = update.message.from_user.id
    nuevoUsu = buscarContacto(chatId)
    
    if nuevoUsu == 0:
        altaContactos(chatId,alias)

    usoUsu(chatId)
    
    if tipo == 'private':
        try:
            con,cursor = conexionBDD()
            cursor.execute('UPDATE usuario SET idioma = "es" WHERE id = %s', chatId)
            con.commit()
            con.close()

            update.message.reply_text('Idioma cambiado a español.')
        except:
            update.message.reply_text('Usuario no encontrado.\nTiene que introducir tu tag en el comando, ejemplo:\n/registro 2Y0J28QY')
    else:
        chatIdChat = update.message.chat.id
        chatNombre = update.message.chat.title
        clanRegistro = saberSiTengoClanSpam(chatIdChat)
            
        if clanRegistro == 0:
            altaClan(chatIdChat,chatNombre)

        nombreBD = sacarNombreClan(chatIdChat)

        if nombreBD != chatNombre:
            cambioNombreClan(chatNombre,chatIdChat)

        keyboard = [[InlineKeyboardButton('Privado 🤖', url = 't.me/ClashRoyaleAPIBot')]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text('El funcionamiento de este comando es por privado', reply_markup=reply_markup)

def en(update, context):
    tipo = update.message.chat.type
    alias = update.message.from_user.username
    chatId = update.message.from_user.id
    nuevoUsu = buscarContacto(chatId)
    
    if nuevoUsu == 0:
        altaContactos(chatId,alias)

    usoUsu(chatId)
    
    if tipo == 'private':
        try:
            con,cursor = conexionBDD()
            cursor.execute('UPDATE usuario SET idioma = "en" WHERE id = %s', chatId)
            con.commit()
            con.close()

            update.message.reply_text('(BETA) Language changed to English.\nThe following translation is not exact, it is automatic and contains errors.')
        except:
            update.message.reply_text('User not found.\nYou have to enter your tag in the command, example:\n/registro 2Y0J28QY')
    else:
        chatIdChat = update.message.chat.id
        chatNombre = update.message.chat.title
        clanRegistro = saberSiTengoClanSpam(chatIdChat)
            
        if clanRegistro == 0:
            altaClan(chatIdChat,chatNombre)

        nombreBD = sacarNombreClan(chatIdChat)

        if nombreBD != chatNombre:
            cambioNombreClan(chatNombre,chatIdChat)
            
        keyboard = [[InlineKeyboardButton('Private 🤖', url = 't.me/ClashRoyaleAPIBot')]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text('The operation of the bot is by private', reply_markup=reply_markup)

def info(update, context):
    tipo = update.message.chat.type
    alias = update.message.from_user.username
    chatId = update.message.from_user.id
    nuevoUsu = buscarContacto(chatId)
    
    if nuevoUsu == 0:
        altaContactos(chatId,alias)

    usoUsu(chatId)
    
    if tipo == 'private':
        textoI = traducir(chatId,'''
Online desde mayo de 2020.
/start (Funcionamiento por privado)
    + Información del perfil: Muestra toda la información del usuario en el juego.
    + Siguientes cofres: Muestra los siguientes cofres que te van a tocar.
    + Oro para las cartas: Muestra el oro restante que te falta para subir tus cartas por diferentes tipos de calidad y el oro total.
    + Donaciones: Muestra lo que ha donado y le han donado. Ordenado por más donaciones realizadas y en caso de empate por donaciones recibidas.
    + Actividad en guerras: Muestra la participación del clan en las últimas 10 guerras.
    + Ranking en la guerra: Muestra la clasificación de los clanes en la guerra actual, ordenado por puntos y luego puntos de reparación.
    + Inactivos del clan: Muestra los jugadores inactivos con más de 7 días sin entrar al juego.
    + Miembros del clan: Muestra todos los miembros del clan. Ordenado por trofeos.

/registro (Funcionamiento por privado)
    - Registra el tag del usuario en el juego, si no se hace el registro no se puede dar la información.

/sinatacarenguerra (Funcionamiento por privado y en grupos)
    - Listado de los miembros del clan que están sin atacar en guerra, es decir, con 0 puntos y los que tienen menos de un 30% de puntos totales obtenidos por el clan en la guerra actual. La idea es que el bot mencione a los que están con ataques pendientes, la única manera que el bot mencione a la persona es que esté registrada /registro, si no, solo dirá el nombre sin mencionar.

/topdecks (Funcionamiento por privado y en grupos)
    - Muestra los mejores decks 1 vs 1 en ladder el día de hoy (mínimo 6000 trofeos).

/lang (Funcionamiento por privado)
    - (BETA) Cambia el idioma del bot. Todos los idiomas, excepto el español, no son exactos, es una traducción automática y contiene errores.
    - Todas las abreviaturas de los lenguajes soportados: /idiomasDisponibles

/info (Funcionamiento por privado)
    - Muestra la información del bot.
''')
        textoI = textoI + '\nhttps://t.me/clashRoyaleAPI'
        update.message.reply_text(textoI)
    else:
        chatIdChat = update.message.chat.id
        chatNombre = update.message.chat.title
        clanRegistro = saberSiTengoClanSpam(chatIdChat)
            
        if clanRegistro == 0:
            altaClan(chatIdChat,chatNombre)

        nombreBD = sacarNombreClan(chatIdChat)

        if nombreBD != chatNombre:
            cambioNombreClan(chatNombre,chatIdChat)

        texto0I = traducir(chatId,'Privado')
        texto1I = traducir(chatId,'El funcionamiento de este comando es por privado')
        keyboard = [[InlineKeyboardButton(texto0I + ' 🤖', url = 't.me/ClashRoyaleAPIBot')]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text(texto1I, reply_markup=reply_markup)

if __name__ == '__main__':
    main()