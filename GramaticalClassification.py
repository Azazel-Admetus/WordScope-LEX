import spacy
import re

# Carregar modelo em inglês do spaCy
nlp = spacy.load("en_core_web_sm")

def process_text(text):
    # 1. Quebrar o texto em palavras
    words = re.findall(r'\b\w+\b', text)

    # 2. Criar estrutura inicial
    word_objects = []
    for word in words:
        clean_word = re.sub(r'[.,!?;:]', '', word)
        doc = nlp(clean_word)
        pos_tag = doc[0].pos_ if doc else "UNKNOWN"
        word_objects.append({
            "original": word,
            "clean": clean_word,
            "pos": pos_tag,
            "translation": None,  # aqui será preenchido pelo código de tradução
            "examples": []        # aqui serão adicionadas frases de exemplo
        })
    return word_objects

# Teste inicial
text = "Hello world! This is a test sentence."
words_data = process_text(text)

for w in words_data:
    print(w)