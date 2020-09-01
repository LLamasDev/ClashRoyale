def atacaFuncion(alias,chatId,usuario):
    try:
        usuarioInfoJson = enlace(usuario,'info')
        clan = str(usuarioInfoJson['clan']['tag'])
        clan = clan.replace('#', '', 1)
        nameClan = str(usuarioInfoJson['clan']['name'])
        usuarioAtacaJson = enlace(clan,'clanWar')
        state = str(usuarioAtacaJson['state'])
        
        if state != 'notInWar':
            try:
                diccionario = {}
                numero = 0

                if state == 'collectionDay':
                    state = 'día de recolección'
                elif state == 'warDay':
                    state = 'guerra'

                respuesta = nameClan + ' en ' + state + '.\nAtaques que faltan:'

                while True:
                    try:
                        numberOfBattles = int(usuarioAtacaJson['participants'][numero]['numberOfBattles'])
                        battlesPlayed = int(usuarioAtacaJson['participants'][numero]['battlesPlayed'])

                        resultado = numberOfBattles - battlesPlayed

                        if resultado > 0:
                            name = str(usuarioAtacaJson['participants'][numero]['name'])
                            tag = str(usuarioAtacaJson['participants'][numero]['tag'])
                            tag = tag.replace('#', '', 1)
                            posibleNombre = sacarUsuarioConTag(tag)

                            if posibleNombre != None:
                                name += ' (@' + posibleNombre + ')'

                            diccionario[name] = resultado

                        numero += 1
                    except:
                        break
                    
                for nombre,falta in diccionario.items():
                    respuesta += '\n' + nombre + ' le faltan ' + str(falta)

                return respuesta
            except:
                return 'API caída'
        else:
            return 'No en guerra'
    except:
        return 'Sin clan'

def traducirIdioma(abreviaturaUsu):
    languages = {'es': 'español','ca': 'catalán','gl': 'gallego','en': 'inglés','af': 'afrikaans','sq': 'albanian','am': 'amharic','ar': 'arabic','hy': 'armenian','az': 'azerbaijani','eu': 'basque','be': 'belarusian','bn': 'bengali','bs': 'bosnian','bg': 'bulgarian','ceb': 'cebuano','ny': 'chichewa','zh-cn': 'chinese (simplified)','zh-tw': 'chinese (traditional)','co': 'corsican','hr': 'croatian','cs': 'czech','da': 'danish','nl': 'dutch','eo': 'esperanto','et': 'estonian','tl': 'filipino','fi': 'finnish','fr': 'french','fy': 'frisian','ka': 'georgian','de': 'german','el': 'greek','gu': 'gujarati','ht': 'haitian creole','ha': 'hausa','haw': 'hawaiian','iw': 'hebrew','hi': 'hindi','hmn': 'hmong','hu': 'hungarian','is': 'icelandic','ig': 'igbo','id': 'indonesian','ga': 'irish','it': 'italian','ja': 'japanese','jw': 'javanese','kn': 'kannada','kk': 'kazakh','km': 'khmer','ko': 'korean','ku': 'kurdish (kurmanji)','ky': 'kyrgyz','lo': 'lao','la': 'latin','lv': 'latvian','lt': 'lithuanian','lb': 'luxembourgish','mk': 'macedonian','mg': 'malagasy','ms': 'malay','ml': 'malayalam','mt': 'maltese','mi': 'maori','mr': 'marathi','mn': 'mongolian','my': 'myanmar (burmese)','ne': 'nepali','no': 'norwegian','ps': 'pashto','fa': 'persian','pl': 'polish','pt': 'portuguese','pa': 'punjabi','ro': 'romanian','ru': 'russian','sm': 'samoan','gd': 'scots gaelic','sr': 'serbian','st': 'sesotho','sn': 'shona','sd': 'sindhi','si': 'sinhala','sk': 'slovak','sl': 'slovenian','so': 'somali','su': 'sundanese','sw': 'swahili','sv': 'swedish','tg': 'tajik','ta': 'tamil','te': 'telugu','th': 'thai','tr': 'turkish','uk': 'ukrainian','ur': 'urdu','uz': 'uzbek','vi': 'vietnamese','cy': 'welsh','xh': 'xhosa','yi': 'yiddish','yo': 'yoruba','zu': 'zulu','fil': 'Filipino','he': 'Hebrew'}

    for abreviatura,idioma in languages.items():
        if abreviatura == abreviaturaUsu:
            return idioma