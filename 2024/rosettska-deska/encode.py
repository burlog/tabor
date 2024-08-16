import sys
import json
import random
import simplemma
import seznam.lemmatizer

path = "/home/burlog/git/fulltext/lemmatizer/lemmatizer/data/cs/2016_01_11/"
lemmatizer = seznam.lemmatizer.Lemmatizer("../../.." + path)

D = {
    "usirem": "usir",
    "usirovo": "usir",
    "usira": "usir",
    "sakkára": "sakkára",
    "sakkáře": "sakkára",
    "eset": "eset",
    "mernefera": "mernefer",
    "mernefer": "mernefer",
    "merneferovi": "mernefer",
    "merneferova": "mernefer",
    "hyksósy": "hyksós",
    "hyksósům": "hyksós",
    "hyksóse": "hyksós",
    "hyksósové": "hyksós",
    "šepseskare": "šepseskare",
    "re": "re",
    "seth": "seth",
    "setha": "seth",
    "egypt": "egypt",
    "egyptu": "egypt",
    "egyptě": "egypt",
    "nil": "nil",
}

T = json.load(open("table.json"))

def keep(c):
    return c.isalnum() or c in "., "

def tokenize(filename, ignore_empty=False):
    for line in open(filename):
        line = line.replace(",", " , ").replace(".", " . ")
        line = "".join([c if keep(c) else " " for c in line])
        line = line.strip().lower()
        if not ignore_empty and not line:
            yield "="
            continue
        for token in line.split():
            if ignore_empty and token.strip() in ".,!?":
                continue
            yield token.strip()

def get_lemma(token):
    if simplemma.is_known(token, lang="cs"):
        return simplemma.lemmatize(token, lang="cs")
    lemmas = seznam.lemmatizer.Lemmas()
    res = lemmatizer.lemmatize(token, lemmas)
    if res == 0:
        for lemma in lemmas:
            return lemma.lemma
    exit(f"Unknown token: {token}")

def translate(filename):
    print("=" * 80)
    i = 0
    for token in tokenize(filename):
        if token == "=":
            print()
            print()
            i = 0
        elif token in ".,!?":
            print(token, end=" ")
        else:
            lemma = D[token] if token in D else get_lemma(token)
            print(f"{T[lemma]}({lemma})", end=" ")
            # print(f"{T[lemma]}", end=" ")
            i += 1
            if i == 7:
                print()
                i = 0
    print()

# def add_token(token, hyeroglyph=None):
#     if token not in T:
#         if hyeroglyph:
#             T[token] = hyeroglyph
#         else:
#             T[token] = H.pop()
#
# for token in tokenize("all", ignore_empty=True):
#     if token in D:
#         add_token(token, D[token])
#     else:
#         add_token(get_lemma(token))

translate("zprava-cs.txt")
translate("stela-cs.txt")

# json.dump(T, open("table.json", "w"), indent=2, ensure_ascii=False)
