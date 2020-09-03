from bean.Grafo import Grafo

class GraphGenerator():
    __instance = None

    def __new__(self):
        if not self.__instance:
            self.__instance = super(GraphGenerator, self).__new__(self)
        return self.__instance

    def __init__(self):
        self.__grafo = Grafo("G1")

    def graphJS(self, array):
        self.__grafo = Grafo('g1')

        arrayEstado = []
        arrayEstado.append("q0")
        arrayEstado.append("q1")
        for x in arrayEstado:
            self.__grafo.agregarNodo(Nodo(x))

        for w in array:
            if w[2] == "Id":
                counter = 0
                while (counter < len(str(w[3]))):
                    if counter == 0 :
                        x = "q0"
                    else:
                        x = "q1"
                    y = "q1"
                    self.__grafo.obtenerNodo(x).crearArista(self.__grafo.obtenerNodo(y), str(w[3])[counter]) 
                    counter = counter + 1           
        # Estado Incial
        self.__grafo.setEstadoInicial("q0")

        # Estado de aceptacion
        self.__grafo.setearNodoAceptacion("q1")

            
        self.__grafo.graficar()


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