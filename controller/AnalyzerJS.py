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
                        "PARENTESISC": ')', "COMILLAS": "'", "COMILLAD": "\"", "ASTERISCO": "*", "SLASH": "/", "SUMA": '+',
                        "NEGATIVO": '-', "DIVICION2": '%', "MAYORQ": '>', "MENORQ": '<', "PUNTO": '.', "COMA": ',',
                        "CONJUNCION":'&', "DISYUNCION": '|', "NEGACION": '!', "CORCHETEA": '[', "CORCHETEC": "]"}
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
            #S0 -> S3
            elif symbol.isalpha():  
                sizeLexema = self.getSizeLexema(self.counter, content)
                self.stateIdentificador(sizeLexema, content)
            elif symbol.isnumeric():
                sizeLexema = self.getSizeLexema(self.counter, content)
                self.stateNumero(sizeLexema, content)
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
        
        #for x in self.arrayTokens:
        #   print(x)

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
            if (content[i] == " " or content[i] == "{" or content[i] == "}" or content[i] == "," or 
                content[i] == ";" or content[i] == ":" or content[i] == "\n" or content[i] == "\t" or 
                content[i] == "\r" or content[i] == "(" or content[i] == ")" or content[i] == "\"" or
                content[i] == "\'"):
                break

            longitud+=1
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
            if line[2] == 'ComentaryL':
                arrayTemp.append(line[0])

        for line in arrayTemp:
            for x in self.arrayTokens:
                if line == x[0]:
                    x[2] = "ComentaryL"

    def multiLineComentary(self):
        arrayTemp = []
        apertura = True
        lineaApertura = 0
        lineaCierre = 0
        columnaApertura = 0
        columnaCierre = 0

        for line in self.arrayTokens:
            if line[3] == '/*' or line[3] == '*/':
                if (apertura == True ):      #fila , columna apertura# and lineaApertura != line[0]
                    #arrayTemp.append([line[0], line[1]], "A")
                    apertura = False
                    lineaApertura = line[0]
                    columnaApertura = line[1]
                else: 
                    #fila , columna A, columna C
                    lineaCierre = line[0]
                    columnaCierre = line[1]
                    arrayTemp.append([lineaApertura, lineaCierre, columnaApertura, columnaCierre])
                    
                    apertura = True

        for line in arrayTemp:
            for x in self.arrayTokens:
                #una linea
                if (line[0] == x[0] and x[1] >= line[2] and x[1] <= line[3]):
                    x[2] = "ComentaryL"
                #multi linea
                elif (line[0] != line[1] and x[0] >= line[0] and x[0] <= line[1]):
                    x[2] = "ComentaryL"
        
            for x in self.arrayErrores:
                if (line[0] == x[0] and x[1] >= line[2] and x[1] <= line[3]):
                    self.arrayTokens.append([x[0], x[1], "ComentaryL", x[2]])
                    self.arrayErrores.remove(x)
                elif (line[0] != line[1] and x[0] >= line[0] and x[0] <= line[1]):
                    self.arrayTokens.append([x[0], x[1], "ComentaryL", x[2]])
                    self.arrayErrores.remove(x)

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
            ## rescatando de los errores
            for x in self.arrayErrores:
                if line[0] == x[0] and x[1] >= line[1] and x[1] <= line[2]:            
                    self.arrayTokens.append([x[0], x[1], "COMILLA", x[2]])
                    self.arrayErrores.remove(x)

    def getArrayErrors(self):
        return self.arrayErrores