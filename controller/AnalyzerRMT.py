from controller.AnalyzerSinc import AnalyzerSinc

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

        self.signos = {"PAREA": '(', "PAREC": ')', "MAS": '+', "RESTA": '-', "POR": '*', "DIV": '/'}

        self.sintac = AnalyzerSinc()
        self.arrayLineas = [] #Lineas a analizar sintacticamente
        self.arrayReport = []
        self.banderaSintactico = False

    def analizar(self, content):
        self.banderaSintactico = False
        self.arrayToken = []
        self.arrayError = []
        self.arrayLineas = []
        self.arrayReport = []
        self.row = 1
        self.column = 1
        self.counter = 0
        #columna anteriror para validar
        self.tempCounter = 0

        while (self.counter < len(content)):
            symbol = content[self.counter]
            if (symbol == "\n"):
                #print(str(content[self.tempCounter:self.counter]))
                #agregando las lineas detectadas
                self.arrayLineas.append([self.row, content[self.tempCounter:self.counter]])
                self.counter += 1
                self.tempCounter = self.counter
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
        self.addToken(self.row, self.column, 'ID', content[self.counter : size])
        self.counter = self.counter + sizeLexema
        self.column = self.column + sizeLexema
        self.contadorRecorridoId = False

    #estado de numeros
    def stateNumero(self, sizeLexema, content):
        size = self.counter + sizeLexema
        if (content[self.counter : size].isnumeric() or '.' in content[self.counter : size]):
            self.addToken(self.row, self.column, 'NUM', content[self.counter : size])
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


    def comprobadorSintactico(self):
        #Estructura [#Linea, valor] 
        arrayTemp = []
        for x in self.arrayLineas:
            arrayTemp = []
            for z in self.arrayToken:
                #Linea = Linea
                if (x[0] ==  z[0]):
                    arrayTemp.append(z)
            parceo = self.sintac.parse(arrayTemp)
            if(parceo):
                self.arrayReport.append([x[0], x[1], "CORRECTO"])
            else:
                self.arrayReport.append([x[0], x[1], "INCORRECTO"])

        self.generarReporte()

    def getArrayReport(self):
        return self.arrayReport


    def addToken(self, row, column, content, word):
        self.arrayToken.append([row, column, content, word])

    def addError(self, row, column, content):
        self.arrayError.append([row, column, content])

    def getArrayError(self):
        return self.arrayError

    def generarReporte(self):
        contenido = ""
        contenido2 = ""
        contenido1 = "<!DOCTYPE html>\n<html>\n<head>\n<link rel=\"stylesheet\" href=\"https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css\" integrity=\"sha384-JcKb8q3iqJ61gNV9KGb8thSsNjpSL0n8PARn9HuZOnIxN0hoP+VmmDGMN5t9UJ0Z\" crossorigin=<\"anonymous\"><style>\ntable {\n font-family: arial, sans-serif;\nborder-collapse: collapse;\nwidth: 100%;\n}\ntd, th {\nborder: 1px solid #dddddd;\ntext-align: left;\npadding: 8px;\n}\ntr:nth-child(even) {\nbackground-color: #dddddd;\n}\n</style>\n</head>\n<body>\n<div class=\"jumbotron jumbotron-fluid\"><div class=\"container\"> <h1 class=\"display-4\">Reporte de Analisis Sintactico</h1><p class=\"lead\">Cristian Gomez - 201801480</p></div></div> \n<table class=\"table\">\n<tr>\n<th>No.</th>\n<th>Linea</th>\n<th>Operacion</th>\n<th>Analisis</th>\n</tr>\n"
        counter = 1
        for x in self.arrayReport:
            contenido2 = contenido2 + "<tr>"+"<td>"+ str(counter) +"</td>"+"<td>"+ str(x[0]) +"</td>"+"<td>"+ str(x[1]) +"</td>"+"<td>"+ str(x[2])+"</td>"+"</tr>\n"
            counter += 1

        contenido = contenido1 + contenido2 + "</table>\n" + "</body>\n" +"</html>\n"
        path = "REPORTE_RMT.html"
        file = open(path, "w")
        file.write(contenido)
        file.close()