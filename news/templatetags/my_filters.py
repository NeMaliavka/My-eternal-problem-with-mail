from django import template

register = template.Library()
#CENSORED_WORDS = []
CENSORED_WORDS = ['редиска', 'сосиска']
# try:
#     file = open('bad_words.txt', 'r')
# except FileNotFoundError:
#     file = ''
#
# for word in file:
#     CENSORED_WORDS.append(word.lower())
#
# file.close()

@register.filter()
def censor(value):
    if not isinstance(value, str):
        raise ValueError('Фильтр применяется только к строкам')
    value = value.lower()
    for word in CENSORED_WORDS:
        if word in value:
            value = value.replace(word, '*'*len(word))
    return value

