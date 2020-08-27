import pygame
import os
from Controller.Grafo import Grafo
from pygame.locals import *


class animacion:
    def __init__(self,grafo):
        self.corriendo = True
        self.pantalla = None
        self.fondo = None
        self.fuente = None
        self.vertice = None
        self.camion=None
        self.empresa=None
        self.montaña=None
        self.grafo=grafo
        self.size = self.weight, self.height = 1270, 670
        self.ubicacion_actual = os.path.dirname(__file__)  # Where your .py file is located
        self.ubicacion_imagen = os.path.join(self.ubicacion_actual, 'imagenes')  # The image folder path

    def iniciar(self):
        pygame.init()
        pygame.display.set_caption('Montaña  Acme')
        self.montaña = pygame.image.load(os.path.join(self.ubicacion_imagen, 'montaña.png'))
        pygame.display.set_icon(self.montaña)
        self.pantalla = pygame.display.set_mode(self.size)
        self.corriendo = True
        self.fondo = pygame.image.load(os.path.join(self.ubicacion_imagen, 'fondo.jpg'))
        self.camion = pygame.image.load(os.path.join(self.ubicacion_imagen, 'camion.png'))
        self.empresa = pygame.image.load(os.path.join(self.ubicacion_imagen, 'empresa.png'))
        self.vertice = pygame.image.load(os.path.join(self.ubicacion_imagen, 'cueva.png'))
        self.fuente = pygame.font.Font(None, 30)

    def evento(self, evento):
        if evento.type == pygame.QUIT:
            self.corriendo = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                self.corriendo = False
            if evento.key == pygame.K_1:
                self.agregar_cueva()

    def on_loop(self):
        pass

    def mostrar(self):
        self.pantalla.blit(self.fondo, (0, 0))
        self.pantalla.blit(self.empresa, (25,165))
        self.pantalla.blit(self.camion,(200,225))
        lista=[]
        lista=self.cuevas(self.grafo.getListaVertices(),270,100,0,0,lista)
        self.carreteras(lista,self.grafo.getListaAristas(),0)
        pygame.display.flip()

    def cuevas(self,vertices,x,y,contador,posicion,lista):
        if posicion < len(vertices):
            if contador < 3:
                self.pantalla.blit(self.fuente.render(vertices[posicion].getDato(), True,(255, 255, 255)), (x+60, y-30))
                self.pantalla.blit(self.vertice, (x, y))
                lista.append({'Nombre' : vertices[posicion].getDato(), 'x' : x, 'y' : y } )
                return self.cuevas(vertices,x,y+130,contador+1,posicion+1,lista)
            else:
                y=100
                return self.cuevas(vertices,x+270,y,contador-contador,posicion,lista)
        else:
            return lista

    def carreteras(self,lista,aristas,posicion):
        if posicion < len(aristas):
            posicion_inicial = None
            posicion_final = None
            for diccionario in lista:
                if diccionario['Nombre'] == aristas[posicion].getOrigen():
                    posicion_inicial = (diccionario['x']+45, diccionario['y']+10)
                if diccionario['Nombre'] == aristas[posicion].getDestino():
                    posicion_final = (diccionario['x']+45, diccionario['y']+10)
                color = (155, 155, 155)
                width = 9
                if posicion_inicial and posicion_final != None:
                    pygame.draw.line(self.fondo, color, posicion_inicial, posicion_final, width)
                    return self.carreteras(lista,aristas,posicion+1)
        else:
            return

    def agregar_cueva(self,x,y,dato,grafo):
        self.pantalla.blit(self.fuente.render(dato, True, (255, 255, 255)), (x + 75, y - 53))
        self.pantalla.blit(self.vertice, (x, y))
        grafo.agregar_vertice(dato)


    def salir(self):
        pygame.quit()

    def ejecutar(self):
        if self.iniciar() == False:
            self.corriendo = False

        while (self.corriendo):
            for event in pygame.event.get():
                self.evento(event)
            self.on_loop()
            self.mostrar()
        self.salir()

