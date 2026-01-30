import re
import json
import spacy
from langdetect import detect
from deep_translator import GoogleTranslator

# ======================
# Inicialização
# ======================

nlp = spacy.load("en_core_web_sm")

# ======================
# Funções utilitárias
# ======================

def identificar_idioma(texto: str) -> str:
    return detect(texto)

def traduzir(texto: str, destino: str = "pt") -> str:
    return GoogleTranslator(source="auto", target=destino).translate(texto)

def limpar_palavra(palavra: str) -> str:
    return re.sub(r"[^\w']", "", palavra.lower())

# ======================
# Exemplos (MVP seguro)
# ======================

def gerar_exemplo(lemma: str, pos: str):
    if pos == "NOUN":
        return f"This is my {lemma}."
    if pos == "VERB":
        return f"I {lemma} every day."
    return None

# ======================
# ENGINE PRINCIPAL
# ======================

def analyze_text(text: str) -> dict:
    idioma = identificar_idioma(text)
    palavras = re.findall(r"\b\w+\b", text)

    resultado = {
        "language": idioma,
        "words": {}
    }

    for palavra in palavras:
        clean = limpar_palavra(palavra)
        doc = nlp(clean)
        token = doc[0]

        lemma = token.lemma_
        pos = token.pos_

        if lemma not in resultado["words"]:
            traducao = traduzir(lemma) if idioma != "pt" else lemma

            entrada = {
                "originals": [palavra],
                "clean": clean,
                "lemma": lemma,
                "pos": pos,
                "translation": traducao,
                "examples": [],
                "count": 1
            }

            exemplo = gerar_exemplo(lemma, pos)
            if exemplo:
                entrada["examples"].append(exemplo)

            resultado["words"][lemma] = entrada
        else:
            resultado["words"][lemma]["originals"].append(palavra)
            resultado["words"][lemma]["count"] += 1

    return resultado

# ======================
# Teste local
# ======================

if __name__ == "__main__":
    texto = input("Digite algo em inglês: ")
    resultado = analyze_text(texto)
    print(json.dumps(resultado, indent=2, ensure_ascii=False))