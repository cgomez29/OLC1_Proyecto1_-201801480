from enum import Enum


class Tipo(Enum):
    # Simbolos del Lenguaje
    LLAVEIZQ = 1
    LLAVEDER = 2
    DPUNTOS = 3
    PCOMA = 4
    PARARENTESISA = 5
    PARARENTESISC = 6

    # Palabras reservadas
    IF = 5
    ELSE = 6
    CLASS = 7

    # Expresiones Regulares
    ENTEROS = 12
    ID = 13
    NINGUNO = 14

class Token:
    tipoToken = Tipo.NINGUNO
    valorToken = ""
    def __init__(self, tipo, valor ):
        self.tipoToken = tipo
        self.valorToken = valor