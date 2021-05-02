import pymysql
import requests
from data import *
from controloUsu import *
from estadisticas import *

def main():
    controlUsu(miID, miAlias)
    consultaTodo = estadisticas()
    # consulta = consultaTodo.replace('_', '\_')
    
    # peticion = 'https://api.telegram.org/bot' + TOKENINFO + '/sendMessage?chat_id=' + grupoPeticion + '&parse_mode=Markdown&text=' + consulta
    # requests.get(peticion)
    
    con, cursor = conexionBDD()
    
    try:
        cursor.execute('UPDATE clanes SET spam = "si" WHERE spam = "no"')
        con.commit()
        cursor.execute('UPDATE usuario SET usoHoy = "0" WHERE usoHoy != "0"')
        con.commit()
    except:
        con.rollback()
    
    con.close()
    cursor.close()
    
    try:
        f = open('/bot/daily.txt','w+')
    except FileNotFoundError:
        print('Archivo no existe')
        exit()
    except PermissionError:
        print('No se tienen permisos para leer el archivo')
        exit()
    
    consultaTodo = consultaTodo + '\n\n'
    f.write(consultaTodo)
    f.close()

if __name__ == "__main__":
    main()