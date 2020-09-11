class AnalyzerSinc():
    __instance = None

    def __new__(self):
        if not self.__instance:
            self.__instance = super(AnalyzerSinc, self).__new__(self)
        return self.__instance

    def __init__(self):
        self.counter = 0
        self.tabla = { 
            'E' : { 'PAREA' : "XT", 'NUM' : "XT", "ID" : 'XT'},

            'X' : { 'MAS' : "XT+", 'RESTA' : "XT-",'PAREC' : None, '$' : None }, #X = E

            'T' : { 'PAREA' : "ZF", 'NUM' : "ZF", 'ID': "ZF" },

            'Z' : { 'POR' : "ZF*", 'DIV' : "ZF/", 'MAS' : None, 'RESTA' : None, 'PAREC' : None, '$' : None }, #Z = T'
            
            'F' : { 'PAREA' : ")E(", 'NUM' : "i", 'ID' : "N" } #NUMERIC = i
            }
        self.pila = ['$','E'] #EOF, produccion inicial
        self.Errores = []

    def obtenerMatrix(self, produccion, token):
        try:
            print("-------------------->" + str(self.tabla[produccion][token]))
            return self.tabla[produccion][token]
        except:#AQUI SE MANEJARIAN LOS ERRORES :D
            #print("ERROR SINTACTICO")
            return "ERROR"
    
    def pushear(self, producciones):
        lista = list(producciones)
        for l in lista:
            if l == "(":
                self.pila.append('PAREA')
            elif l == ")":
                self.pila.append('PAREC')
            elif l == "i":
                self.pila.append('NUM')
            elif l == "N":
                self.pila.append('ID')
            elif l == "+":
                self.pila.append('MAS')
            elif l == "*":
                self.pila.append('POR')
            elif l == "-":
                self.pila.append('RESTA')
            elif l == "/":
                self.pila.append('DIV')
            else:
                self.pila.append(l)

    def parse(self,tokens):
        self.pila = []
        self.pila = ['$','E'] #EOF, produccion inicial
        tokens.append([0,0,'$',0])
        while len(self.pila) -1 >= 0:
            self.counter = len(self.pila) -1
            var1 = self.pila[self.counter]  
            var2 = tokens[0][2]           
            if var1 == var2:
                if var1 == "$":
                    #pila
                    #print(self.pila)
                    #Bufer
                    #print(tokens)
                    #final
                    return True
                elif var1 == "NUM" or var1 == "ID" or var1 == "PAREA" or var1 == "PAREC" or var1 == "MAS" or var1 == "POR" or var1 == "RESTA" or var1 == "DIV":
                    self.pila.pop()
                    del tokens[0]
                    #print("*******************PILA***************************")
                    #print(self.pila)
                    #print("***************************************************")
                    #print(tokens)
            else:
                self.pila.pop() 
                val = self.obtenerMatrix(var1, var2)
                
                if val == "ERROR":
                    return False
                elif val != None:
                    self.pushear(val)
                #print("**********************PILA*******************************")
                #print(self.pila)
                #print("*********************************************************")
                #print(tokens)
