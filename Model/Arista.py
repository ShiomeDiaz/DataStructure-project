class Arista:
    def __init__(self, origen, destino, peso):
        self.origen = origen
        self.destino = destino
        self.peso = peso

    def getOrigen(self):
        return self.origen

    def setOrigen(self, origen):
        self.origen = origen

    def getDestino(self):
        return self.destino

    def setDestino(self, destino):
        self.destino = destino

    def getPeso(self):
        return self.peso

    def setPeso(self, peso):
        self.peso = peso
