from googletrans import Translator
from db import *

def traducir(chatId,texto):
    idioma = saberIdioma(chatId)

    if idioma == 'es':
        return texto
    else:
        '''
        translator = Translator()
        miroIdioma = translator.detect(texto)

        try:
            respuesta = translator.translate(texto, src=miroIdioma.lang, dest=idioma)
        except:
            respuesta = translator.translate(texto, src='es', dest=idioma)

        respuesta = respuesta.text.replace('@ ', '@')
        respuesta = respuesta.replace(':', ': ')
        respuesta = respuesta.replace(':  ', ': ')
        '''
        if texto == 'Elige una opción:':
            respuesta = '⚠⚠⚠ Translation temporarily disabled, under maintenance. ⚠⚠⚠\n\n\n' + texto
        else:
            respuesta = texto

        return respuesta