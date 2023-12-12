bad_words_list = [
    'loco',
    'tonto',
    'mierda',
    'cabron',
    'puta',

]

def contiene_palabra_inapropiada(comentario_texto):
    for bad_word in bad_words_list:
        if bad_word.lower() in comentario_texto.lower():
            return True
    return False
