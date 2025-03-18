import ply.lex as lex
from tokens import *

def t_STRING(t):
    r"「(.*?)」"
    t.value = t.value[1:-1]
    return t

def t_PARTICLE(t):
    r"は|が|の|を|という|と|に|から|まで|より"
    t.type = particles.get(t.value, "PARTICLE")
    return t

def t_NUMBER(t):
    r"\d+"
    t.value = int(t.value)
    return t

def t_KANJI(t):
    r"[一-龯]+"
    if t.value in reserved:
        t.type = reserved[t.value]
    elif t.value in verbs.keys():
        t.type = verbs[t.value]
    return t

def t_HIRAGANA(t):
    r"[ぁ-ん]+"
    if t.value in reserved:
        t.type = reserved[t.value]
    elif t.value in base_forms.values():
        t.type = "VERB_B"
    elif t.value in te_forms.values():
        t.type = "TE_VERB_B"
    elif t.value in negative_forms.values():
        t.type = "NEGATIVE_VERB_B"
    elif t.value in negative_te_forms.values():
        t.type = "NEGATIVE_TE_VERB_B"
    return t

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()