from bean.Grafo import Grafo

class GraphGenerator():
    __instance = None

    def __new__(self):
        if not self.__instance:
            self.__instance = super(GraphGenerator, self).__new__(self)
        return self.__instance

    def __init__(self):
        self.__grafo = Grafo("G1")
        self.arrayEstado = []

    def graphJS(self, array):
        self.__grafo = Grafo('g1')
        self.arrayEstado = []

        for x in array:
            if (self.estadoRepetido(x[0])):
                self.arrayEstado.append(x[0])
            if (self.estadoRepetido(x[1])):
                self.arrayEstado.append(x[1])

        for x in self.arrayEstado:
            self.__grafo.agregarNodo(Nodo(x))

        for w in array:                
            self.__grafo.obtenerNodo(str(w[0])).crearArista(self.__grafo.obtenerNodo(str(w[1])), str(w[2])) 
            #print(w)

        # Estado Incial
        self.__grafo.setEstadoInicial("q0")

        # Estado de aceptacion
        for w in array:   
            if (w[3]):
                #print("Aceptacion: " + str(w[0]))
                if (str(w[0]) != "q6" and str(w[0]) != "q7"):
                    self.__grafo.setearNodoAceptacion(str(w[0]))
            else:
                #print("Aceptacion: " + str(w[1]))
                self.__grafo.setearNodoAceptacion(str(w[1]))

        self.__grafo.graficar()

    # si no lo encuentro, lo agrego
    def estadoRepetido(self, state):
        for x in self.arrayEstado:
            if (x == state):
                return False
        return True

class Nodo:
    def __init__(self, nombre):
        self.nombre = nombre
        self.lista_aristas = []
        self.inicial = False

    def crearArista(self, nodo_final, valor):
        self.lista_aristas.append(Arista(self, nodo_final, valor))

class Arista:
    def __init__(self, inicial, final, valor):
            self.nodo_inicial = inicial
            self.nodo_final = final
            self.valor = valor