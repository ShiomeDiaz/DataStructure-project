
import pygame as pg
import pygame
import os
from Controller.Grafo import Grafo
from pygame.locals import *

from Controller.Methods import *



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
        self.seleccion = ""
        self.texto = ""
        self.x = None
        self.y = None

        self.lista = []
        self.grafo=grafo
        self.size = self.weight, self.height = 1466, 768 #1270, 670
        self.ubicacion_actual = os.path.dirname(__file__)  # Where your .py file is located
        self.ubicacion_imagen = os.path.join(self.ubicacion_actual, 'imagenes')  # The image folder path
        self.cursor = None
        self.ColorActive = None
        self.ColorInactive = None
        self.Font = None

        self.clock = None
        self.lista_cuevas = []
        self.lista_carreteras = []




    def iniciar(self):
        pygame.init()
        pygame.display.set_caption('Montaña  Acme')

        self.clock=pygame.time.Clock()

        self.montaña = pygame.image.load(os.path.join(self.ubicacion_imagen, 'montaña.png'))
        pygame.display.set_icon(self.montaña)
        self.pantalla = pygame.display.set_mode(self.size)
        self.corriendo = True
        self.fondo = pygame.image.load(os.path.join(self.ubicacion_imagen, 'fondo.jpg'))
        self.camion = pygame.image.load(os.path.join(self.ubicacion_imagen, 'camion.png'))
        self.empresa = pygame.image.load(os.path.join(self.ubicacion_imagen, 'empresa.png'))
        self.vertice = pygame.image.load(os.path.join(self.ubicacion_imagen, 'cueva.png'))
        self.fuente = pygame.font.Font(None, 30)

        self.cursor=Cursor()
        self.ColorActive = pygame.Color('lightskyblue3')#color del cuadro de texto
        self.ColorInactive = pygame.Color('dodgerblue2')#color del cuadro de texto
        self.Font = pygame.font.Font(None, 32)#fuente en el que se va a escribir


    def evento(self, evento):
        if evento.type == pygame.QUIT:
            self.corriendo = False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                self.corriendo = False

            if self.seleccion == "Profundidad":
                if evento.key == pygame.K_0:

                    self.profundidad(self.texto)

                    self.kruskal()
                    #self.profundidad(self.texto)

                else:
                    self.texto = self.texto + evento.unicode

        if evento.type == MOUSEBUTTONDOWN:
            x_mouse, y_mouse = pygame.mouse.get_pos()
            if 20 <= x_mouse <= 170 and 315 <= y_mouse <= 350:
                self.seleccion = "Profundidad"

    def on_loop(self):
        pass

    def kruskal(self):
        lista=[]
        lista = self.grafo.Kruskal()
        for i in range(0,len(lista)):
            for diccionario in self.lista_carreteras:
                if lista[i].getOrigen() == diccionario['inicio'] and lista[i].getDestino() == diccionario['final']:
                    color = (255, 0, 0)
                    width = 9
                    pygame.draw.line(self.fondo, color, diccionario['arranque'], diccionario['termino'], width)
                    pygame.display.flip()
                    break
    def prim(self):
        lista=[]
        lista = self.grafo.prim()
        for i in range(0,len(lista)):
            for diccionario in self.lista_carreteras:
                if lista[i].getOrigen() == diccionario['inicio'] and lista[i].getDestino() == diccionario['final']:
                    color = (255, 0, 0)
                    width = 9
                    pygame.draw.line(self.fondo, color, diccionario['arranque'], diccionario['termino'], width)
                    pygame.display.flip()
                    break

    def boru(self):
        lista=[]
        lista = self.grafo.Boruvka()
        for i in range(0,len(lista)):
            for diccionario in self.lista_carreteras:
                if lista[i].getOrigen() == diccionario['inicio'] and lista[i].getDestino() == diccionario['final']:
                    color = (255, 0, 0)
                    width = 9
                    pygame.draw.line(self.fondo, color, diccionario['arranque'], diccionario['termino'], width)
                    pygame.display.flip()
                    break

    def profundidad(self, inicio):
        lista = []
        lista = self.grafo.profundidad(inicio, lista)


        for i in range(0,len(lista)):
            for diccionario in self.lista_cuevas:
                if diccionario['Nombre'] == lista[i]:

                    self.x = diccionario['x']
                    self.y = diccionario['y']
                    self.mostrar(True)
                    break

            for diccionario in self.lista_carreteras:
                if i+1 <len(lista):
                    if lista[i] == diccionario['inicio'] and lista[i+1] == diccionario['final'] :
                        color = (255, 0, 0)
                        width = 9
                        pygame.draw.line(self.fondo, color, diccionario['arranque'], diccionario['termino'], width)
                        pygame.display.flip()
                        clock = pygame.time.Clock()
                        clock.tick(1)
                        break


    def mostrar(self, bandera):
        self.pantalla.blit(self.fondo, (0, 0))
        self.pantalla.blit(self.empresa, (30, 165))
        self.menu(self.seleccion)


        self.lista_cuevas = self.cuevas(self.grafo.getListaVertices(), 300, 100, 1, 0, self.lista_cuevas)
        self.lista_carreteras=self.carreteras(self.lista_cuevas, self.grafo.getListaAristas(), 0,self.lista_carreteras)
        self.clock.tick(1)

        if bandera == False:
            self.x = 210
            self.y = 225
            self.pantalla.blit(self.camion, (self.x, self.y))
        else:
            self.pantalla.blit(self.camion, (self.x, self.y))

        self.grafo.dibujarTabla(self.weight, self.height, self.pantalla)


        pygame.display.flip()

    def menu(self,seleccion):
        s = pygame.Surface((270, 340))  # the size of your rect
        s.set_alpha(128)  # alpha level
        s.fill((255, 255, 255))  # this fills the entire surface
        self.pantalla.blit(s, (16, 310))  # (0,0) are the top-left coordinates
        texto="PROFUNDIDAD"
        s = pygame.Surface((150, 25))  # the size of your rect
        s.set_alpha(192)  # alpha level
        s.fill((155, 155, 155))  # this fills the entire surface
        self.pantalla.blit(s, (20, 315))  # (0,0) are the top-left coordinates
        self.pantalla.blit(self.fuente.render(texto, True, (0, 0, 0)), (20, 320))
        self.pantalla.blit(self.fuente.render(self.texto, True, (0, 0, 0)), (200, 320))


    def cuevas(self,vertices,x,y,contador,posicion,lista_cuevas):

        if posicion < len(vertices):
            if contador < 3:
                self.pantalla.blit(self.fuente.render(vertices[posicion].getDato(), True,(255, 255, 255)), (x+60, y-30))
                self.pantalla.blit(self.vertice, (x, y))
                lista_cuevas.append({'Nombre' : vertices[posicion].getDato(), 'x' : x, 'y' : y } )
                return self.cuevas(vertices,x,y+130,contador+1,posicion+1,lista_cuevas)
            else:
                y=100
                return self.cuevas(vertices,x+270,y,contador-contador,posicion,lista_cuevas)
        else:
            return lista_cuevas

    def carreteras(self,lista_cuevas,aristas,posicion,lista_carreteras):
        if posicion < len(aristas):
            posicion_inicial = None
            posicion_final = None
            inicio=None
            final=None
            for diccionario in lista_cuevas:
                if diccionario['Nombre'] == aristas[posicion].getOrigen():
                    posicion_inicial = (diccionario['x']+45, diccionario['y']+10)
                    inicio=diccionario['Nombre']
                if diccionario['Nombre'] == aristas[posicion].getDestino():
                    posicion_final = (diccionario['x']+45, diccionario['y']+10)
                    final = diccionario['Nombre']
                color = (155, 155, 155)
                width = 9
                if posicion_inicial and posicion_final!= None:
                    pygame.draw.line(self.fondo, color, posicion_inicial, posicion_final, width)
                    lista_carreteras.append({'inicio': inicio,'final': final,'arranque': posicion_inicial,'termino': posicion_final})
                    return self.carreteras(lista_cuevas,aristas,posicion+1,lista_carreteras)
        else:
            return lista_carreteras

    def agregar_cueva(self,x,y,dato,grafo):
        self.pantalla.blit(self.fuente.render(dato, True, (255, 255, 255)), (x + 75, y - 53))
        self.pantalla.blit(self.vertice, (x, y))
        grafo.agregar_vertice(dato)


    def salir(self):
        pygame.quit()

    def ejecutar(self):


        clock = pg.time.Clock()
        input_box1 = InputBox(50, 345, 32, 32)
        input_boxes = [input_box1]
        done = False
        if self.iniciar() == False:
            self.corriendo = False

        # 1. profundidad
        valores = input_box1.getValor()

        if valores:
            if valores[0] == 1 and len(valores) == 2:
                self.profundidad(valores[1])
                a = []
                input_box1.setValor(a)



        while (self.corriendo):
            for event in pygame.event.get():
                self.evento(event)
                for box in input_boxes:
                    box.handle_event(event)
            for box in input_boxes:
                box.update()
            for box in input_boxes:
                box.draw(self.pantalla)

            # 1. profundidad
            valores = input_box1.getValor()
            print(valores)
            if len(valores) == 2:

                if valores[0] == '1':
                    self.profundidad(valores[1])
                    a = []
                    input_box1.setValor(a)
                if valores[0] == '2':
                    # Amplitud
                    a = []
                    input_box1.setValor(a)

            pygame.display.flip()
            clock.tick(20)
            self.on_loop()
            self.cursor.update()
            self.mostrar(False)



        self.salir()

