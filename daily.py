import pymysql
import requests
from db import *
from data import *

usoUsu(miID)
consulta = estadisticas()
consulta = consulta.replace('_', '\_')

peticion = 'https://api.telegram.org/bot' + TOKENINFO + '/sendMessage?chat_id=' + grupoPeticion + '&parse_mode=Markdown&text=' + consulta
requests.get(peticion)

con,cursor = conexionBDD()

try:
    cursor.execute('UPDATE clanes SET spam = "si"')
    con.commit()
    cursor.execute('UPDATE usuario SET usoHoy = "0"')
    con.commit()
except:
    con.rollback()

con.close()