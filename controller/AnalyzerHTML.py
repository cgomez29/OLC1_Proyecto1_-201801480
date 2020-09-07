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
        
        self.reservadas = ['DOCTYPE', 'html', 'meta', 'p', 'label', 'input', 'head', 'body', 'title',
                            'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'img', 'a', 'ul', 'li', 'style', 'tr',
                            'th', 'table', 'td', 'caption', 'colgroup', 'col', 'thead', 'tbody', 'tfoot']
        self.signos = {"MENORQUE": '<', "MAYORQ": '>', "SLASH": "/", "IGUAL": '=', "EXCLAMACION": '!',
                        "COMILLAD": '\"', "COMILLAS": '\''}
        ##Ubicando path de archivo
        self.contadorUbicacion = True
        self.ubicacionArchivo = ""

    def analizar(self, content):
        self.contadorUbicacion = True
        self.arrayToken = []
        self.arrayError = []
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
                        temp =  symbol + content[self.counter + 1: self.counter + 4]
                        if (symbol == ">"):
                            self.arrayToken.append([self.row, self.column, key, valor.replace('\\','')])
                            self.counter += 1
                            self.column += 1
                            self.letras(self.counter, content) 
                            isSign = True
                        elif (temp == "<!--"):
                            self.multiLineComentary(self.counter, content)
                            isSign =  True
                        elif (symbol == '\"' or symbol == '\''):
                            self.stateString(self.counter, content)
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

        self.wordReserved()
        self.generar_archivo_corregido(content)
        return self.arrayToken




    def letras(self, posInicio, content):
        longitud = 0
        for i in range(posInicio, len(content)):
            if (content[i] == "\n"):
                size = self.counter + longitud 
                self.addToken(self.row, self.column, 'TEXTO', content[self.counter : size])
                self.counter = self.counter + longitud 
                self.column = self.column + longitud 
                self.column = 1
                self.counter +=1
                self.row += 1
                longitud = 0
            elif (content[i] == "<" or content[i] == ">" ):
               
                size = self.counter + longitud
                self.addToken(self.row, self.column, 'TEXTO', content[self.counter : size])
                self.counter = self.counter + longitud
                self.column = self.column + longitud 
                longitud = 0
                break
            else:
                longitud += 1

    def getSizeLexema(self, posInicio, content):
        longitud = 0
        for i in range(posInicio, len(content)): ## len(content)-1
            if (content[i].isalpha() or content[i].isnumeric()):
                longitud+=1
            else:
                break

        return longitud
    
    def stateIdentificador(self, sizeLexema, content):
        size = self.counter + sizeLexema
        self.addToken(self.row, self.column, 'Id', content[self.counter : size])
        self.counter = self.counter + sizeLexema
        self.column = self.column + sizeLexema


    def stateString(self, posInicio, content):
        longitud = 0
        for i in range(posInicio + 1, len(content)):
            if (content[i] == "\n"):
                longitud += 1
                size = self.counter + longitud 
                self.addToken(self.row, self.column, 'COMILLA', content[self.counter : size])
                self.counter = self.counter + longitud 
                self.column = self.column + longitud 
                self.column = 1
                self.counter +=1
                self.row += 1
                longitud = 0
            elif (content[i]== '\"' or content[i] == '\''):
                longitud += 2
                size = self.counter + longitud
                self.addToken(self.row, self.column, 'COMILLA', content[self.counter : size])
                self.counter = self.counter + longitud
                self.column = self.column + longitud 
                break
            else:
                longitud += 1


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

    def multiLineComentary(self, posInicio, content):
        longitud = 0
        for i in range(posInicio, len(content)):
            incremento =  i + 3
            if incremento != len(content):
                temp = content[i] + content[i+ 1: incremento]
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
            elif (temp == "-->"):
                longitud += 3
                size = self.counter + longitud
                self.addToken(self.row, self.column, 'ComentaryL', content[self.counter : size])
                if self.contadorUbicacion and "PATHW" in content[self.counter : size] :
                    self.ubicacionArchivo = content[self.counter : size - 3]
                    self.contadorUbicacion = False
                self.counter = self.counter + longitud
                self.column = self.column + longitud 
                break
            else:
                longitud += 1


    def generar_archivo_corregido(self, content):
        path = ""
        contador = 0
        for x in self.ubicacionArchivo:
            if (x.lower() == "c"):
                path = self.ubicacionArchivo[contador: len(self.ubicacionArchivo)]
                break
            contador+=1

        counter = 0
        line = 1
        column = 1

        newContent = ""
        #arreglo temporal de errores
        arrayTemp = []
        for x in self.arrayError:
            arrayTemp.append(x)

        while counter < len(content):
            bandera = True
            for error in arrayTemp:
                if error[0] == line and error[1] == column:
                    size = len(error[2])
                    counter = counter + size
                    column = column + size
                    bandera = False
                    arrayTemp.remove(error)

            if (bandera):
                if (content[counter] == "\n"):
                    line +=1
                    column = 1
                else:
                    column +=1

                newContent = newContent + content[counter]
                counter+=1

        
        #print(newContent)
        
        path = path.replace(" ", "") + "new_file.html"
        file = open(path, "w")
        file.write(newContent)
        file.close()