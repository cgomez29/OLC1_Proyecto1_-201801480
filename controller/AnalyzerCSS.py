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
                            'border-style', 'bottom', 'left', 'max-width', 'min-height']
        self.signos = {"PUNTOYCOMA": ';', "LLAVEA": '{', "LLAVEC": '}', "DOSPUNTOS": ':', "SLASH" : '/', "ASTERISCO": '*'}

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
            elif ((symbol == "#" and content[self.counter + 1].isalpha()) or (symbol == '.' and content[self.counter + 1].isalpha())) :
                sizeLexema = self.getSizeLexema(self.counter, content)
                self.stateSelector(sizeLexema, content)
            else:
                isSign = False
                tempSymbol = ""
                #---------- S0 -> s1
                for key in self.signos:
                    valor = self.signos[key]
                    if symbol == valor:
                        tempSymbol = symbol + content[self.counter + 1]
                        if (tempSymbol == "/*" or tempSymbol == "*/"):
                            self.arrayToken.append([self.row, self.column, "ComentaryL", tempSymbol])
                            self.counter += 2
                            self.column += 2
                            isSign = True
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
        self.multiLineComentary()
        print("Tokens")
        for x in self.arrayToken:
            print(x)
        print("-----------------------------------")
        return self.arrayToken

    def multiLineComentary(self):
        arrayTemp = []
        apertura = True
        lineaApertura = 0
        lineaCierre = 0
        columnaApertura = 0
        columnaCierre = 0

        for line in self.arrayToken:
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
            for x in self.arrayToken:
                    #Misma linea 
                if (line[0] == x[0] and x[1] >= line[2] and x[1] <= line[3]):
                    x[2] = "ComentaryL"
                    ##varias lineas
                elif ( line[0] != line[1] and  x[0] >= line[0] and x[0] <= line[1]):
                    x[2] = "ComentaryL"
        
            for x in self.arrayError:
                if (line[0] == x[0] and x[1] >= line[2] and x[1] <= line[3]):
                    self.arrayToken.append([x[0], x[1], "ComentaryL", x[2]])
                    self.arrayError.remove(x)
                elif (line[0] != line[1] and x[0] >= line[0] and x[0] <= line[1]):
                    self.arrayToken.append([x[0], x[1], "ComentaryL", x[2]])
                    self.arrayError.remove(x)


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
            if (content[i] == " " or content[i] == "{" or content[i] == "}" or content[i] == "," or 
                content[i] == ";" or content[i] == ":" or content[i] == "\n" or content[i] == "\t" or 
                content[i] == "\r" or content[i] == "(" or content[i] == ")" or content[i] == "\"" or
                content[i] == "\'"):
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

    
    def addToken(self, row, column, content, word):
        self.arrayToken.append([row, column, content, word])

    def getArrayError(self):
        return self.arrayError