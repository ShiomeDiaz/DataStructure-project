class Vertice:
    def __init__(self, dato):
        self.dato = dato
        self.listaAdyacentes = []

    def getDato(self):
        return  self.dato

    def setDato(self, dato):
        self.dato = dato

    def getListaAdyacentes(self):
        return  self.listaAdyacentes

    def setListaAdyacentes(self, listaAdyacentes):
        self.listaAdyacentes = listaAdyacentes