import pymysql
from data import *

def estadisticas():
    con, cursor = conexionBDD()

    try:
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
        cursor.execute('SELECT alias, usoHoy FROM usuario WHERE usoHoy > 0 ORDER BY usoHoy DESC LIMIT 9')
        contadorTopHoy = ''
        contadorH = 1

        for usuario,contador in cursor:
            contadorTopHoy += '\t' + str(contadorH) + ' - @' + str(usuario) + ': ' + str(contador) + '\n'
            contadorH += 1

        cursor.execute('SELECT alias, usoTotal FROM usuario ORDER BY usoTotal DESC LIMIT 9')
        contadorTopTotal = ''
        contadorT = 1

        for usuario,contador in cursor:
            contadorTopTotal += '\t' + str(contadorT) + ' - @' + str(usuario) + ': ' + str(contador) + '\n'
            contadorT += 1
    except:
        con.rollback()

    con.close()
    cursor.close()

    consulta = 'Estadísticas @ClashRoyaleAPIBot:\n\t - Usuarios que han usado el bot: ' + str(contadorTotal) + '\n\t - Usuarios registrados: ' + str(contadorRegistrado) + '\n\t - Grupos que han usado el bot: ' + str(contadorGrupos) + '\n\nIdiomas en uso:\n' + contadorIdiomas + '\nComandos usados:\n\t - Hoy: ' + str(contadorUsoHoy) + '\n\t - Total: ' + str(contadorUsoTotal) + '\n\nTop 9 usuarios de hoy (' + str(contadorUsoHoy) + '):\n' + str(contadorTopHoy) + '\nTop 9 usuarios (' + str(contadorUsoTotal) + '):\n' + str(contadorTopTotal)

    return consulta

def allEstadisticas():
    con, cursor = conexionBDD()

    try:
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
    except:
        con.rollback()

    con.close()
    cursor.close()

    resultado = 'Estadísticas @ClashRoyaleAPIBot:\n\t - Usuarios que han usado el bot: ' + str(contadorTotal) + '\n\t - Grupos que han usado el bot: ' + str(contadorGrupos) + '\n\nComandos usados:\n\t - Hoy: ' + str(contadorUsoHoy) + '\n\t - Total: ' + str(contadorUsoTotal) + '\n\nIdiomas en uso:\n' + contadorIdiomas
    
    return resultado

def traducirIdioma(abreviaturaUsu):
    languages = {'es': 'español','ca': 'catalán','gl': 'gallego','en': 'inglés','af': 'afrikaans','sq': 'albanian','am': 'amharic','ar': 'arabic','hy': 'armenian','az': 'azerbaijani','eu': 'basque','be': 'belarusian','bn': 'bengali','bs': 'bosnian','bg': 'bulgarian','ceb': 'cebuano','ny': 'chichewa','zh-cn': 'chinese (simplified)','zh-tw': 'chinese (traditional)','co': 'corsican','hr': 'croatian','cs': 'czech','da': 'danish','nl': 'dutch','eo': 'esperanto','et': 'estonian','tl': 'filipino','fi': 'finnish','fr': 'french','fy': 'frisian','ka': 'georgian','de': 'german','el': 'greek','gu': 'gujarati','ht': 'haitian creole','ha': 'hausa','haw': 'hawaiian','iw': 'hebrew','hi': 'hindi','hmn': 'hmong','hu': 'hungarian','is': 'icelandic','ig': 'igbo','id': 'indonesian','ga': 'irish','it': 'italian','ja': 'japanese','jw': 'javanese','kn': 'kannada','kk': 'kazakh','km': 'khmer','ko': 'korean','ku': 'kurdish (kurmanji)','ky': 'kyrgyz','lo': 'lao','la': 'latin','lv': 'latvian','lt': 'lithuanian','lb': 'luxembourgish','mk': 'macedonian','mg': 'malagasy','ms': 'malay','ml': 'malayalam','mt': 'maltese','mi': 'maori','mr': 'marathi','mn': 'mongolian','my': 'myanmar (burmese)','ne': 'nepali','no': 'norwegian','ps': 'pashto','fa': 'persian','pl': 'polish','pt': 'portuguese','pa': 'punjabi','ro': 'romanian','ru': 'russian','sm': 'samoan','gd': 'scots gaelic','sr': 'serbian','st': 'sesotho','sn': 'shona','sd': 'sindhi','si': 'sinhala','sk': 'slovak','sl': 'slovenian','so': 'somali','su': 'sundanese','sw': 'swahili','sv': 'swedish','tg': 'tajik','ta': 'tamil','te': 'telugu','th': 'thai','tr': 'turkish','uk': 'ukrainian','ur': 'urdu','uz': 'uzbek','vi': 'vietnamese','cy': 'welsh','xh': 'xhosa','yi': 'yiddish','yo': 'yoruba','zu': 'zulu','fil': 'Filipino','he': 'Hebrew'}

    for abreviatura, idioma in languages.items():
        if abreviatura == abreviaturaUsu:
            return idioma