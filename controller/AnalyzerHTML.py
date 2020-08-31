class AnalyzerHTML():
    __instance = None

    def __new__(self):
        if not self.__instance:
            self.__instance = super(AnalyzerHTML, self).__new__(self)
        return self.__instance

    def __init__(self):
        self.row = 0
        self.column = 0
        self.counter = 0
        self.arrayError = []
        self.arrayToken = []
        
        self.reservadas = ['DOCTYPE', 'html', 'meta', 'p', 'label', 'input', 'head', 'body']
        self.signos = {"MENORQUE": '<', "MAYORQ": '>', "SLASH": "/", "IGUAL": '=', "EXCLAMACION": '!',
                        "COMILLAD": '\"'}


    def analizar(self, content):
        self.arrayTokens = []
        self.arrayErrores = []
        self.row = 1
        self.column = 1
        self.counter = 0
        while self.counter < len(content):
            symbol = content[self.counter]
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
            elif symbol.isalpha():  
                sizeLexema = self.getSizeLexema(self.counter, content)
                self.stateIdentificador(sizeLexema, content)
            else:
                isSign = False
                tempSymbol = ""
                #---------- S0 -> s1
                for key in self.signos:
                    valor = self.signos[key]
                    if symbol == valor:
                        self.arrayToken.append([self.row, self.column, key, valor.replace('\\','')])
                        self.counter += 1
                        self.column += 1
                        isSign = True
                        break
                #-------------------S0 -> S4
                if not isSign:
                    self.arrayError.append([self.row, self.column, content[self.counter]])
                    self.column += 1
                    self.counter += 1

        self.wordReserved()
        self.stateString()
        return self.arrayToken

    def getSizeLexema(self, posInicio, content):
        longitud = 0
        for i in range(posInicio, len(content)): ## len(content)-1
            if (content[i] == " " or content[i] == "{" or content[i] == "}" or content[i] == "," or 
                content[i] == ";" or content[i] == ":" or content[i] == "\n" or content[i] == "\t" or 
                content[i] == "\r" or content[i] == "(" or content[i] == ")" or content[i] == "\"" or
                content[i] == "\'" or content[i] == '<' or content[i] == '>' or content[i] == '='):
                break

            longitud+=1
        return longitud
    
    def stateIdentificador(self, sizeLexema, content):
        size = self.counter + sizeLexema
        self.addToken(self.row, self.column, 'Id', content[self.counter : size])
        self.counter = self.counter + sizeLexema
        self.column = self.column + sizeLexema


    def stateString(self):
        arrayTemp = []
        apertura = True
        lineaApertura = -1
        columnaApertura = 0
        columnaCierre = 0

        for line in self.arrayToken:
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
            for x in self.arrayToken:
                if line[0] == x[0] and x[1] >= line[1] and x[1] <= line[2]:
                    x[2] = "COMILLA"
            ## rescatando de los errores
            for x in self.arrayError:
                if line[0] == x[0] and x[1] >= line[1] and x[1] <= line[2]:            
                    self.arrayToken.append([x[0], x[1], "COMILLA", x[2]])
                    self.arrayError.remove(x)


    def wordReserved(self):
        for token in self.arrayToken:
            if token[2] == 'Id':
                for reservada in self.reservadas:
                    if token[3].lower() == reservada:
                        token[2] = "reservada"
                        break 

    def addToken(self, row, column, content, word):
        self.arrayToken.append([row, column, content, word])

    def addError(self, row, column, content):
        self.arrayError.append([row, column, content])

    def getArrayError(self):
        return self.arrayError