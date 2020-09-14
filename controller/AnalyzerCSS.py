import os
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
        self.contadorUbicacion = True
        self.ubicacionArchivo = ""
        self.recorridoID = []

    def analizar(self, content):
        self.contadorUbicacion = True
        self.arrayError = []
        self.arrayToken = []
        self.row = 1
        self.column = 1
        self.counter = 0 
        self.recorridoID = []

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
                ## cargando transicion
                self.recorridoID.append(["--", "--", "--", "--"])
                self.recorridoID.append(["q0", "q1", symbol , False ])
                sizeLexema = self.getSizeLexema(self.counter, content)
                self.stateIdentificador(sizeLexema, content)
            elif (symbol.isnumeric()):
                self.recorridoID.append(["--", "--", "--", "--"])
                self.recorridoID.append(["q0", "q4", symbol , False ])
                sizeLexema = self.getSizeLexemaNumeric(self.counter, content)
                #if (sizeLexema != 0):
                self.stateNumero(sizeLexema, content)
                #else:
                #    sizeLexema = self.getSizeLexema(self.counter, content)
                #    self.addError(self.row, self.column, content[self.counter : self.counter + sizeLexema])
                #    self.counter = self.counter + sizeLexema
                #    self.column = self.column + sizeLexema
            elif (symbol == "-"):
                if (content[self.counter + 1].isnumeric()):
                    sizeLexema = self.getSizeLexemaNumeric(self.counter + 1, content)
                    #if (sizeLexema != 0):
                    self.stateNumero(sizeLexema + 1, content)
                    #else:
                    #    sizeLexema = self.getSizeLexema(self.counter, content)
                    #    self.addError(self.row, self.column, content[self.counter : self.counter + sizeLexema])
                    #    self.counter = self.counter + sizeLexema
                    #    self.column = self.column + sizeLexema
            elif ((symbol == "#" and content[self.counter + 1].isalpha()) or (symbol == '.' and content[self.counter + 1].isalpha())) :
                self.recorridoID.append(["--", "--", "--", "--"])
                self.recorridoID.append(["q0", "q2", symbol , False ])
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
                            self.recorridoID.append(["--", "--", "--", "--"])
                            self.recorridoID.append(["q0", "q7", tempSymbol , False ])
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
                    self.recorridoID.append(["TOKEN", " ", content[self.counter] , "NO aceptado" ])
                    self.column += 1
                    self.counter += 1

        ##palabras reservadas
        self.wordReserved()
        self.stateString()
        
        #print("Tokens")
        #for x in self.arrayToken:
        #    print(x)
        #print("-----------------------------------")
        self.generar_archivo_corregido(content)
        self.generarReporte()
        return self.arrayToken

        #estado de numeros
    def stateNumero(self, sizeLexema, content):
        size = self.counter + sizeLexema
        self.addToken(self.row, self.column, 'int', content[self.counter : size])
        self.recorridoID.append(["TOKEN", " ", content[self.counter : size], "Aceptado"])
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
                self.recorridoID.append(["q7", "q8", content[self.counter + 2 : size] , False ])
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
                self.recorridoID.append(["q8", "q9", "*/" , False ])
                self.recorridoID.append(["TOKEN", " ", content[self.counter : size], "Aceptado"])
                if self.contadorUbicacion and "PATHW" in content[self.counter : size] :
                    self.ubicacionArchivo = content[self.counter : size - 2]
                    self.contadorUbicacion = False
                self.counter = self.counter + longitud
                self.column = self.column + longitud 
                break
            else:
                longitud += 1


    def stateIdentificador(self, sizeLexema, content):
        size = self.counter + sizeLexema
        self.addToken(self.row, self.column, 'Id', content[self.counter : size])
        self.recorridoID.append(["TOKEN", " ", content[self.counter : size], "Aceptado"])
        self.counter = self.counter + sizeLexema
        self.column = self.column + sizeLexema

    # Para identificar selectores con . or #
    def stateSelector(self, sizeLexema, content):
        size = self.counter + sizeLexema
        self.addToken(self.row, self.column, 'Id', content[self.counter : size])
        self.recorridoID.append(["TOKEN", " ", content[self.counter : size], "Aceptado"])
        self.counter = self.counter + sizeLexema
        self.column = self.column + sizeLexema

    def getSizeLexema(self, posInicio, content):
        longitud = 0
        for i in range(posInicio, len(content)): ## len(content)-1
            if (content[i].isalpha() or content[i] == "_" or content[i] == "-" or
                content[i].isnumeric()):
                longitud+=1
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
            if (content[i].isnumeric() or content[i] == "."): 
                longitud+=1
                x = i
                x +=1
                if ((x - 1) != len(content)):
                    if (content[x].isnumeric()):
                        if (content[x - 1].isnumeric()):
                            self.recorridoID.append(["q4", "q4", content[x], False ])
                        else:
                            self.recorridoID.append(["q5", "q4", content[x], False ])
                    elif (content[x] == "."):
                        if (content[x - 1].isnumeric()):
                            self.recorridoID.append(["q4", "q5", content[x], False ])
                        else:
                            self.recorridoID.append(["q5", "q5", content[x], False ])


            #elif (content[i].isalpha()):
            #    if ((i + 2) != len(content)):
            #        valor = content[i: i + 2] 
            #        print(str(valor))
            #        if (valor == "px" or valor == "em" or valor == "vh" or valor == "vw" or
            #            valor == "in" or valor == "cm" or valor == "mm" or valor == "pt" or
            #            valor == "pc"):
            #            return longitud
            #        else: 
            #            return 0
            else:
                break

        return longitud 

    def wordReserved(self):
        for token in self.arrayToken:
            if token[2] == 'Id':
                for reservada in self.reservadas:
                    if token[3].lower() == reservada:
                        token[2] = "reservada"
                        #q0 -> q6
                        #id -> reservada
                        self.recorridoID.append(["q0", "q6", token[3], False ])
                        self.recorridoID.append(["TOKEN", " ", token[3], "Aceptado"])
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
                    self.recorridoID.append(["TOKEN", " ", x[3], "Aceptado"])
            ## rescatando de los errores
            for x in self.arrayError:
                if line[0] == x[0] and x[1] >= line[1] and x[1] <= line[2]:            
                    self.arrayToken.append([x[0], x[1], "COMILLA", x[2]])
                    self.arrayError.remove(x)

    def addToken(self, row, column, content, word):
        self.arrayToken.append([row, column, content, word])

    def addError(self, row, column, content):
        self.recorridoID.append(["TOKEN", " ", content, "NO aceptado" ])
        self.arrayError.append([row, column, content])
        return self.arrayError


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
        try:
            os.stat(path)
        except:
            os.mkdir(path)
        path = path.replace(" ", "") + "new_file.css"
        file = open(path, "w")
        file.write(newContent)
        file.close()


    def return_reorrido(self):
        return self.recorridoID


    def generarReporte(self):
        contenido = ""
        contenido2 = ""
        contenido1 = "<!DOCTYPE html>\n<html>\n<head>\n<link rel=\"stylesheet\" href=\"https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css\" integrity=\"sha384-JcKb8q3iqJ61gNV9KGb8thSsNjpSL0n8PARn9HuZOnIxN0hoP+VmmDGMN5t9UJ0Z\" crossorigin=<\"anonymous\"><style>\ntable {\n font-family: arial, sans-serif;\nborder-collapse: collapse;\nwidth: 100%;\n}\ntd, th {\nborder: 1px solid #dddddd;\ntext-align: left;\npadding: 8px;\n}\ntr:nth-child(even) {\nbackground-color: #dddddd;\n}\n</style>\n</head>\n<body>\n<div class=\"jumbotron jumbotron-fluid\"><div class=\"container\"> <h1 class=\"display-4\">Reporte CSS</h1><p class=\"lead\">Cristian Gomez - 201801480</p></div></div> \n<table class=\"table\">\n<tr>\n<th>No.</th>\n<th>Linea</th>\n<th>Columna</th>\n<th>Error</th>\n</tr>\n"
        counter = 1
        for x in self.arrayError:
            contenido2 = contenido2 + "<tr>"+"<td>"+ str(counter) +"</td>"+"<td>"+ str(x[0]) +"</td>"+"<td>"+ str(x[1]) +"</td>"+"<td> El caracter \'"+ str(x[2]) +"\' no pertenece al lenguaje. </td>"+"</tr>\n"
            counter += 1

        contenido = contenido1 + contenido2 + "</table>\n" + "</body>\n" +"</html>\n"
        path = "REPORTE_CSS.html"
        file = open(path, "w")
        file.write(contenido)
        file.close()
        os.system(path)

    def getArrayError(self):
        return self.arrayError