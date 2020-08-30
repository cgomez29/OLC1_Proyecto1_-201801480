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
                            'top', 'float', 'min-windth', 'auto']
        self.signos = {"PUNTOYCOMA": ';', "LLAVEA": '{', "LLAVEC": '}'}
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
            #S0 -> S3
            elif symbol.isalpha():  
                sizeLexema = self.getSizeLexema(self.counter, content)
                size = self.counter + sizeLexema
                self.addToken(self.row, self.column, 'Id', content[self.counter : size])
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
                            self.arrayToken.append([self.row, self.column, "ComentaryL", tempSymbol.replace('\\','')])
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

        print("Tokens")
        for x in self.arrayToken:
            print(x)
        print("-----------------------------------")

        return self.arrayToken

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
        self.arrayToken.append([row, column, content, word])

    def getArrayError(self):
        return self.arrayError