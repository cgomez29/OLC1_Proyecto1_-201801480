class AnalyzerJS():

    __instance = None

    def __new__(self):
        if not self.__instance:
            self.__instance = super(AnalyzerJS, self).__new__(self)
        return self.__instance

    def __init__(self):
        self.row = 0
        self.column = 0
        self.counter = 0
        #self.counter2 = 0
        self.arrayErrores = []
        self.arrayTokens = []
        self.reservadas = ['if', 'else', 'while', 'for', 'var',
                            'await', 'break', 'case', 'catch' ,'class','const', 'continue', 'debugger',
                            'default', 'delete', 'do', 'export', 'extends', 'finally', 'function', 'import',
                            'in', 'instanceof', 'new', 'return', 'super', 'switch', 'this', 'throw', 'try',
                            'typeof', 'void', 'with', 'async', 'console', 'log', 'math', 'pow']

        self.signos = {"PUNTOCOMA":';', "LLAVEAPERTURA":'{', "LLAVECIERRE":'}', "IGUAL":'=', "PARENTECISA": '(',
                        "PARENTESISC": ')', "COMILLAS": "\'", "COMILLAD": "\"", "ASTERISCO": "*", "SLASH": "/", "SUMA": '+',
                        "NEGATIVO": '-', "DIVICION2": '%', "MAYORQ": '>', "MENORQ": '<', "PUNTO": '.', "COMA": ',',
                        "CONJUNCION":'&', "DISYUNCION": '|', "NEGACION": '!', "CORCHETEA": '[', "CORCHETEC": ']', "GUIONBAJO": '_',
                        "DOSPUNTOS": ':'}
                    
        self.comentarys = {"CA": '/*', "CC":"*/", "CL": "//"}


    def analizar(self, content):
        self.arrayTokens = []
        self.arrayErrores = []
        self.row = 1
        self.column = 1
        self.counter = 0
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
            elif symbol == "_":
                temp = content[self.counter + 1]
                if (temp.isalpha()):
                    sizeLexema = self.getSizeLexema(self.counter, content)
                    self.stateIdentificador(sizeLexema, content)
            #S0 -> S3
            elif symbol.isalpha():  
                sizeLexema = self.getSizeLexema(self.counter, content)
                self.stateIdentificador(sizeLexema, content)

            elif symbol.isnumeric():
                sizeLexema = self.getSizeLexemaNumeric(self.counter, content)
                self.stateNumero(sizeLexema, content)
            else:
                isSign = False
                tempSymbol = ""
                #---------- S0 -> s1
                for key in self.signos:
                    valor = self.signos[key]
                    if symbol == valor:
                        tempSymbol = symbol + content[self.counter + 1]
                        if (tempSymbol == "/*"):
                            self.multiLineComentary(self.counter,content)
                            isSign = True
                        elif (tempSymbol == "//"):
                            self.arrayTokens.append([self.row, self.column, "ComentaryL", "//"])
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
        # dantos entre comillas "x" and 'x'
        self.stateString()
        self.lineComentary()
        
        for x in self.arrayTokens:
           print(x)

        return self.arrayTokens


    #estado de numeros
    def stateNumero(self, sizeLexema, content):
        size = self.counter + sizeLexema
        if (content[self.counter : size].isnumeric() or '.' in content[self.counter : size]):
            self.addToken(self.row, self.column, 'int', content[self.counter : size])
        else:
            self.addError(self.row, self.column, content[self.counter : size])
        
        self.counter = self.counter + sizeLexema
        self.column = self.column + sizeLexema


    def stateIdentificador(self, sizeLexema, content):
        size = self.counter + sizeLexema
        self.addToken(self.row, self.column, 'Id', content[self.counter : size])
        self.counter = self.counter + sizeLexema
        self.column = self.column + sizeLexema

    #Retorna el tamaño del lexema
    def getSizeLexema(self, posInicio, content):
        longitud = 0
        for i in range(posInicio, len(content)): ## len(content)-1
            if (content[i].isalpha() or content[i] == "_" or content[i].isnumeric()):
                longitud+=1
            else:
                break
        return longitud

    def getSizeLexemaNumeric(self, posInicio, content):
        longitud = 0
        for i in range(posInicio, len(content)): ## len(content)-1
            if (content[i].isnumeric() or content[i] == "."): # or content[i].isalpha() si se coloca reconoce numero y luego las letras
                longitud+=1
            else:
                break

        return longitud
    

    def addToken(self, row, column, content, word):
        self.arrayTokens.append([row, column, content, word])

    def addError(self, row, column, content):
        self.arrayErrores.append([row, column, content])


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
            if line[2] == 'ComentaryL' and line[3] == "//":
                arrayTemp.append([line[0], line[1]])

        for line in arrayTemp:
            for x in self.arrayTokens:
                if line[0] == x[0] and  x[1] >= line[1] and x[2] != 'COMILLA':
                    x[2] = "ComentaryL"
                

    def multiLineComentary(self, posInicio, content):
        longitud = 0
        for i in range(posInicio, len(content)):
            incremento =  i + 1
            if incremento != len(content):
                temp = content[i] + content[incremento]
            else:
                break
            
            if (content[i] == "\n"):
                size = self.counter + longitud 
                self.addToken(self.row, self.column, 'ComentaryL', content[self.counter : size])
                self.counter = self.counter + longitud 
                self.column = self.column + longitud 
                self.column = 1
                self.counter +=1
                self.row += 1
                longitud = 0
            elif (temp == "*/"):
                longitud += 2
                size = self.counter + longitud
                self.addToken(self.row, self.column, 'ComentaryL', content[self.counter : size])
                self.counter = self.counter + longitud
                self.column = self.column + longitud 
                break
            else:
                longitud += 1

       


    def stateString(self):
        arrayTemp = []
        apertura = True
        lineaApertura = 0
        columnaApertura = 0

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
                    apertura = True
                

        for line in arrayTemp:
            for x in self.arrayTokens:
                if (line[0] == x[0] and (x[1] >= line[1] and x[1] <= line[2])):
                    x[2] = "COMILLA"
            ## rescatando de los errores
            for x in self.arrayErrores:
                if (line[0] == x[0] and (x[1] >= line[1] and x[1] <= line[2])):            
                    self.arrayTokens.append([x[0], x[1], "COMILLA", x[2]])
                    self.arrayErrores.remove(x)



    def getArrayErrors(self):
        return self.arrayErrores