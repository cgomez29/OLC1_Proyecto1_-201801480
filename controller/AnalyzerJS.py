import re
from bean.Token import Token
from bean.Token import Tipo

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
        #self.counter2 = 0
        self.arrayErrores = []
        self.arrayTokens = []
        self.reservadas = ['if', 'else', 'while', 'for', 'var',
                            'await', 'break', 'case', 'catch' ,'class','const', 'continue', 'debugger',
                            'default', 'delete', 'do', 'export', 'extends', 'finally', 'function', 'import',
                            'in', 'instanceof', 'new', 'return', 'super', 'switch', 'this', 'throw', 'try',
                            'typeof', 'void', 'with', 'async']

        self.signos = {"PUNTOCOMA":';', "LLAVEAPERTURA":'{', "LLAVECIERRE":'}', "IGUAL":'=', "PARENTECISA": '(',
                        "PARENTESISC": ')', "COMILLAS": "'", "COMILLAD": "\"", "ASTERISCO": "*", "SLASH": "/"}
        self.comentarys = {"CA": '/*', "CC":"*/", "CL": "//"}


    def analizar(self, content):
        self.arrayTokens = []
        self.arrayErrores = []
        while self.counter < len(content):
            symbol = content[self.counter]
            # S0 -> S1 (Simbolos del Lenguaje)
            if symbol == "\n":
                self.counter += 1
                self.row += 1
                self.column = 1 
            elif symbol =="\t":
                self.counter += 1
                self.column += 1 
            elif symbol ==" ":
                self.counter += 1
                self.column += 1
            #S0 -> S3
            elif symbol.isalpha():  
                sizeLexema = self.getSizeLexema(self.counter, content)
                size = self.counter + sizeLexema
                self.addToken(self.row, self.column, 'Id', content[self.counter : size])
                self.counter = self.counter + sizeLexema
                self.column = self.column + sizeLexema
            elif symbol.isnumeric():
                sizeLexema = self.getSizeLexema(self.counter, content)
                size = self.counter + sizeLexema
                self.addToken(self.row, self.column, 'int', content[self.counter : size])
                self.counter = self.counter + sizeLexema
                self.column = self.column + sizeLexema
            else:
                isSign = False
                tempSymbol = ""
                #---------- S0 -> s1
                for key in self.signos:
                    valor = self.signos[key]
                    if symbol == valor:
                        tempSymbol = symbol + content[self.counter + 1]
                        if (tempSymbol == "/*" or tempSymbol == "*/" or tempSymbol == "//"):
                            self.arrayTokens.append([self.row, self.column, "ComentaryL", tempSymbol.replace('\\','')])
                            self.counter += 2
                            self.column += 2
                            isSign = True
                        else:
                            self.arrayTokens.append([self.row, self.column, key, valor.replace('\\','')])
                            self.counter += 1
                            self.column += 1
                            isSign = True
                            break
                #-------------------S0 -> S4
                if not isSign:
                    self.arrayErrores.append([self.row, self.column, content[self.counter]])
                    self.column += 1
                    self.counter += 1
        #----------- S2 -> S3
        self.wordReserved()
        self.wordBoolean()
        self.lineComentary()
        # dantos entre comillas "x" and 'x'
        self.stateString()
        self.multiLineComentary()
        for x in self.arrayTokens:
            print(x)

        return self.arrayTokens


    #Retorna el tamaño del lexema
    def getSizeLexema(self, posInicio, content):
        longitud = 0
        for i in range(posInicio, len(content)): ## len(content)-1
            if (content[i] == " " or content[i] == "{" or content[i] == "}" or content[i] == "," or 
                content[i] == ";" or content[i] == ":" or content[i] == "\n" or content[i] == "\t" or 
                content[i] == "\r" or content[i] == "(" or content[i] == ")" or content[i] == "\"" or
                content[i] == "\'"):
                break

            longitud+=1
        return longitud

    def addToken(self, row, column, content, word):
        self.arrayTokens.append([row, column, content, word])

    def addError(self, row, column, content, word):
        self.arrayErrores.append([row, column, content, word])


    def wordReserved(self):
        for token in self.arrayTokens:
            if token[2] == 'Id':
                for reservada in self.reservadas:
                    if token[3].lower() == reservada:
                        token[2] = "reservada"
                        break 
    
    def wordBoolean(self):
        for token in self.arrayTokens:
            if (token[2] == 'Id' and (token[3].lower() == 'true' or token[3].lower()  == 'false')):
                token[2] = "Boolean"
                 

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

    def stateString(self):
        arrayTemp = []
        apertura = True
        lineaApertura = -1
        columnaApertura = 0
        columnaCierre = 0

        for line in self.arrayTokens:
            if line[2] == 'COMILLAD' or line[2] == 'COMILLAS':
                if (apertura == True ):      #fila , columna apertura# and lineaApertura != line[0]
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