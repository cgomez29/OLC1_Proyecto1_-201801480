from controller.GraphGenerator import GraphGenerator
import os

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
        self.graphGenerator = GraphGenerator()
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
                        #TransicionA, #TransicionB, No terminal, True A es aceotacion si no es B
        self.recorridoID = []
        self.contadorRecorridoId = True
        self.contadorUbicacion = True
        self.ubicacionArchivo = ""

    def analizar(self, content):
        #grafo de ID a imprimir solo una vez por documento
        self.contadorRecorridoId = True
        self.contadorUbicacion = True
        
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
            #S0 -> S2
            elif symbol == "_":
                temp = content[self.counter + 1]
                if (temp.isalpha()):
                    if (self.contadorRecorridoId):
                        self.recorridoID.append(["q0", "q2", "_", False ])

                    sizeLexema = self.getSizeLexema(self.counter, content)
                    self.stateIdentificador(sizeLexema, content)
                    
            #S0 -> S3
            elif symbol.isalpha():  
                if (self.contadorRecorridoId):
                    self.recorridoID.append(["q0", "q1", content[self.counter], False ])

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
                            self.multiLineComentary(self.counter, content)
                            isSign = True
                        elif (tempSymbol == "//"):
                            self.lineComentary(self.counter, content)
                            isSign = True
                        elif (symbol == "&"):
                            if (content[self.counter + 1] == "&"):
                                self.arrayTokens.append([self.row, self.column, "CONJUNCION", "&&"])
                                self.counter += 2
                                self.column += 2
                                isSign = True
                        elif (symbol == '\"' or symbol == '\''):
                            self.stateString(self.counter, content)
                            isSign = True
                        elif (symbol == "|"):
                            if (content[self.counter + 1] == "|"):
                                self.arrayTokens.append([self.row, self.column, "DISYUNCION", "||"])
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
        if (self.contadorRecorridoId == False):
            ## arreglo con datos del afd
            self.graphGenerator.graphJS(self.recorridoID)
        
        #for x in self.arrayTokens:
        #  print(x)

        ## generando archivo corregido
        self.generar_archivo_corregido(content)
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
        self.contadorRecorridoId = False


    #Retorna el tamaño del lexema
    #S0 -> S1(Letras)
    #S1 -> S2("_")
    def getSizeLexema(self, posInicio, content):
        longitud = 0
        for i in range(posInicio, len(content)): ## len(content)-1
            if (content[i].isalpha() or content[i] == "_" or content[i].isnumeric()):
                longitud+=1
                if (self.contadorRecorridoId):
                    x = i
                    x +=1
                    if (x != len(content)):
                        if (content[x].isalpha()):
                            if (content[x-1].isnumeric()):
                                self.recorridoID.append(["q3", "q1", content[x], False ])
                            elif (content[x-1] == "_"):
                                self.recorridoID.append(["q2", "q1", content[x], False ])
                            else:
                                self.recorridoID.append(["q1", "q1", content[x], False ])
                        elif (content[x] == "_"):
                            if (content[x-1].isnumeric()):
                                self.recorridoID.append(["q3", "q2", "_", False ])
                            elif (content[x-1].isalpha()):
                                self.recorridoID.append(["q1", "q2", "_", False ])
                            else:
                                self.recorridoID.append(["q2", "q2", "_", False ])
                        elif (content[x].isnumeric()):
                            if (content[x-1].isalpha()):
                                self.recorridoID.append(["q1", "q3", content[x], False ])
                            elif(content[x-1] == "_"):
                                self.recorridoID.append(["q2", "q3", content[x], False ])
                            else:
                                self.recorridoID.append(["q3", "q3", content[x], False ])
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
                 

    def lineComentary(self, posInicio, content):
        longitud = 0
        for i in range(posInicio, len(content)):
            
            if (content[i] == "\n"):
                size = self.counter + longitud
                self.addToken(self.row, self.column, 'ComentaryL', content[self.counter : size])
                #Buscando la linea del path
                if self.contadorUbicacion and "PATHW" in content[self.counter : size] :
                    self.ubicacionArchivo = content[self.counter : size]
                    self.contadorUbicacion = False
                self.counter = self.counter + longitud
                self.column = self.column + longitud 
                self.column = 1
                self.counter +=1
                self.row += 1
                longitud = 0
                break
            else:
                longitud += 1
                

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



    def getArrayErrors(self):
        return self.arrayErrores



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
        for x in self.arrayErrores:
            arrayTemp.append(x)

        #print("AREGLO TEMP" + str(arrayTemp))
        while counter < len(content):
            bandera = True
            for error in arrayTemp:
                #linea, columna, error
                if error[0] == line and error[1] == column:
                    #tamaño del error
                    #print("-------------")
                    #print("column actual: " + str(column))
                    size = len(error[2])
                    counter = counter + size
                    column = column + size
                    #print("ERROR: " + str(error))
                    #print("size: " + str(size))
                    #print("column: " + str(column))
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
        path = path + "new_file.js"
        file = open(path, "w")
        file.write(newContent)
        file.close()
        #os.system(path)