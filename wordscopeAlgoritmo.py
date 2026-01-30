import re
import spacy
from langdetect import detect
from deep_translator import GoogleTranslator

# Carregar modelo do spaCy
nlp = spacy.load("en_core_web_sm")

# -------------------------
# Funções auxiliares
# -------------------------

def identificarlang(texto):
    return detect(texto)

def traduzirtext(texto, destino="pt"):
    try:
        return GoogleTranslator(source="auto", target=destino).translate(texto)
    except:
        return texto

def limpar_palavra(palavra):
    palavra = palavra.lower()
    palavra = re.sub(r"[^\w']", "", palavra)
    return palavra

def gerar_exemplo(token):
    if token["pos"] == "NOUN":
        return f"This is my {token['lemma']}."
    
    if token["pos"] == "VERB":
        return f"I {token['lemma']} every day."

    return None

# -------------------------
# Função principal
# -------------------------

def process_text(text):
    idioma = identificarlang(text)
    doc = nlp(text)

    word_objects = []

    for token in doc:
        if token.is_punct or token.is_space:
            continue

        clean = limpar_palavra(token.text)

        translation = (
            traduzirtext(clean)
            if idioma != "pt"
            else clean
        )

        word_data = {
            "original": token.text,
            "clean": clean,
            "lemma": token.lemma_,
            "pos": token.pos_,
            "translation": translation,
            "examples": []
        }

        exemplo = gerar_exemplo(word_data)
        if exemplo:
            word_data["examples"].append(exemplo)

        word_objects.append(word_data)

    return word_objects

# -------------------------
# Teste
# -------------------------

texto = input("Digite algo em inglês: ")
resultado = process_text(texto)

for w in resultado:
    print(w)