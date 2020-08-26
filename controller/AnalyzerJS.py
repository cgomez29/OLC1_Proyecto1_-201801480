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
        self.reservadas = ['if', 'else', 'while', 'for', 'var', 'int', 'Boolean', 'String', 'Char',
                            'await', 'break', 'case', 'catch' ,'class','const', 'continue', 'debugger',
                            'default', 'delete', 'do', 'export', 'extends', 'finally', 'function', 'import',
                            'in', 'instanceof', 'new', 'return', 'super', 'switch', 'this', 'throw', 'try',
                            'typeof', 'void', 'with', 'async']

        self.signos = {"PUNTOCOMA":';', "LLAVEAPERTURA":'{', "LLAVECIERRE":'}', "IGUAL":'=', "PARENTECISA": '\(',
                        "PARENTESISC": '\)', "COMILLAS": "'", "COMILLAD": "\""}
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
                    #self.column += 1
                    self.arrayErrores.append([self.row, self.column, content[self.counter]])
                    self.column += 1
                    self.counter += 1
        self.lineComentary()
        self.stateString()
        self.multiLineComentary()
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

    def multiLineComentary(self):
        arrayTemp = []
        apertura = True
        lineaApertura = -1
        lineaCierre = -1
        columnaApertura = 0
        columnaCierre = 0

        for line in self.arrayTokens:
            if line[3] == '/*' or line[3] == '*/':
                if (apertura == True and lineaApertura != line[0]):      #fila , columna apertura
                    #arrayTemp.append([line[0], line[1]], "A")
                    apertura = False
                    lineaApertura = line[0]
                    columnaApertura = line[1]
                elif (lineaApertura != line[0]): 
                    #fila A, fila C , columna A, columna C
                    arrayTemp.append([lineaApertura, line[0]])
                    apertura = True

        for line in arrayTemp:
            for i in self.arrayErrores:
                if i[0] >= line[0] and i[0] <= line[1]:            
                    self.arrayTokens.append([i[0], i[1], ["ComentaryL"], i[2]])
                    self.arrayErrores.remove(i)
            
            for x in self.arrayTokens:
                #if x[0] >= line[0] and x[0] <= line[1] and x[1] >= line[2] and x[1] <= line[3]:
                if x[0] >= line[0] and x[0] <= line[1]:
                    #print("Row1" + str(x[0]))
                    #print("RowInicio" + str(line[0]))
                    #print("RowFIn" + str(line[1]))
                    #print("----------------")
                    x[2] = "ComentaryL"
                    

    ## ver lo del salto de linea por eso no lo pinta en griss


    def wordReserved(self, arrayTokens):
        for token in self.arrayTokens:
            if token[2] == 'Id':
                for reservada in self.reservadas:
                    word = r"^" + reservada + "$"
                    if re.match(word, token[3], re.IGNORECASE):
                        token[2] = "reservada"
                        break 
    
    def stateString(self):
        arrayTemp = []
        apertura = True
        lineaApertura = -1
        columnaApertura = 0
        columnaCierre = 0

        for line in self.arrayTokens:
            if line[2] == 'COMILLAD' or line[2] == 'COMILLAS':
                if (apertura == True and lineaApertura != line[0]):      #fila , columna apertura
                    #arrayTemp.append([line[0], line[1]], "A")
                    apertura = False
                    lineaApertura = line[0]
                    columnaApertura = line[1]
                elif (lineaApertura == line[0]): 
                    #fila , columna A, columna C
                    arrayTemp.append([line[0], columnaApertura, line[1]])
                    columnaCierre = line[0]
                    apertura = True

        for line in arrayTemp:
            for x in self.arrayTokens:
                if line[0] == x[0] and x[1] >= line[1] and x[1] <= line[2]:
                    x[2] = "COMILLA"

    def getArrayErrors(self):
        return self.arrayErrores
    #que sea igual a la linea y mayor que esa columna