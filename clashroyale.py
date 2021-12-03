#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
import requests
import urllib.request
from datetime import date
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from boton_perfil_info import *
from boton_perfil_cofres import *
from boton_perfil_oro import *
from boton_clan_info import *
from boton_clan_miembros import *
from boton_clan_donaciones import *
from boton_clan_inactivos import *
from boton_guerra_ranking import *
from boton_guerra_actividad import *
from controloUsu import *
from enlaceapi import *
from funcionesrepes import *
from estadisticas import *
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

            update.message.reply_text('Registrado con el nombre de usuario: ' + nombre + ' #' + usuDice)
        except:
            update.message.reply_text('Usuario no encontrado.\nTiene que introducir tu tag en el comando, ejemplo:\n/registro 2Y0J28QY')
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

                update.message.reply_text(textoFuncion)

                cambioSpam(chatIdChat)
            else:
                keyboard = [[InlineKeyboardButton('Privado 🤖', url = 't.me/ClashRoyaleAPIBot')]]
                reply_markup = InlineKeyboardMarkup(keyboard)

                update.message.reply_text('Usuario no registrado, no puedo darte información de tu clan si no tengo tu información.\nTiene que introducir tu tag en el comando por privado, ejemplo:\n/registro 2Y0J28QY', reply_markup=reply_markup)
        else:
            keyboard = [[InlineKeyboardButton('Privado 🤖', url = 't.me/ClashRoyaleAPIBot')]]
            reply_markup = InlineKeyboardMarkup(keyboard)

            update.message.reply_text('Hasta las 00:00 no se puede volver a usar el comando, para evitar mencionar más de una vez, si quieres ver los que faltan, usa el comando por privado.', reply_markup=reply_markup)
    else:
        textoFuncion = atacaFuncion(alias, chatId, usuario)

        update.message.reply_text(textoFuncion)

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

def info(update, context):
    alias = update.message.from_user.username
    chatId = update.message.from_user.id

    controlUsu(chatId, alias)

    texto = '''
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
       + Actividad en guerras: Muestra la participación del clan en las últimas 5 guerras, ordenado por puntos y luego ataques en guerra en caso de empate, solo se mostrarán los 20 mejores.
       + Ranking en la guerra: Muestra la clasificación de los clanes en la guerra actual, ordenado por puntos y luego puntos de reparación en caso de empate.

/registro (Funcionamiento por privado)
    - Registra el tag del usuario en el juego, si no se hace el registro no se puede dar la información.

/sinatacarenguerra (Funcionamiento por privado y en grupos)
    - Listado de los miembros del clan que están sin atacar en guerra, es decir, que no ha realizado los 4 ataques en la guerra actual, ordenado por los ataques del día de hoy y luego por los ataques totales en la guerra en caso de empate siempre de menos a más. La idea es que el bot mencione a los que están con ataques pendientes, la única manera que el bot mencione a la persona es que esté registrada /registro, si no, solo dirá el nombre sin mencionar.

/topdecks (Funcionamiento por privado y en grupos)
    - Muestra los mejores decks 1 vs 1 en ladder el día de hoy (mínimo 6000 trofeos).

/info (Funcionamiento por privado y en grupos)
    - Muestra la información del bot.

Toda la familia de bots Clash de Supercell:
 - @ClashOfClansAPIBot (Beta)
 - @ClashRoyaleAPIBot

https://t.me/clashRoyaleAPI
'''

    update.message.reply_text(texto)

if __name__ == '__main__':
    main()
