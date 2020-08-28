import pygame
from Model.Arista import Arista
from Model.Vertice import Vertice
from collections import deque
from copy import copy
import json
class Grafo:
    def __init__(self):
        self.listaVertices = []
        self.listaAristas = []
        self.listaVisitados = []
        self.listaBloqueadas = []

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

    def profundidad(self,posicion,lista_visitados):
        if self.verificarVertice(posicion):
            if not lista_visitados:
                lista_visitados.append(posicion)
            for adyacente in self.verificarVertice(posicion).getListaAdyacentes():
                if adyacente not in lista_visitados:
                    lista_visitados.append(adyacente)
                    lista_visitados=self.profundidad(adyacente,lista_visitados)
            return lista_visitados
        else:
            return "El vertice señalado para iniciar el recorrido no existe"

    """def profundidad(self, dato):
        if dato in self.listaVisitados:
            return
        else:
            vertice = self.verificarVertice(dato)
            if vertice is not None:
                self.listaVisitados.append(vertice.getDato())
                for dato in vertice.getListaAdyacentes():
                    self.profundidad(dato)
    """
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

    def ordenamiento(self, copiaAristas): # Ordeno de menor a mayor
        for i in range(len(copiaAristas)):
            for j in range(len(copiaAristas)):
                if copiaAristas[i].getPeso() < copiaAristas[j].getPeso():
                    temp = copiaAristas[i]
                    copiaAristas[i] = copiaAristas[j]
                    copiaAristas[j] = temp

    def prim(self):
        copiaAristas = copy(self.listaAristas)
        conjunto = [] # se va encargar de guardar los vertices visitados
        aristasPrim = []
        aristasTemp = []
        self.ordenamiento(copiaAristas)
        self.dirigido(copiaAristas)
        menor = copiaAristas[0]
        conjunto.append(menor.getOrigen())
        terminado = False
        while terminado == False:
            for vertice in conjunto:
                self.algoritmoPrim(copiaAristas, conjunto, aristasPrim, aristasTemp, vertice)
            if len(self.listaVertices) == len(conjunto):
                terminado = True
        print(conjunto)
        for arista in aristasPrim:
            print('Origen: {0} - Destino: {1} - Peso: {2}'.format(arista.getOrigen(), arista.getDestino(), arista.getPeso()))
        return aristasPrim

    def algoritmoPrim(self, copiaAristas, conjunto, aristasPrim, aristasTemp, vertice):
        ciclo = False
        self.agregarTemp(copiaAristas, aristasTemp, vertice)
        candidata = self.candidataPrim(aristasTemp, copiaAristas, aristasPrim)
        if candidata != None:
            if candidata.getOrigen() in conjunto and candidata.getDestino() in conjunto:
                ciclo = True
            if ciclo == False:
                aristasPrim.append(candidata)
                if not candidata.getOrigen() in conjunto:
                    conjunto.append(candidata.getOrigen())
                if not candidata.getDestino() in conjunto:
                    conjunto.append(candidata.getDestino())

    def agregarTemp(self, copiaAristas, aristasTemp, vertice):
        for arista in copiaAristas:
            if arista.getOrigen() == vertice or arista.getDestino() == vertice:
                if self.verificarAristaTemp(arista, aristasTemp):
                    aristasTemp.append(arista)

    def verificarAristaTemp(self, arista, aristasTemp):
        for elemento in aristasTemp:
            if elemento.getOrigen() == arista.getOrigen() and elemento.getDestino() == arista.getDestino():
                return False
        return True

    def candidataPrim(self, aristasTemp, copiaAristas, aristasPrim):
        menor = copiaAristas[len(copiaAristas) - 1]
        for i in range(len(aristasTemp)):
            if aristasTemp[i].getPeso() < menor.getPeso():
                if self.verificarPrim(aristasTemp[i], aristasPrim):
                    menor = aristasTemp[i]
        aristasTemp.pop(aristasTemp.index(menor))
        return menor

    def verificarPrim(self, candidata, aristasPrim):
        for arista in aristasPrim:
            if arista.getOrigen() == candidata.getOrigen() and arista.getDestino() == candidata.getDestino():
                return False
            if arista.getDestino() == candidata.getDestino() and arista.getOrigen() == candidata.getOrigen():
                return False
        return True

    def dirigido(self, copiaAristas):
        for elemento in copiaAristas:
            for i in range(len(copiaAristas)):
                if elemento.getOrigen() == copiaAristas[i].getDestino() and elemento.getDestino() ==  copiaAristas[i].getOrigen():
                    copiaAristas.pop(i)
                    break

    def noDirigido(self, copiaAristas):
        dirigido = False
        for elemento in copiaAristas:
            for i in range(len(copiaAristas)):
                if elemento.getOrigen() == copiaAristas[i].getDestino() and elemento.getDestino() == copiaAristas[i].getOrigen():
                    dirigido = True
            if dirigido == False:
                copiaAristas.append(Arista(elemento.getDestino(),elemento.getOrigen(),elemento.getPeso()))

    def Kruskal(self):
        copiaAristas = copy(self.getListaAristas())  # copia de las aristas
        AristasKruskal = []
        ListaConjuntos = []

        self.ordenamiento(copiaAristas)  # ordeno las aristas
        for menor in copiaAristas:
            self.Operacionesconjuntos(menor, ListaConjuntos, AristasKruskal)
        # esta ordenada de mayor a menor
        print("-----------Kruskal---------------")
        for dato in AristasKruskal:
            print("Origen: {0} destino: {1} peso: {2}".format(dato.getOrigen(), dato.getDestino(), dato.getPeso()))
        return AristasKruskal
    def Operacionesconjuntos(self, menor, ListaConjuntos, AristasKruskal):
        encontrado1 = -1
        encontrado2 = -1

        if not ListaConjuntos:  # si esta vacia
            ListaConjuntos.append({menor.getOrigen(), menor.getDestino()})
            AristasKruskal.append(menor)

        else:
            for i in range(len(ListaConjuntos)):
                if (menor.getOrigen() in ListaConjuntos[i]) and (menor.getDestino() in ListaConjuntos[i]):
                    return  ##Camino cicliclo

            for i in range(len(ListaConjuntos)):
                if menor.getOrigen() in ListaConjuntos[i]:
                    encontrado1 = i
                if menor.getDestino() in ListaConjuntos[i]:
                    encontrado2 = i

            if encontrado1 != -1 and encontrado2 != -1:
                if encontrado1 != encontrado2:  # si pertenecen a dos conjuntos diferentes
                    # debo unir los dos conjuntos
                    ListaConjuntos[encontrado1].update(ListaConjuntos[encontrado2])
                    #este update si funciona correctemente
                    ListaConjuntos[encontrado2].clear()  # elimino el conjunto
                    AristasKruskal.append(menor)

            if encontrado1 != -1 and encontrado2 == -1:  # si va unido por un conjunto
                # el update se cambio con por el add ya que al agregar cadenas a Listaconjuntos
                # no se guardaba como "Silvestre" sino que la desglosaba en sus caracteres "S,i,l,v,e,t,r,e" en Listaconjuntos
                ListaConjuntos[encontrado1].add(menor.getOrigen())
                ListaConjuntos[encontrado1].add(menor.getDestino())
                AristasKruskal.append(menor)

            if encontrado1 == -1 and encontrado2 != -1:  # si va unido por un conjunto
                ListaConjuntos[encontrado2].add(menor.getOrigen())
                ListaConjuntos[encontrado2].add(menor.getDestino())
                AristasKruskal.append(menor)

            if encontrado1 == -1 and encontrado2 == -1:  # si no existe en los conjuntos
                ListaConjuntos.append({menor.getOrigen(), menor.getDestino()})
                AristasKruskal.append(menor)

    def Boruvka(self):
        copiaNodos = copy(self.getListaVertices())  # copia de los nodos
        copiaAristas = copy(self.getListaAristas())  # copia de las aristas

        AristasBorukvka = []
        ListaConjuntos = []
        bandera = True
        cantidad = 0
        while(cantidad > 1 or bandera):
            for Nodo in copiaNodos:
                self.OperacionesconjuntosB(Nodo, ListaConjuntos, AristasBorukvka,copiaAristas)
            bandera = False
            cantidad = self.Cantidadconjuntos(ListaConjuntos)

        for dato in AristasBorukvka:
            print("Origen: {0} destino: {1} peso: {2}".format(dato.getOrigen(), dato.getDestino(), dato.getPeso()))
        return AristasBorukvka

    def Cantidadconjuntos(self,ListaConjuntos):
        cantidad = 0
        for conjunto in ListaConjuntos:
            if len(conjunto) > 0:
                catidad = cantidad + 1
        return cantidad
    def OperacionesconjuntosB(self,Nodo, ListaConjuntos, AristasBorukvka,copiaAristas):
        encontrado1 = -1
        encontrado2 = -1
        menor = self.Buscarmenor(Nodo, copiaAristas)

        if not menor==None:#si no esta vacio
            if not ListaConjuntos:#si esta vacia
                ListaConjuntos.append({menor.getOrigen(),menor.getDestino()})
                AristasBorukvka.append(menor)
            else:
                for i in range(len(ListaConjuntos)):
                    if  (menor.getOrigen()  in ListaConjuntos[i]) and (menor.getDestino() in ListaConjuntos[i]):
                        return False##Camino cicliclo

                for i in range(len(ListaConjuntos)):
                    if menor.getOrigen() in ListaConjuntos[i]:
                        encontrado1 = i
                    if menor.getDestino() in ListaConjuntos[i]:
                        encontrado2 = i

                if encontrado1!=-1 and encontrado2!=-1:
                    if encontrado1!=encontrado2:#si pertenecen a dos conjuntos diferentes
                        #debo unir los dos conjuntos
                        ListaConjuntos[encontrado1].update(ListaConjuntos[encontrado2])
                        ListaConjuntos[encontrado2].clear()#elimino el conjunto
                        AristasBorukvka.append(menor)

                if encontrado1!=-1 and encontrado2==-1:# si va unido por un conjunto
                    ListaConjuntos[encontrado1].update(menor.getOrigen())
                    ListaConjuntos[encontrado1].update(menor.getDestino())
                    AristasBorukvka.append(menor)

                if encontrado1 == -1 and encontrado2 != -1:# si va unido por un conjunto
                    ListaConjuntos[encontrado2].update(menor.getOrigen())
                    ListaConjuntos[encontrado2].update(menor.getDestino())
                    AristasBorukvka.append(menor)

                if encontrado1 == -1 and encontrado2 == -1:# si no existe en los conjuntos
                    ListaConjuntos.append({menor.getOrigen(), menor.getDestino()})
                    AristasBorukvka.append(menor)



    def Buscarmenor(self,Nodo,copiaAristas):
        temp = []
        for adyacencia in Nodo.getListaAdyacentes():
            for Arista in copiaAristas:
                #busco las aristas de esa lista de adyacencia
                if Arista.getOrigen()==Nodo.getDato() and Arista.getDestino()==adyacencia:
                    temp.append(Arista)
        if temp:#si no esta vacia
            #una vez obtenga todas las aristas, saco la menor
            self.ordenamiento(temp)  # ordeno las aristas
            #elimin ese destino porque ya lo voy a visitar
            #print("{0}-{1}:{2}".format(temp[0].getOrigen(), temp[0].getDestino(), temp[0].getPeso()))

            Nodo.getListaAdyacentes().remove(temp[0].getDestino())
            return temp[0]  # es la menor

        return None#es la menor

    def cambiarDireccion(self, origen, destino):
        for arista in self.listaAristas:
            origenCopia = str(arista.getOrigen())
            destinoCopia = str(arista.getDestino())
            if origen == origenCopia and destino == destinoCopia:
                temp = arista.getOrigen()
                arista.setOrigen(arista.getDestino())
                arista.setDestino(temp)

    def bloquearArista(self, origen, destino):
        for arista in self.listaAristas:
            origenCopia = str(arista.getOrigen())
            destinoCopia = str(arista.getDestino())
            if origen == origenCopia and destino == destinoCopia:
                self.listaBloqueadas.append(arista)
                indice = self.listaAristas.index(arista)
                self.listaAristas.pop(indice)

    def desbloquearArista(self, origen, destino):
        for arista in self.listaBloqueadas:
            origenCopia = str(arista.getOrigen())
            destinoCopia = str(arista.getDestino())
            if origen == origenCopia and destino == destinoCopia:
                self.listaAristas.append(arista)
                indice = self.listaBloqueadas.index(arista)
                self.listaBloqueadas.pop(indice)

    def gradoVertice(self, vertice):
        gradoVertice = 0
        verticeEntrada = self.verificarVertice(vertice)
        copiaAristas = copy(self.listaAristas)
        self.noDirigido(self.listaAristas)
        for vertice in self.listaVertices:
            if vertice == verticeEntrada:
                gradoVertice = len(vertice.getListaAdyacentes())
        self.listaAristas = copiaAristas
        return gradoVertice

    def caminoMasCorto(self, origen, destino):
        VerticesAux = []
        VerticesD = []
        caminos = self.dijkstra(origen, VerticesAux)
        cont = 0
        for i in caminos:
            print("La distancia mínima a: " + self.listaVertices[cont].getDato() + " es " + str(i))
            cont = cont + 1
        self.rutas(VerticesD, VerticesAux, destino, origen)
        print("El camino más corto de: " + origen + " a " + destino + " es: ")
        print(VerticesD)

    def rutas(self, VerticesD, VerticesAux, destino, origen):
        verticeDestino = self.verificarVertice(destino)
        indice = self.listaVertices.index(verticeDestino)
        if VerticesAux[indice] is None:
            print("No hay camino entre: ", (origen, destino))
            return
        aux = destino
        while aux is not origen:
            verticeDestino = self.verificarVertice(aux)
            indice = self.listaVertices.index(verticeDestino)
            VerticesD.insert(0, aux)
            aux = VerticesAux[indice]
        VerticesD.insert(0, aux)

    def dijkstra(self, origen, VerticesAux):
        marcados = []  # la lista de los que ya hemos visitado
        caminos = []  # la lista final
        # iniciar los valores en infinito
        for v in self.listaVertices:
            caminos.append(float("inf"))
            marcados.append(False)
            VerticesAux.append(None)
            if v.getDato() is origen:
                caminos[self.listaVertices.index(v)] = 0
                VerticesAux[self.listaVertices.index(v)] = v.getDato()
        while not self.todosMarcados(marcados):
            aux = self.menorNoMarcado(caminos, marcados)  # obtuve el menor no marcado
            if aux is None:
                break
            indice = self.listaVertices.index(aux)  # indice del menor no marcado
            marcados[indice] = True  # marco como visitado
            valorActual = caminos[indice]
            for vAdya in aux.getListaAdyacentes():
                indiceNuevo = self.listaVertices.index(self.verificarVertice(vAdya))
                arista = self.verificarArista(vAdya, aux.getDato())
                if caminos[indiceNuevo] > valorActual + arista.getPeso():
                    caminos[indiceNuevo] = valorActual + arista.getPeso()
                    VerticesAux[indiceNuevo] = self.listaVertices[indice].getDato()
        return caminos

    def menorNoMarcado(self, caminos, marcados):
        verticeMenor = None
        caminosAux = sorted(caminos)
        copiacaminos = copy(caminos)
        bandera = True
        contador = 0
        while bandera:
            menor = caminosAux[contador]
            if marcados[copiacaminos.index(menor)] == False:
                verticeMenor = self.listaVertices[copiacaminos.index(menor)]
                bandera = False
            else:
                copiacaminos[copiacaminos.index(menor)] = "x"
                contador = contador + 1
        return verticeMenor

    def todosMarcados(self, marcados):
        for j in marcados:
            if j is False:
                return False
        return True

    def cargarRedInicial(self, ruta):
        with open(ruta) as contenido:
            redAcme = json.load(contenido)
        for vertice in redAcme["Cuevas"]:
            self.ingresarVertice(vertice)
        for arista in redAcme["Caminos"]:
            self.ingresarArista(arista[0], arista[1], arista[2])
        self.noDirigido(self.listaAristas)

    def dibujarTabla(self, x, y, ventana, aguaMarina = pygame.Color(14, 236, 125), blanco = pygame.Color(255, 255, 255), negro = pygame.Color(0, 0, 0)):
        contador = 0
        pygame.draw.rect(ventana, aguaMarina, (x - 200, 0, 400, 30))
        pygame.draw.rect(ventana, blanco, (x - 200, 30, 400, y - 30))
        miFuente = pygame.font.Font(None, 23)
        miTexto = miFuente.render('LISTA ARISTAS', 0, blanco)
        ventana.blit(miTexto, (x - 195, 8))
        for arista in self.listaAristas:
            miTexto1 = miFuente.render(
                '{} - {} - {}'.format(arista.getOrigen(), arista.getDestino(), arista.getPeso()), 0, negro)
            ventana.blit(miTexto1, (x - 195, 35 + contador))
            contador += 25
        pygame.draw.rect(ventana, aguaMarina, (x - 200, 0 + contador + 35, 400, 30))
        miTexto = miFuente.render('LISTA BLOQUEADAS', 0, blanco)
        ventana.blit(miTexto, (x - 195, 8 + 35 + contador))
        for bloqueada in self.listaBloqueadas:
            miTexto1 = miFuente.render(
                '{} - {} - {}'.format(bloqueada.getOrigen(), bloqueada.getDestino(), bloqueada.getPeso()), 0, negro)
            ventana.blit(miTexto1, (x - 195, 40 + 35 + contador))
            contador += 25

    def dibujarResultado(self, x, y, ventana,texto, blanco = pygame.Color(255, 255, 255), negro = pygame.Color(0, 0, 0)):
        pygame.draw.rect(ventana, blanco, ((x/2)/ 2, y - 150, 800, y - 100))
        miFuente = pygame.font.Font(None, 30)
        neuvoTexto = str(texto)
        miTexto = miFuente.render(neuvoTexto, 0, negro)
        ventana.blit(miTexto, (((x/2)/2) + 25, y - 50))

    def cambiarDireccion(self, origen, destino):
        for arista in self.listaAristas:
            origenCopia = str(arista.getOrigen())
            destinoCopia = str(arista.getDestino())
            if origen == origenCopia and destino == destinoCopia:
                temp = arista.getOrigen()
                arista.setOrigen(arista.getDestino())
                arista.setDestino(temp)

    def bloquearArista(self, origen, destino):
        for arista in self.listaAristas:
            origenCopia = str(arista.getOrigen())
            destinoCopia = str(arista.getDestino())
            if origen == origenCopia and destino == destinoCopia:
                self.listaBloqueadas.append(arista)
                indice = self.listaAristas.index(arista)
                self.listaAristas.pop(indice)

    def desbloquearArista(self, origen, destino):
        for arista in self.listaBloqueadas:
            origenCopia = str(arista.getOrigen())
            destinoCopia = str(arista.getDestino())
            if origen == origenCopia and destino == destinoCopia:
                self.listaAristas.append(arista)
                indice = self.listaBloqueadas.index(arista)
                self.listaBloqueadas.pop(indice)

    def gradoVertice(self, vertice):
        gradoVertice = 0
        verticeEntrada = self.verificarVertice(vertice)
        copiaAristas = copy(self.listaAristas)
        self.noDirigido(self.listaAristas)
        for vertice in self.listaVertices:
            if vertice == verticeEntrada:
                gradoVertice = len(vertice.getListaAdyacentes())
        self.listaAristas = copiaAristas
        return gradoVertice
