import pymysql
from data import *
from enlaceapi import *

def sacarTag(chatId):
    con, cursor = conexionBDD()

    try:
        cursor.execute('SELECT tag FROM usuario WHERE id = %s', chatId)
        respuesta = cursor.fetchone()[0]
    except:
        con.rollback()

    con.close()
    cursor.close()

    return respuesta

def sacarUsuarioConTag(tag):
    con, cursor = conexionBDD()
    
    cursor.execute('SELECT alias FROM usuario WHERE tag = %s', tag)

    try:
        respuesta = cursor.fetchone()[0]
    except:
        respuesta = None

    con.close()
    cursor.close()

    return respuesta

def saberIdioma(chatId):
    con, cursor = conexionBDD()

    try:
        cursor.execute('SELECT idioma FROM usuario WHERE id = %s', chatId)
        respuesta = cursor.fetchone()[0]
    except:
        con.rollback()

    con.close()
    cursor.close()

    return respuesta

def saberClanSpam(chatId):
    con, cursor = conexionBDD()

    try:
        cursor.execute('SELECT spam FROM clanes WHERE id = %s', chatId)
        respuesta = cursor.fetchone()[0]
    except:
        con.rollback()

    con.close()
    cursor.close()

    return respuesta

def cambioSpam(chatId):
    con, cursor = conexionBDD()

    try:
        cursor.execute('UPDATE clanes SET spam = "no" WHERE id = %s', chatId)
        con.commit()
    except:
        con.rollback()

    con.close()
    cursor.close()

def cambioIdioma(chatId, usuDice):
    con, cursor = conexionBDD()

    try:
        cursor.execute('UPDATE usuario SET idioma = %s WHERE id = %s', (usuDice, chatId))
        con.commit()
    except:
        con.rollback()

    con.close()
    cursor.close()

def registroTag(chatId, usuDice):
    con, cursor = conexionBDD()

    try:
        cursor.execute('UPDATE usuario SET tag = %s WHERE id = %s', (usuDice, chatId))
        con.commit()
    except:
        con.rollback()

    con.close()
    cursor.close()