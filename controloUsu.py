import pymysql
from data import *

def controlUsu(chatId, alias):
    respuestaUsu = buscarUsuario(chatId)

    if respuestaUsu == 0:
        insertoUsuario(chatId, alias)
    else:
        buscarAlias(chatId, alias)

    usoUsu(chatId)

def controlGrupo(chatIdChat, chatNombre):
    respuestaClan = buscarClan(chatIdChat)

    if respuestaClan == 0:
        insertoClan(chatIdChat, chatNombre)
    else:
        buscarNombreClan(chatIdChat, chatNombre)

def usoUsu(chatId):
    con, cursor = conexionBDD()

    try:
        cursor.execute('SELECT usoHoy, usoTotal FROM usuario WHERE id = %s', chatId)
        contadorHoy, contadorTotal = cursor.fetchone()
        cursor.execute('UPDATE usuario SET usoHoy = %s, usoTotal = %s WHERE id = %s', (contadorHoy+1, contadorTotal+1, chatId))
        con.commit()
    except:
        con.rollback()

    con.close()
    cursor.close()

# SELECT *********************************************************************************
def buscarUsuario(chatId):
    con, cursor = conexionBDD()

    try:
        cursor.execute('SELECT count(id) FROM usuario WHERE id = %s', chatId)
        resultadoBusqueda = cursor.fetchone()[0]
    except:
        con.rollback()
        
    con.close()
    cursor.close()

    return resultadoBusqueda

def buscarAlias(chatId, alias):
    con, cursor = conexionBDD()

    try:
        cursor.execute('SELECT alias FROM usuario WHERE id = %s', chatId)
        resultadoBusqueda = cursor.fetchone()[0]
    except:
        con.rollback()

    con.close()
    cursor.close()

    if alias != resultadoBusqueda:
        cambioAlias(chatId, alias)

def buscarClan(chatIdChat):
    con, cursor = conexionBDD()

    try:
        cursor.execute('SELECT count(nombre) FROM clanes WHERE id = %s', chatIdChat)
        resultadoBusqueda = cursor.fetchone()[0]
    except:
        con.rollback()

    con.close()
    cursor.close()

    return resultadoBusqueda

def buscarNombreClan(chatIdChat, chatNombre):
    con, cursor = conexionBDD()

    try:
        cursor.execute('SELECT nombre FROM clanes WHERE id = %s', chatIdChat)
        resultadoBusqueda = cursor.fetchone()[0]
    except:
        con.rollback()

    con.close()
    cursor.close()

    if chatNombre != resultadoBusqueda:
        cambioNombreClan(chatIdChat, chatNombre)

# INSERT *********************************************************************************
def insertoUsuario(chatId, alias):
    con, cursor = conexionBDD()

    try:
        cursor.execute('INSERT INTO usuario (id, alias) VALUES (%s, %s)', (chatId, alias))
        con.commit()
    except:
        con.rollback()

    con.close()
    cursor.close()

def insertoClan(chatIdChat, chatNombre):
    con, cursor = conexionBDD()

    try:
        cursor.execute('INSERT INTO clanes (id, nombre) VALUES (%s, %s)', (chatIdChat, chatNombre))
        con.commit()
    except:
        con.rollback()

    con.close()
    cursor.close()

# UPDATE *********************************************************************************
def cambioAlias(chatId, alias):
    con, cursor = conexionBDD()

    try:
        cursor.execute('UPDATE usuario SET alias = %s WHERE id = %s', (alias, chatId))
        con.commit()
    except:
        con.rollback()

    con.close()
    cursor.close()

def cambioNombreClan(chatIdChat, chatNombre):
    con, cursor = conexionBDD()

    try:
        cursor.execute('UPDATE clanes SET nombre = %s WHERE id = %s', (chatNombre, chatIdChat))
        con.commit()
    except:
        con.rollback()

    con.close()
    cursor.close()