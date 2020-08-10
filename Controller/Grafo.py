from Model.Arista import Arista
from Model.Vertice import Vertice
from collections import deque
from copy import copy

class Grafo:
    def __init__(self):
        self.listaVertices = []
        self.listaAristas = []
        self.listaVisitados = []

    def getListaVertices(self):
        return self.listaVertices

    def getListaAristas(self):
        return self.listaAristas

    def getListaVisitados(self):
        return self.listaVisitados

    def ingresarVertice(self, dato):
        if self.verificarVertice(dato) is None:
            self.listaVertices.append(Vertice(dato))

    def verificarVertice(self, dato):
        for vertice in self.listaVertices:
            if dato == vertice.getDato():
                return vertice
        return None

    def ingresarArista(self, origen, destino, peso):
        if self.verificarArista(origen, destino) is None:
            if self.verificarVertice(origen) is not None and self.verificarVertice(destino) is not None:
                self.listaAristas.append(Arista(origen, destino, peso))
                self.verificarVertice(origen).getListaAdyacentes().append(destino)

    def verificarArista(self, origen, destino):
        for arista in self.listaAristas:
            if arista.getOrigen() == origen and arista.getDestino() == destino:
                return arista
        return None

    def profundidad(self, dato):
        if dato in self.listaVisitados:
            return
        else:
            vertice = self.verificarVertice(dato)
            if vertice is not None:
                self.listaVisitados.append(vertice.getDato())
                for dato in vertice.getListaAdyacentes():
                    self.profundidad(dato)

    def amplitud(self, dato):
        visitadosA = []
        cola = deque()
        vertice = self.verificarVertice(dato)

        if vertice is not None:
            cola.append(vertice)
            visitadosA.append(dato)

        while cola:
            elemento = cola.popleft()
            for adyacencias in elemento.getListaAdyacentes():
                if adyacencias not in visitadosA:
                    vertice = self.verificarVertice(adyacencias)
                    cola.append(vertice)
                    visitadosA.append(adyacencias)
        return visitadosA

    def imprimirVertice(self):
        for vertice in self.listaVertices:
            print(vertice.getDato())

    def imprimirArista(self):
        for arista in self.listaAristas:
            print('Origen: {0} -- Destino: {1} -- Peso: {2}'.format(arista.getOrigen(), arista.getDestino(), arista.getPeso()))

    def imprimirListaAdyacentes(self):
        for vertice in self.listaVertices:
            print('Lista de adyacentes de ', vertice.getDato(), ': ', vertice.getListaAdyacentes())

    def separador(self):
        print()
        print('----------------------------------')
        print()

    def getPozos(self):
        nroPozos = 0
        for vertice in self.listaVertices:
            if len(vertice.getListaAdyacentes()) == 0:
                print('El vertice: ', vertice.getDato(), 'es un pozo')
                nroPozos += 1
        print('La cantidad de pozos del grafo es: ', nroPozos)
        return nroPozos

    def getFuentes(self):
        nroFuentes = 0
        bandera = False
        for vertice in self.listaVertices:
            for arista in self.listaAristas:
                if arista.getDestino() == vertice.getDato():
                        bandera = True
                if bandera != False:
                        break
            if bandera == False:
                print('El vertice:', vertice.getDato(), 'es una fuente')
                nroFuentes += 1
        print('La cantidad de fuentes del grafo es: ', nroFuentes)
        return nroFuentes

    def fuerteConexo(self):
        nroPozos = self.getPozos()
        nroFuentes = self.getFuentes()
        if nroPozos > 0 and nroFuentes > 0:
            print('El grafo es debilmente conexo')
            return True