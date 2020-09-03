from graphviz import Digraph

class Grafo:

    def __init__(self, nombre):
        self.nombre = nombre
        self.nodos = [] 
        self.nodos_aceptacion = []


    def agregarNodo(self, nodo):
        self.nodos.append(nodo)

    def obtenerNodo(self, nombre):
        for n in self.nodos:
            if n.nombre == nombre:
                return n

    def setearNodoAceptacion(self, nombre):
        self.nodos_aceptacion.append(self.obtenerNodo(nombre))

    def esAceptacion(self, nombre):
        for n in self.nodos_aceptacion:
            if n.nombre == nombre:
                return True
        
        return False

    def setEstadoInicial(self, nombre):
        self.obtenerNodo(nombre).inicial = True
    
    def getEstadoInicial(self):
        for n in self.nodos:
            if n.inicial:
                return n
        
        return None

    def graficar(self):
        f = Digraph(format='png', name="x")
        f.attr(rankdir='LR', size='8,5')
        f.attr('node', shape='circle')

        for n in self.nodos:
            
            if not self.esAceptacion(n.nombre):
                f.node(n.nombre)


        f.attr('node', shape='doublecircle')


        for n in self.nodos_aceptacion:
            f.node(n.nombre)

        for n in self.nodos:
            for a in n.lista_aristas:
                f.edge(n.nombre, a.nodo_final.nombre, label=a.valor)

        
        # ------------------ estado de aceptacion ------------------
        f.attr('node', shape='none')
        f.attr('edge', arrowhead='empty', arrowsize='1.5')
        
        f.edge('', self.getEstadoInicial().nombre, None)

        f.render()
        # ----------------------------------------------------------
        self.nodos = [] 
        self.nodos_aceptacion = []
