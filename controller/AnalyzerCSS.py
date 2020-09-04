class AnalyzerCSS():
    __instance = None

    def __new__(self):
        if not self.__instance:
            self.__instance = super(AnalyzerCSS, self).__new__(self)
        return self.__instance


    def __init__(self):
        self.row = 0
        self.column = 0
        self.counter = 0 
        self.arrayError = []
        self.arrayToken = []

        self.reservadas = ['color', 'border', 'text-align', 'font-weigth', 'padding-left',
                            'padding-top', 'line-height', 'margin-top', 'margin-left', 'display',
                            'top', 'float', 'min-windth', 'auto', 'none', 'padding', 'background-color',
                            'opacity', 'font-family', 'font-size', 'padding-rigth', 'width', 'margin-rigth',
                            'margin', 'position', 'rigth', 'clear', 'max-height', 'background-image', 
                            'background', 'font-style', 'font', 'padding-bottom', 'height', 'margin-bottom',
                            'border-style', 'bottom', 'left', 'max-width', 'min-height', 'px', 'em', 'vh', 'vw',
                            'in', 'cm', 'mm', 'pt', 'pc', 'rgba']


        self.signos = {"PUNTOYCOMA": ';', "LLAVEA": '{', "LLAVEC": '}', "DOSPUNTOS": ':', "SLASH" : '/', "ASTERISCO": '*',
                        "COMA": ',', "PORCENTAJE": '%', "NUMERAL": '#', "PARENTESISA": '(', "PARENTESISC": ')', "COMILLAS": "'",
                        "COMILLAD": "\"", "SLASHI": '\\', "NEGATIVO":'-'}

    def analizar(self, content):
        self.arrayError = []
        self.arrayToken = []
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
            elif symbol.isnumeric():
                sizeLexema = self.getSizeLexemaNumeric(self.counter, content)
                self.stateNumero(sizeLexema, content)
            elif ((symbol == "#" and content[self.counter + 1].isalpha()) or (symbol == '.' and content[self.counter + 1].isalpha())) :
                sizeLexema = self.getSizeLexema(self.counter + 1, content)
                self.stateSelector(sizeLexema - 1, content)
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
                        else:
                            if (symbol == "*" and (content[self.counter + 1 ] == " " or content[self.counter + 1 ] == " ")):
                                self.arrayToken.append([self.row, self.column, "Id", symbol])
                                self.counter += 1
                                self.column += 1
                                isSign = True
                                break
                            else:
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

        ##palabras reservadas
        self.wordReserved()
        self.stateString()
        
        print("Tokens")
        for x in self.arrayToken:
            print(x)
        print("-----------------------------------")
        return self.arrayToken

        #estado de numeros
    def stateNumero(self, sizeLexema, content):
        size = self.counter + sizeLexema
        if (content[self.counter : size].isnumeric() or '.' in content[self.counter : size]):
            self.addToken(self.row, self.column, 'int', content[self.counter : size])

        else:
            self.addError(self.row, self.column, content[self.counter : size])
        
        self.counter = self.counter + sizeLexema
        self.column = self.column + sizeLexema

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


    def stateIdentificador(self, sizeLexema, content):
        size = self.counter + sizeLexema
        self.addToken(self.row, self.column, 'Id', content[self.counter : size])
        self.counter = self.counter + sizeLexema
        self.column = self.column + sizeLexema

    # Para identificar selectores con . or #
    def stateSelector(self, sizeLexema, content):
        size = self.counter + sizeLexema
        self.addToken(self.row, self.column, 'Id', content[self.counter : size])
        self.counter = self.counter + sizeLexema
        self.column = self.column + sizeLexema

    def getSizeLexema(self, posInicio, content):
        longitud = 0
        for i in range(posInicio, len(content)): ## len(content)-1
            if (content[i].isalpha() or content[i] == "_" or content[i] == "-" or
                content[i].isnumeric()):
                longitud+=1
            else:
                break

        return longitud


    def getSizeLexemaNumeric(self, posInicio, content):
        longitud = 0
        for i in range(posInicio, len(content)): ## len(content)-1
            if (content[i] == " " or content[i] == "{" or content[i] == "}" or content[i] == "," or 
                content[i] == ";" or content[i] == ":" or content[i] == "\n" or content[i] == "\t" or 
                content[i] == "\r" or content[i] == "(" or content[i] == ")" or content[i] == "\"" or
                content[i] == "\'" or content[i].isalpha() or content[i] == "%" or content[i] == '\\'):
                break

            longitud+=1
        return longitud

    def wordReserved(self):
        for token in self.arrayToken:
            if token[2] == 'Id':
                for reservada in self.reservadas:
                    if token[3].lower() == reservada:
                        token[2] = "reservada"
                        break 

    
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

    def addToken(self, row, column, content, word):
        self.arrayToken.append([row, column, content, word])

    def addError(self, row, column, content):
        self.arrayError.append([row, column, content])

    def getArrayError(self):
        return self.arrayError