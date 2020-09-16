import os
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
        self.generarReporte()
        return self.arrayToken

    #Define como "Texto" a todo los que este entre ">" estas "<"" etiquetas
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

    #retorna la logitud del lexema para reconocer si es un ID
    def getSizeLexema(self, posInicio, content):
        longitud = 0
        for i in range(posInicio, len(content)): ## len(content)-1
            if (content[i].isalpha() or content[i].isnumeric()):
                longitud+=1
            else:
                break

        return longitud
    
    
    #retorna la logitud del lexema numerico
    def getSizeLexemaNumeric(self, posInicio, content):
        longitud = 0
        for i in range(posInicio, len(content)): ## len(content)-1
            if (content[i].isnumeric()): # or content[i].isalpha() si se coloca reconoce numero y luego las letras
                longitud+=1
            else:
                break
        return longitud
    

    #estado de numeros
    def stateNumero(self, sizeLexema, content):
        size = self.counter + sizeLexema
        self.addToken(self.row, self.column, 'int', content[self.counter : size])
        self.counter = self.counter + sizeLexema
        self.column = self.column + sizeLexema
        self.contadorRecorridoNumeric = False

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

    #Pasa de un estado ID a un estado de palabra reservada
    def wordReserved(self):
        for token in self.arrayToken:
            if token[2] == 'Id':
                for reservada in self.reservadas:
                    if token[3].lower() == reservada:
                        token[2] = "reservada"
                        break 

    #Agrega todo lo que este dentro del comentario
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

    #Metodo que genera el archivo corregido(sin errores lexicos)
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
        try:
            os.stat(path)
        except:
            os.mkdir(path)
        path = path.replace(" ", "") + "new_file.html"
        file = open(path, "w")
        file.write(newContent)
        file.close()

    #Metodo que genera el reporte de analisis lexico
    def generarReporte(self):
        contenido = ""
        contenido2 = ""
        contenido1 = "<!DOCTYPE html>\n<html>\n<head>\n<link rel=\"stylesheet\" href=\"https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css\" integrity=\"sha384-JcKb8q3iqJ61gNV9KGb8thSsNjpSL0n8PARn9HuZOnIxN0hoP+VmmDGMN5t9UJ0Z\" crossorigin=<\"anonymous\"><style>\ntable {\n font-family: arial, sans-serif;\nborder-collapse: collapse;\nwidth: 100%;\n}\ntd, th {\nborder: 1px solid #dddddd;\ntext-align: left;\npadding: 8px;\n}\ntr:nth-child(even) {\nbackground-color: #dddddd;\n}\n</style>\n</head>\n<body>\n<div class=\"jumbotron jumbotron-fluid\"><div class=\"container\"> <h1 class=\"display-4\">Reporte HTML</h1><p class=\"lead\">Cristian Gomez - 201801480</p></div></div> \n<table class=\"table\">\n<tr>\n<th>No.</th>\n<th>Linea</th>\n<th>Columna</th>\n<th>Error</th>\n</tr>\n"
        counter = 1
        for x in self.arrayError:
            contenido2 = contenido2 + "<tr>"+"<td>"+ str(counter) +"</td>"+"<td>"+ str(x[0]) +"</td>"+"<td>"+ str(x[1]) +"</td>"+"<td> El caracter \'"+ str(x[2]) +"\' no pertenece al lenguaje. </td>"+"</tr>\n"
            counter += 1

        contenido = contenido1 + contenido2 + "</table>\n" + "</body>\n" +"</html>\n"
        path = "REPORTE_HTML.html"
        file = open(path, "w")
        file.write(contenido)
        file.close()
        os.system(path)

    #Metodo para agregar tokens
    def addToken(self, row, column, content, word):
        self.arrayToken.append([row, column, content, word])
    #Metodo para agregar errores encontrados
    def addError(self, row, column, content):
        self.arrayError.append([row, column, content])

    #Metodo que retorna el arreglo de errores lexicos
    def getArrayError(self):
        return self.arrayError