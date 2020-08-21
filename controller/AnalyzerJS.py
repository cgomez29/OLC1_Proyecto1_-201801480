import re

class AnalyzerJS():

    __instance = None

    def __new__(self):
        if not self.__instance:
            self.__instance = super(AnalyzerJS, self).__new__(self)
        return self.__instance

    def __init__(self):
        self.row = 1
        self.column = 1
        self.counter = 0
        self.counter2 = 0
        self.arrayErrores = []
        self.arrayTokens = []
        self.reservadas = ['if', 'else', 'while', 'for', 'var']
        self.signos = {"PUNTOCOMA":';', "LLAVEAPERTURA":'{', "LLAVECIERRE":'}', "IGUAL":'=', "PARENTECISA": '\(',
                        "PARENTESISC": '\)'}
        self.comentarys = {"CA": '/*', "CC":"*/"}
    def analyzer_java(self, content):

        while self.counter < len(content):
            
            if re.search(r"[A-Za-z]", content[self.counter]) :
                self.arrayTokens.append(self.stateId(self.row, self.column, content, content[self.counter]))
            elif re.search(r"[\/*+\**]", content[self.counter]):
                #self.counter += 1
                #self.column += 1 
                self.arrayTokens.append(self.stateComentary(self.row, self.column, content, content[self.counter]))
            elif re.search(r"[\n]", content[self.counter]):
                self.counter += 1
                self.row += 1
                self.column = 1 
            elif re.search(r"[ \t]", content[self.counter]):
                self.counter += 1
                self.column += 1 
            else:
                #signos
                isSign = False
                for key in self.signos:
                    valor = self.signos[key]
                    if re.search(valor, content[self.counter]):
                        self.arrayTokens.append([self.row, self.column, key, valor.replace('\\','')])
                        self.counter += 1
                        self.column += 1
                        isSign = True
                        break
                if not isSign:
                    self.column += 1
                    self.arrayErrores.append([self.row, self.column, content[self.counter]])
                    self.counter += 1
        self.lineComentary()
        self.wordReserved(self.arrayTokens)
        return self.arrayTokens

    def returnErrors(self):
        return self.arrayErrores
    ##Fila, columna, contenido, palabra
    def stateId(self, row, column, content, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(content):
            if re.search(r"[a-zA-Z_0-9]", content[self.counter]):
                return  self.stateId(row, column, content, word + content[self.counter])
            else: 
                return [row, column, 'Id', word]
        else:
            return [row, column, 'Id', word]

    
    def stateComentary(self, row, column, content, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(content):
            if re.search(r"[\/*+\**]", content[self.counter]):
                return self.stateComentary(row, column, content, word + content[self.counter])
            else: 
                return [row, column, 'ComentaryL', word]
        else: 
            return [row, column, 'ComentaryL', word]

    def lineComentary(self):
        arrayTemp = []
        for line in self.arrayTokens:
            if line[2] == 'ComentaryL':
                arrayTemp.append(line[0])

        for line in arrayTemp:
            for x in self.arrayTokens:
                if line == x[0]:
                    x[2] = "ComentaryL"

    def wordReserved(self, arrayTokens):
        for token in self.arrayTokens:
            if token[2] == 'Id':
                for reservada in self.reservadas:
                    word = r"^" + reservada + "$"
                    if re.match(word, token[3], re.IGNORECASE):
                        token[2] = "reservada"
                        break 
