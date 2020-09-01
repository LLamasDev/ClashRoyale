import pymysql
from data import *
from enlaceapi import *
from funcionesrepes import *

def usoUsu(chatId):
    con,cursor = conexionBDD()
    cursor.execute('SELECT usoHoy FROM usuario WHERE id = %s', chatId)
    contadorHoy = cursor.fetchall()[0][0]
    cursor.execute('SELECT usoTotal FROM usuario WHERE id = %s', chatId)
    contadorTotal = cursor.fetchall()[0][0]
    cursor.execute('UPDATE usuario SET usoHoy = %s, usoTotal = %s WHERE id = %s', (contadorHoy+1,contadorTotal+1,chatId))
    con.commit()
    cursor.close()

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

def sacarUsuarioConTag(tag):
    con,cursor = conexionBDD()
    cursor.execute('SELECT alias FROM usuario WHERE tag = %s', tag)

    try:
        respuesta = cursor.fetchall()[0][0]
    except:
        respuesta = None

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

def saberSiTengoClanSpam(chatId):
    con,cursor = conexionBDD()
    cursor.execute('SELECT count(*) FROM clanes WHERE id = %s', chatId)
    respuesta = cursor.fetchone()[0]
    cursor.close()

    return respuesta

def saberClanSpam(chatId):
    con,cursor = conexionBDD()
    cursor.execute('SELECT spam FROM clanes WHERE id = %s', chatId)
    respuesta = cursor.fetchone()[0]
    cursor.close()

    return respuesta

def sacarNombreClan(chatId):
    con,cursor = conexionBDD()
    cursor.execute('SELECT nombre FROM clanes WHERE id = %s', chatId)
    respuesta = cursor.fetchall()[0][0]
    cursor.close()

    return respuesta

def altaClan(chatId,nombre):
    con,cursor = conexionBDD()
    cursor.execute('INSERT INTO clanes (id,nombre) VALUES (%s, %s)', (chatId,nombre))
    con.commit()
    con.close()

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

def cambioSpam(chatId):
    con,cursor = conexionBDD()
    cursor.execute('UPDATE clanes SET spam = "no" WHERE id = %s', chatId)
    con.commit()
    con.close()

def cambioNombreClan(nombre,chatId):
    con,cursor = conexionBDD()
    cursor.execute('UPDATE clanes SET nombre = %s WHERE id = %s', (nombre,chatId))
    con.commit()
    con.close()

def estadisticas():
    con,cursor = conexionBDD()
    cursor.execute('SELECT count(*) FROM usuario')
    contadorTotal = cursor.fetchone()[0]
    cursor.execute('SELECT count(*) FROM usuario WHERE NOT tag = "None"')
    contadorRegistrado = cursor.fetchone()[0]
    cursor.execute('SELECT count(*) FROM clanes')
    contadorGrupos = cursor.fetchone()[0]
    cursor.execute('SELECT idioma, COUNT(*) FROM usuario GROUP BY idioma ORDER BY COUNT(*) DESC')
    contadorIdiomas = ''

    for idioma in cursor:
        contadorIdiomas += '\t - ' + str(traducirIdioma(idioma[0])) + ': ' + str(idioma[1]) + '\n'

    cursor.execute('SELECT sum(usoHoy) FROM usuario')
    contadorUsoHoy = cursor.fetchone()[0]
    cursor.execute('SELECT sum(usoTotal) FROM usuario')
    contadorUsoTotal = cursor.fetchone()[0]
    cursor.execute('SELECT sum(usoHoy) FROM usuario WHERE id != %s', miID)
    contadorUsoHoySM = cursor.fetchone()[0]
    cursor.execute('SELECT sum(usoTotal) FROM usuario WHERE id != %s', miID)
    contadorUsoTotalSM = cursor.fetchone()[0]
    cursor.execute('SELECT alias,usoHoy FROM usuario WHERE usoHoy > 0 ORDER BY usoHoy DESC LIMIT 9')
    contadorTopHoy = ''
    contadorH = 1

    for usuario,contador in cursor:
        contadorTopHoy += '\t' + str(contadorH) + ' - @' + str(usuario) + ': ' + str(contador) + '\n'
        contadorH += 1

    cursor.execute('SELECT alias,usoTotal FROM usuario ORDER BY usoTotal DESC LIMIT 9')
    contadorTopTotal = ''
    contadorT = 1

    for usuario,contador in cursor:
        contadorTopTotal += '\t' + str(contadorT) + ' - @' + str(usuario) + ': ' + str(contador) + '\n'
        contadorT += 1

    cursor.close()

    consulta = 'Estadísticas @ClashRoyaleAPIBot:\n\t - Usuarios que han usado el bot: ' + str(contadorTotal) + '\n\t - Usuarios registrados: ' + str(contadorRegistrado) + '\n\t - Grupos que han usado el bot: ' + str(contadorGrupos) + '\n\nIdiomas en uso:\n' + contadorIdiomas + '\nComandos usados:\n\t - Hoy: ' + str(contadorUsoHoy) + '\n\t - Total: ' + str(contadorUsoTotal) + '\n\nComandos no mios:\n\t - Hoy: ' + str(contadorUsoHoySM) + '\n\t - Total: ' + str(contadorUsoTotalSM) + '\n\nTop 9 usuarios de hoy (' + str(contadorUsoHoy) + '):\n' + str(contadorTopHoy) + '\nTop 9 usuarios (' + str(contadorUsoTotal) + '):\n' + str(contadorTopTotal)

    return consulta