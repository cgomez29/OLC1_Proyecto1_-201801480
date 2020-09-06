class AnalyzerRMT():
    __instance = None

    def __new__(self):
        if not self.__instance:
            self.__instance = super(AnalyzerRMT, self).__new__(self)
        return self.__instance


    def __init__(self):
        self.row = 0
        self.column = 0
        self.counter = 0 
        self.arrayError = []
        self.arrayToken = []

        self.signos = {"PARENTESISA": '(', "PARENTESISC": ')', "CORCHETEA": '[', "CORCHETEC": ']',
                        "SUMA": '+', "RESTA": '-', "MULTIPLICACION": '*', "DIVICION": '/'}


    def analizar(self, content):
        self.arrayToken = []
        self.arrayError = []
        self.row = 1
        self.column = 1
        self.counter = 0
        while (self.counter < len(content)):
            symbol = content[self.counter]
            if (symbol == "\n"):
                self.counter += 1
                self.row += 1
                self.column = 1 
            elif (symbol =="\t"):
                self.counter += 1
                self.column += 1 
            elif (symbol ==" "):
                self.counter += 1
                self.column += 1
            elif (symbol.isnumeric()):
                sizeLexema = self.getSizeLexemaNumeric(self.counter, content)
                self.stateNumero(sizeLexema, content)
            elif (symbol.isalpha()):
                sizeLexema = self.getSizeLexema(self.counter, content)
                self.stateIdentificador(sizeLexema, content)
            else:
                isSign = False
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

        return self.arrayToken

    #estado de identicadores
    def stateIdentificador(self, sizeLexema, content):
        size = self.counter + sizeLexema
        self.addToken(self.row, self.column, 'Id', content[self.counter : size])
        self.counter = self.counter + sizeLexema
        self.column = self.column + sizeLexema
        self.contadorRecorridoId = False

    #estado de numeros
    def stateNumero(self, sizeLexema, content):
        size = self.counter + sizeLexema
        if (content[self.counter : size].isnumeric() or '.' in content[self.counter : size]):
            self.addToken(self.row, self.column, 'int', content[self.counter : size])
        else:
            self.addError(self.row, self.column, content[self.counter : size])
        
        self.counter = self.counter + sizeLexema
        self.column = self.column + sizeLexema


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
        self.arrayToken.append([row, column, content, word])

    def addError(self, row, column, content):
        self.arrayError.append([row, column, content])

    def getArrayError(self):
        return self.arrayError