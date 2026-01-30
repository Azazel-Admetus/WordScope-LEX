# importando bibliotecas
from langdetect import detect
from deep_translator import GoogleTranslator
# input do usuário
texto = input("Digite algo: ")
# função para traduzir texto
def traduzirtext(texto, destino="pt"):
    traducao = GoogleTranslator(source='auto', target=destino).translate(texto)

    return traducao
# função para identificar idioma
def identificarlang(texto):
    idioma = detect(texto)
    return idioma

textidioma = identificarlang(texto)
if textidioma == "pt":
    print(texto)
else:
    textoprint = traduzirtext(texto)
    print(textoprint)
