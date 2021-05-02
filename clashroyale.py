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
from botoninfoclan import *
from botonguerras import *
from estadisticas import *
from botonperfil import *
from botoncofres import *
from botonguerra import *
from controloUsu import *
from translate import *
from botonclan import *
from enlaceapi import *
from botonoro import *
from data import *
from db import *

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def menuPrincipal(update, context):
    query = update.callback_query
    chatId = query.message.chat.id
    alias = query.message.chat.username

    controlUsu(chatId, alias)

    context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text='Elige una opción:', reply_markup=menuPrincipal_keyboard())

def menuPerfil(update, context):
    query = update.callback_query
    chatId = query.message.chat.id
    alias = query.message.chat.username

    controlUsu(chatId, alias)
    
    context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text='Elige una opción del perfil:', reply_markup=menuPerfil_keyboard())

def menuPerfilDatos(update, context):
    query = update.callback_query
    chatId = query.message.chat.id
    alias = query.message.chat.username

    controlUsu(chatId, alias)
    
    context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=perfil(chatId), reply_markup=menuPerfil_keyboard())

def menuPerfilCofres(update, context):
    query = update.callback_query
    chatId = query.message.chat.id
    alias = query.message.chat.username

    controlUsu(chatId, alias)
    
    context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=cofres(chatId), reply_markup=menuPerfil_keyboard())

def menuPerfilOro(update, context):
    query = update.callback_query
    chatId = query.message.chat.id
    alias = query.message.chat.username

    controlUsu(chatId, alias)
    
    context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=cartas(chatId), reply_markup=menuPerfil_keyboard())

def menuClan(update, context):
    query = update.callback_query
    chatId = query.message.chat.id
    alias = query.message.chat.username

    controlUsu(chatId, alias)
    
    context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text='Elige una opción del clan:', reply_markup=menuClan_keyboard())

def menuClanDatos(update, context):
    query = update.callback_query
    chatId = query.message.chat.id
    alias = query.message.chat.username

    controlUsu(chatId, alias)
    
    context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=clanInfo(chatId), reply_markup=menuClan_keyboard())

def menuClanMiembros(update, context):
    query = update.callback_query
    chatId = query.message.chat.id
    alias = query.message.chat.username

    controlUsu(chatId, alias)
    
    context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=clan(chatId), reply_markup=menuClan_keyboard())

def menuClanDonaciones(update, context):
    query = update.callback_query
    chatId = query.message.chat.id
    alias = query.message.chat.username

    controlUsu(chatId, alias)
    
    context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=donaciones(chatId), reply_markup=menuClan_keyboard())

def menuClanInactivos(update, context):
    query = update.callback_query
    chatId = query.message.chat.id
    alias = query.message.chat.username

    controlUsu(chatId, alias)
    
    context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=inactivos(chatId), reply_markup=menuClan_keyboard())

def menuGuerra(update, context):
    query = update.callback_query
    chatId = query.message.chat.id
    alias = query.message.chat.username

    controlUsu(chatId, alias)
    
    context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text='Elige una opción de la guerra:', reply_markup=menuGuerra_keyboard())

def menuGuerraActividad(update, context):
    query = update.callback_query
    chatId = query.message.chat.id
    alias = query.message.chat.username

    controlUsu(chatId, alias)
    
    context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=guerras(chatId), reply_markup=menuGuerra_keyboard())

def menuGuerraRanking(update, context):
    query = update.callback_query
    chatId = query.message.chat.id
    alias = query.message.chat.username

    controlUsu(chatId, alias)
    
    context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=guerra(chatId), reply_markup=menuGuerra_keyboard())

def menuPrincipal_keyboard():
    keyboard = [[InlineKeyboardButton('Perfil', callback_data='perfilMain')], [InlineKeyboardButton('Clan', callback_data='clanMain')], [InlineKeyboardButton('Guerra', callback_data='guerraMain')]]
                
    return InlineKeyboardMarkup(keyboard)

def menuPerfil_keyboard():
    keyboard = [[InlineKeyboardButton('Menú principal', callback_data='main')], [InlineKeyboardButton('Información del perfil', callback_data='pDatosUsu')], [InlineKeyboardButton('Siguientes cofres', callback_data='pCofres')], [InlineKeyboardButton('Oro restante para las cartas', callback_data='pOro')]]
                
    return InlineKeyboardMarkup(keyboard)

def menuClan_keyboard():
    keyboard = [[InlineKeyboardButton('Menú principal', callback_data='main')], [InlineKeyboardButton('Datos del clan', callback_data='cInfo')], [InlineKeyboardButton('Miembros del clan', callback_data='cMiembros')], [InlineKeyboardButton('Donaciones', callback_data='cDonaciones')], [InlineKeyboardButton('Inactivos del clan', callback_data='cInactivos')]]
                
    return InlineKeyboardMarkup(keyboard)

def menuGuerra_keyboard():
    keyboard = [[InlineKeyboardButton('Menú principal', callback_data='main')], [InlineKeyboardButton('Actividad en guerras', callback_data='cActividad')], [InlineKeyboardButton('Ranking en la guerra', callback_data='cRanking')]]
                
    return InlineKeyboardMarkup(keyboard)

def mensajePrivado():
    keyboard = [[InlineKeyboardButton('Privado 🤖', url = 't.me/ClashRoyaleAPIBot')]]
                
    return InlineKeyboardMarkup(keyboard)

def main():
    updater = Updater(TOKEN, use_context=True)
    ud = updater.dispatcher
    ud.add_handler(CommandHandler('start', start))
    ud.add_handler(CommandHandler('all', all))
    ud.add_handler(CommandHandler('yo', yo))
    ud.add_handler(CommandHandler('registro', register, pass_args=True))
    ud.add_handler(CommandHandler('sinatacarenguerra', ataca))
    ud.add_handler(CommandHandler('topdecks', topDecks))
    ud.add_handler(CommandHandler('lang', lang, pass_args=True))
    ud.add_handler(CommandHandler('idiomasDisponibles', supportedLanguages))
    ud.add_handler(CommandHandler('auto', auto))
    ud.add_handler(CommandHandler('es', es))
    ud.add_handler(CommandHandler('en', en))
    ud.add_handler(CommandHandler('info', info))
    ud.add_handler(CallbackQueryHandler(menuPrincipal, pattern='main'))
    ud.add_handler(CallbackQueryHandler(menuPerfil, pattern='perfilMain'))
    ud.add_handler(CallbackQueryHandler(menuPerfilDatos, pattern='pDatosUsu'))
    ud.add_handler(CallbackQueryHandler(menuPerfilCofres, pattern='pCofres'))
    ud.add_handler(CallbackQueryHandler(menuPerfilOro, pattern='pOro'))
    ud.add_handler(CallbackQueryHandler(menuClan, pattern='clanMain'))
    ud.add_handler(CallbackQueryHandler(menuClanDatos, pattern='cInfo'))
    ud.add_handler(CallbackQueryHandler(menuClanMiembros, pattern='cMiembros'))
    ud.add_handler(CallbackQueryHandler(menuClanDonaciones, pattern='cDonaciones'))
    ud.add_handler(CallbackQueryHandler(menuClanInactivos, pattern='cInactivos'))
    ud.add_handler(CallbackQueryHandler(menuGuerra, pattern='guerraMain'))
    ud.add_handler(CallbackQueryHandler(menuGuerraActividad, pattern='cActividad'))
    ud.add_handler(CallbackQueryHandler(menuGuerraRanking, pattern='cRanking'))
    updater.start_polling()
    updater.idle()

def all(update, context):
    chatId = update.message.from_user.id
    alias = update.message.from_user.username

    controlUsu(chatId, alias)

    if chatId == miID:
        update.message.reply_text(allEstadisticas())

def yo(update, context):
    chatId = update.message.from_user.id
    alias = update.message.from_user.username

    controlUsu(chatId, alias)

    if chatId == miID:
        update.message.reply_text(estadisticas())

def start(update, context):
    tipo = update.message.chat.type
    alias = update.message.from_user.username
    chatId = update.message.from_user.id
    
    controlUsu(chatId, alias)

    if tipo == 'private':
        update.message.reply_text('Elige una opción:', reply_markup=menuPrincipal_keyboard())
    else:
        chatIdChat = update.message.chat.id
        chatNombre = update.message.chat.title

        controlGrupo(chatIdChat, chatNombre)
        
        update.message.reply_text('El funcionamiento de este comando es por privado', reply_markup=mensajePrivado())

def register(update, context):
    tipo = update.message.chat.type
    alias = update.message.from_user.username
    chatId = update.message.from_user.id

    controlUsu(chatId, alias)
    
    if tipo == 'private':
        usuDice = ' '.join(context.args)

        try:
            primeraLetra = usuDice[0]

            if primeraLetra == '#':
                usuDice = usuDice.replace('#', '', 1)

            usuarioInfoJson = enlace(usuDice,'info')
            nombre = str(usuarioInfoJson['name'])
            registroTag(chatId, usuDice)

            textoI = traducir(chatId,'Registrado con el nombre de usuario: ')
            update.message.reply_text(textoI + nombre + ' #' + usuDice)
        except:
            textoI = traducir(chatId,'Usuario no encontrado.\nTiene que introducir tu tag en el comando, ejemplo:')
            update.message.reply_text(textoI + '\n/registro 2Y0J28QY')
    else:
        chatIdChat = update.message.chat.id
        chatNombre = update.message.chat.title

        controlGrupo(chatIdChat, chatNombre)

        update.message.reply_text('El funcionamiento de este comando es por privado', reply_markup=mensajePrivado())

def ataca(update, context):
    alias = update.message.from_user.username
    chatId = update.message.from_user.id
    tipo = update.message.chat.type

    controlUsu(chatId, alias)
    usuario = sacarTag(chatId)

    if tipo != 'private':
        chatIdChat = update.message.chat.id
        chatNombre = update.message.chat.title

        controlGrupo(chatIdChat, chatNombre)
        clanSpam = saberClanSpam(chatIdChat)

        if clanSpam == 'si':
            if usuario != 'None':
                textoFuncion = atacaFuncion(alias, chatId, usuario)
                textoI = traducir(chatId, textoFuncion)
                update.message.reply_text(textoI)

                cambioSpam(chatIdChat)
            else:
                texto0I = traducir(chatId, 'Privado')
                texto1I = traducir(chatId, 'Usuario no registrado, no puedo darte información de tu clan si no tengo tu información.\nTiene que introducir tu tag en el comando por privado, ejemplo:')
                keyboard = [[InlineKeyboardButton(texto0I + ' 🤖', url = 't.me/ClashRoyaleAPIBot')]]
                reply_markup = InlineKeyboardMarkup(keyboard)

                update.message.reply_text(texto1I + '\n/registro 2Y0J28QY', reply_markup=reply_markup)
        else:
            texto0I = traducir(chatId, 'Privado')
            texto1I = traducir(chatId, 'Hasta las 00:00 no se puede volver a usar el comando, para evitar mencionar más de una vez, si quieres ver los que faltan, usa el comando por privado.')
            keyboard = [[InlineKeyboardButton(texto0I + ' 🤖', url = 't.me/ClashRoyaleAPIBot')]]
            reply_markup = InlineKeyboardMarkup(keyboard)

            update.message.reply_text(texto1I, reply_markup=reply_markup)
    else:
        textoFuncion = atacaFuncion(alias, chatId, usuario)
        textoI = traducir(chatId, textoFuncion)
        update.message.reply_text(textoI)

def topDecks(update, context):
    alias = update.message.from_user.username
    chatId = update.message.from_user.id
    tipo = update.message.chat.type
    
    controlUsu(chatId, alias)

    if tipo != 'private':
        chatIdChat = update.message.chat.id
        chatNombre = update.message.chat.title

        controlGrupo(chatIdChat, chatNombre)

    respuesta = sacoTopDecks()

    update.message.reply_text(respuesta, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

def lang(update, context):
    tipo = update.message.chat.type
    alias = update.message.from_user.username
    chatId = update.message.from_user.id
    
    controlUsu(chatId, alias)
    
    if tipo == 'private':
        try:
            usuDice = ' '.join(context.args)

            if len(usuDice) > 0:
                idiomas = traducirIdioma(usuDice)

                if idiomas != None:
                    cambioIdioma(chatId, usuDice)

                    idiomasI = traducir(chatId,idiomas)
                    texto = '⚠⚠⚠ Translation temporarily disabled, under maintenance. ⚠⚠⚠\n\n\n(BETA) Idioma cambiado a ' + idiomasI + '. La siguiente traducción no es exacta, es automática y contiene errores.'
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

        controlGrupo(chatIdChat, chatNombre)

        update.message.reply_text('El funcionamiento de este comando es por privado', reply_markup=mensajePrivado())

def auto(update, context):
    tipo = update.message.chat.type
    alias = update.message.from_user.username
    chatId = update.message.from_user.id
    
    controlUsu(chatId, alias)
    
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
                cambioIdioma(chatId, idiomaUsu)

                idiomasI = traducir(chatId,idiomas)
                texto = '⚠⚠⚠ Translation temporarily disabled, under maintenance. ⚠⚠⚠\n\n\n(BETA) Idioma cambiado a ' + idiomasI + '. La siguiente traducción no es exacta, es automática y contiene errores.'
                textoI = traducir(chatId,texto)
                update.message.reply_text(textoI)
        except:
            textoI = traducir(chatId,'Usuario no encontrado.\nTiene que introducir tu tag en el comando, ejemplo:')
            update.message.reply_text(textoI + '\n/registro 2Y0J28QY')
    else:
        chatIdChat = update.message.chat.id
        chatNombre = update.message.chat.title

        controlGrupo(chatIdChat, chatNombre)

        update.message.reply_text('El funcionamiento de este comando es por privado', reply_markup=mensajePrivado())

def supportedLanguages(update, context):
    tipo = update.message.chat.type
    alias = update.message.from_user.username
    chatId = update.message.from_user.id
    
    controlUsu(chatId, alias)
    
    if tipo == 'private':
        languages = {'es': 'español','ca': 'catalán','gl': 'gallego','en': 'inglés','af': 'afrikaans','sq': 'albanian','am': 'amharic','ar': 'arabic','hy': 'armenian','az': 'azerbaijani','eu': 'basque','be': 'belarusian','bn': 'bengali','bs': 'bosnian','bg': 'bulgarian','ceb': 'cebuano','ny': 'chichewa','zh-cn': 'chinese (simplified)','zh-tw': 'chinese (traditional)','co': 'corsican','hr': 'croatian','cs': 'czech','da': 'danish','nl': 'dutch','eo': 'esperanto','et': 'estonian','tl': 'filipino','fi': 'finnish','fr': 'french','fy': 'frisian','ka': 'georgian','de': 'german','el': 'greek','gu': 'gujarati','ht': 'haitian creole','ha': 'hausa','haw': 'hawaiian','iw': 'hebrew','hi': 'hindi','hmn': 'hmong','hu': 'hungarian','is': 'icelandic','ig': 'igbo','id': 'indonesian','ga': 'irish','it': 'italian','ja': 'japanese','jw': 'javanese','kn': 'kannada','kk': 'kazakh','km': 'khmer','ko': 'korean','ku': 'kurdish (kurmanji)','ky': 'kyrgyz','lo': 'lao','la': 'latin','lv': 'latvian','lt': 'lithuanian','lb': 'luxembourgish','mk': 'macedonian','mg': 'malagasy','ms': 'malay','ml': 'malayalam','mt': 'maltese','mi': 'maori','mr': 'marathi','mn': 'mongolian','my': 'myanmar (burmese)','ne': 'nepali','no': 'norwegian','ps': 'pashto','fa': 'persian','pl': 'polish','pt': 'portuguese','pa': 'punjabi','ro': 'romanian','ru': 'russian','sm': 'samoan','gd': 'scots gaelic','sr': 'serbian','st': 'sesotho','sn': 'shona','sd': 'sindhi','si': 'sinhala','sk': 'slovak','sl': 'slovenian','so': 'somali','su': 'sundanese','sw': 'swahili','sv': 'swedish','tg': 'tajik','ta': 'tamil','te': 'telugu','th': 'thai','tr': 'turkish','uk': 'ukrainian','ur': 'urdu','uz': 'uzbek','vi': 'vietnamese','cy': 'welsh','xh': 'xhosa','yi': 'yiddish','yo': 'yoruba','zu': 'zulu','fil': 'Filipino','he': 'Hebrew'}
        respuesta = ''

        for abreviatura, idioma in languages.items():
            respuesta += abreviatura + ': ' + idioma + '\n'

        update.message.reply_text(respuesta)
    else:
        chatIdChat = update.message.chat.id
        chatNombre = update.message.chat.title

        controlGrupo(chatIdChat, chatNombre)

        update.message.reply_text('El funcionamiento de este comando es por privado', reply_markup=mensajePrivado())

def es(update, context):
    tipo = update.message.chat.type
    alias = update.message.from_user.username
    chatId = update.message.from_user.id
    
    controlUsu(chatId, alias)
    
    if tipo == 'private':
        try:
            cambioIdioma(chatId, "es")

            update.message.reply_text('Idioma cambiado a español.')
        except:
            update.message.reply_text('Usuario no encontrado.\nTiene que introducir tu tag en el comando, ejemplo:\n/registro 2Y0J28QY')
    else:
        chatIdChat = update.message.chat.id
        chatNombre = update.message.chat.title

        controlGrupo(chatIdChat, chatNombre)

        update.message.reply_text('El funcionamiento de este comando es por privado', reply_markup=mensajePrivado())

def en(update, context):
    tipo = update.message.chat.type
    alias = update.message.from_user.username
    chatId = update.message.from_user.id
    
    controlUsu(chatId, alias)
    
    if tipo == 'private':
        try:
            cambioIdioma(chatId, "en")

            update.message.reply_text('⚠⚠⚠ Translation temporarily disabled, under maintenance. ⚠⚠⚠\n\n\n(BETA) Language changed to English.\nThe following translation is not exact, it is automatic and contains errors.')
        except:
            update.message.reply_text('User not found.\nYou have to enter your tag in the command, example:\n/registro 2Y0J28QY')
    else:
        chatIdChat = update.message.chat.id
        chatNombre = update.message.chat.title

        controlGrupo(chatIdChat, chatNombre)

        update.message.reply_text('El funcionamiento de este comando es por privado', reply_markup=mensajePrivado())

def info(update, context):
    tipo = update.message.chat.type
    alias = update.message.from_user.username
    chatId = update.message.from_user.id
    
    controlUsu(chatId, alias)
    
    if tipo == 'private':
        textoI = traducir(chatId,'''
Online desde mayo de 2020.
/start (Funcionamiento por privado)
    - Perfil:
       + Información del perfil: Muestra toda la información del usuario en el juego.
       + Siguientes cofres: Muestra los siguientes cofres que te van a tocar.
       + Oro restante para las cartas: Muestra el oro restante que te falta para subir tus cartas por diferentes tipos de calidad y el oro total.
    - Clan:
       + Datos del clan: Muestra la información del clan.
       + Miembros del clan: Muestra todos los miembros del clan. Ordenado por trofeos.
       + Donaciones: Muestra lo que ha donado y le han donado. Ordenado por más donaciones realizadas y en caso de empate por donaciones recibidas.
       + Inactivos del clan: Muestra los jugadores inactivos con más de 7 días sin entrar al juego.
    - Guerra:
       + Actividad en guerras: Muestra la participación del clan en las últimas 5 guerras, ordenado por puntos y luego puntos de reparación en caso de empate, solo se mostrarán los 50 mejores por el límite del tamaño del mensaje que deja mandar telegram.
       + Ranking en la guerra: Muestra la clasificación de los clanes en la guerra actual, ordenado por puntos y luego puntos de reparación en caso de empate.

/registro (Funcionamiento por privado)
    - Registra el tag del usuario en el juego, si no se hace el registro no se puede dar la información.

/sinatacarenguerra (Funcionamiento por privado y en grupos)
    - Listado de los miembros del clan que están sin atacar en guerra, es decir, con 0 puntos y los que tienen menos de un 30% de puntos totales obtenidos por cada miembro en la guerra actual, ordenado por puntos y luego puntos de reparación en caso de empate. La idea es que el bot mencione a los que están con ataques pendientes, la única manera que el bot mencione a la persona es que esté registrada /registro, si no, solo dirá el nombre sin mencionar.

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

        controlGrupo(chatIdChat, chatNombre)

        update.message.reply_text('El funcionamiento de este comando es por privado', reply_markup=mensajePrivado())

if __name__ == '__main__':
    main()