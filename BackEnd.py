from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QProgressBar, QVBoxLayout
from PyQt5.QtGui import QPixmap, QKeyEvent, QTransform
from PyQt5.Qt import QTest, QTimer, QThread, pyqtSignal
from time import time, sleep
from random import randint, random
import math
import numpy
import sys
from Funciones_Utiles import prox_apar, distancia, retornar_tamano

class MoveMyImageEvent:
    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y

class ChangeSizeImageEvent:
    def __init__(self, image, x, y, sizex, sizey):
        self.x = x
        self.y = y
        self.image = image
        self.sizex = sizex
        self.sizey = sizey


class Atacar:
    def __init__(self, obj1, obj2):
        self.obj1 = obj1
        self.obj2 = obj2

class Bonus:
    def __init__(self, dino, obj):
        self.dino = dino
        self.obj = obj


class Dino(QThread):
    trigger = pyqtSignal(MoveMyImageEvent)
    sizetrigger = pyqtSignal(ChangeSizeImageEvent)
    atacktrigger = pyqtSignal(Atacar)
    bonustrigger = pyqtSignal(Bonus)

    lista_threads_activos = []
    id = 0

    def __init__(self, parent, x, y, foto):
        super().__init__()
        self.parent = parent
        self.foto = foto
        #Crea el atributo dentro de la otra ventana
        self.image = QLabel(parent)
        self.pro_bar = QProgressBar(parent)
        self.pro_bar.setTextVisible(False)
        self.crecio_este_nivel = False
        self.id = Dino.id
        Dino.id += 1
        self.rango_vision = 0
        self.rango_escape = 0
        if foto == 'malo':
            #Nos dá el tamaño del monstruo dependiendo de la distribución y del nivel del juego
            tamano = retornar_tamano(self.parent) * 30
            self._size = (tamano, tamano)
            self.image.setGeometry(x, y, tamano, tamano)
            self.pro_bar.setGeometry(x, y - 20, tamano, 10)
            self.lvl_size = tamano / 30
        else:
            tamano = 60
            #Tamaño en la interfaz
            self._size = (tamano, tamano)
            self.image.setGeometry(x, y, tamano, tamano)
            self.pro_bar.setGeometry(x, y - 20, tamano, 10)
            #Nivel de tamaño
            self.lvl_size = 2
        #Lo que le pasamos a la tienda
        self.bonus_correr = 0
        self.bonus_vida = 0
        self.bonus_atacar = 0
        #Inconsistencia en el enunciado, luego desde la tienda lo multiuplico por 1.1
        self.vida_max = (((self.lvl_size ) * 20 ) + 100)
        self._vida = self.vida_max
        self.muerto = False
        #velocidad ataque inicial
        self.ataque = round(self.lvl_size * (1/10) * self.vida_max, 0)
        #velocidad movimiento inicial
        if foto == 'malo':
            self.velocidad = 1
        if foto == 'user':
            self.velocidad = 0.1
        self.vel_ataque = 1
        self.ratio_vel_ataque = self.vel_ataque / self.velocidad
        self.cont = 0
        #Para los safes zones
        self.atacable = True
        #Se crea una lista cada segundo con las distancias de todos los enemigos al personaje principal
        self.distancias = list
        self._nro_foto = ('c', 1)         #C de caminar, tiene 16
        #self.nro_foto = ('a', 1)        #a de atacar, tiene 8
        #self.nro_foto = ('m', 1)        #M de morir 15
        if self.foto == 'user':
            fase = 'Assets/principal/{} ({}).png'.format(str(self.nro_foto[0]), str(self.nro_foto[1]))
        else:
            fase = 'Assets/enemigo/{} ({}).png'.format(str(self.nro_foto[0]), str(self.nro_foto[1]))
        print(fase)
        self.pixmap = QPixmap(fase)
        self.image.setPixmap(self.pixmap)
        self.image.setScaledContents(True)
        self.pro_bar.setValue((self.vida / self.vida_max) * 100)
        self.image.show()
        self.pro_bar.show()
        self.image.setVisible(True)
        self.pro_bar.setVisible(True)
        self.trigger.connect(parent.actualizar_imagen)
        self.sizetrigger.connect(parent.agrandar_imagen)
        self.atacktrigger.connect(parent.atacar)
        self.bonustrigger.connect(parent.bonuses)
        self.rotation = 0

        self.__position = (x,y)
        self.position= (x,y)
        self.pos_centro = ""
        self.calcular_zona()

        self.lista_mov = []
        prox_apar(self.parent)

    @property
    def vida(self):
        return self._vida

    @vida.setter
    def vida(self, value):
        if value <= 0:
            self.muerto = True
        else:
            self._vida = value

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, value):
        ancho = int(self.parent.centralwidget.size().width()) - self.size[0]
        alto_barra = int(self.parent.pro_bar.size().height()) + 23 + int(self.parent.score_no.size().height())
        largo = int(self.parent.centralwidget.size().height()) - self.size[0] + 21

        if value[1] > alto_barra:
            if value[0] > 0:
                if value[0] < ancho:
                    if value[1] < largo:
                        self.__position = value
                        self.trigger.emit(MoveMyImageEvent(
                            self.image, self.position[0], self.position[1]))
                        self.trigger.emit(MoveMyImageEvent(
                            self.pro_bar, self.position[0], self.position[1] - 17))
                    else:
                        self.__position = (value[0], largo)
                        self.trigger.emit(MoveMyImageEvent(
                            self.image, self.position[0], self.position[1]))
                        self.trigger.emit(MoveMyImageEvent(
                            self.pro_bar, self.position[0], self.position[1] - 17))
                elif value[0] >= ancho and value[1] <= largo:
                    self.__position = (ancho, value[1])
                    self.trigger.emit(MoveMyImageEvent(
                        self.image, self.position[0], self.position[1]))
                    self.trigger.emit(MoveMyImageEvent(
                        self.pro_bar, self.position[0], self.position[1] - 17))
            elif value[0] <= 0  and value[0] <= ancho and value[1] <= largo:
                self.__position = (0, value[1])
                self.trigger.emit(MoveMyImageEvent(
                    self.image, self.position[0], self.position[1]))
                self.trigger.emit(MoveMyImageEvent(
                    self.pro_bar, self.position[0], self.position[1] - 17))
        elif value[1] <= alto_barra and value[0] >= 0 and value[0] <= ancho:
            self.__position = (value[0], alto_barra)
            self.trigger.emit(MoveMyImageEvent(
                self.image, self.position[0], self.position[1]))
            self.trigger.emit(MoveMyImageEvent(
                self.pro_bar, self.position[0], self.position[1] - 17))
        #Cada vez que se mueve se calcula el centro del circulo nuevamente
        self.calcular_zona()
        # print(self.pos_centro)
        # print(self.position)
        # print(self.size)

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        if value[0] <= 300:
            self._size = value
            self.sizetrigger.emit(ChangeSizeImageEvent(image= self.image,
                                                       x = self.position[0],
                                                       y = self.position[1],
                                                       sizex= self.size[0],
                                                       sizey= self.size[1]))

    @property
    def nro_foto(self):
        return self._nro_foto

    @nro_foto.setter
    def nro_foto(self, value):
        if self.foto == 'user':
            if value[0] == 'c':
                if value[1] == 9:
                    self._nro_foto = ('c', 1)
                else:
                    self._nro_foto = value
            if value[0] == 'a':
                if value[1] == 9:
                    self._nro_foto = ('a', 0)
                else:
                    self._nro_foto = value
        if self.foto == 'malo':
            if value[0] == 'c':
                if value[1] == 9:
                    self._nro_foto = ('c', 1)
                else:
                    self._nro_foto = value

    def crece(self):
        self.size = (self.size[0] + 30, self.size[1] + 30)
        self.lvl_size = self.size[0] / 30
        self.calcular_zona()
        self.vida_max = (((self.lvl_size ) * 20 ) + 100)
        self.ataque = round(self.lvl_size * (1/10) * self.vida_max, 0)
        self.pro_bar.setGeometry(self.position[0], self.position[1] - 20, self.lvl_size * 30, 10)


    def calcular_zona(self):
        """Esta función nos va a entregar el centro de un círculo alrededor del personaje
        que nos va a ayudar a darnos cuenta cuando hay un choque o un acercamiento"""
        sizes = self.image.size()
        alto = sizes.height()
        ancho = sizes.width()
        #coordenadas de la esquina superior derecha
        corx = self.position[0]
        cory = self.position[1]
        #circulo de centro(cirx, ciry)
        cirx = corx + (ancho / 2)
        ciry = cory + (alto / 2)
        self.radio = (((self.size[0]/2)**2 + (self.size[1]/2)**2) **(1/2))
        self.pos_centro = (cirx, ciry)

    def check_dir(self):
        if 'up' in self.lista_mov:
            self.position = (self.position[0] + 10 * math.cos(math.radians(self.rotation)),
                             self.position[1] + 10 * math.sin(math.radians(self.rotation)))
        if 'down' in self.lista_mov:
            self.position = (self.position[0] - 10*math.cos(math.radians(self.rotation)),
                             self.position[1] - 10*math.sin(math.radians(self.rotation)))
        if 'right' in self.lista_mov and self.atacable:
            self.rotation += 5
        if 'left' in self.lista_mov and self.atacable:
            self.rotation -= 5
        if self.atacable:
            transform = QTransform().rotate(self.rotation)

        #Caminar
        self.nro_foto = (self.nro_foto[0], self.nro_foto[1] + 1)
        self.pixmap = QPixmap('Assets/principal/{} ({}).png'.format(str(self.nro_foto[0]), str(self.nro_foto[1])))
        pixmap = self.pixmap.transformed(transform)
        self.image.setPixmap(pixmap)
        self.image.show()


    def check_crash(self):
        elem = ''
        if not self.muerto:
            for i in self.distancias:
                '''self.distancias contiene una lista de tuplas [(distancia, objeto)]'''
                if i[0] < i[1].radio + self.radio and not i[1].muerto:
                    if i[1].foto == 'malo' and self.foto == 'user':
                        print('Choque con el {} número {}'.format(i[1].foto, i[1].id))
                        self.atacktrigger.emit(Atacar(self, i[1]))

                    if self.foto == 'user' and i[1].foto == 'extra':
                        print('Agarramos el elemento {}'.format(i[1].elem))
                        self.bonustrigger.emit(Bonus(self, i[1]))
                        elem = i[1].elem
                        if elem == 'safe_zone':
                            self.atacable = False

                    if self.foto == 'malo' and i[1].foto == 'user':
                        self.atacktrigger.emit(Atacar(self, i[1]))
                        print('ataque de verdad')


                if elem != 'safe_zone':
                    self.atacable = True

    def malo_moverse(self):
        '''Solo para los malos, estos son los movimientos aleatorios + los que persiguen a Dino(El personaje principal)'''
        self.rango_vision = self.lvl_size * 30 + self.radio
        self.rango_escape = self.rango_vision * 1.5 + self.radio

        self.distancias = [(distancia(self.pos_centro, i.pos_centro), i)
                           for i in Dino.lista_threads_activos
                           if i.muerto == False
                           and i.foto == 'user']
        obj_in_rango_vision = [i for i in self.distancias if i[0] < self.rango_vision]
        obj_in_rango_escape = [i for i in self.distancias if i[0] < self.rango_escape]
        obj_in_ataque = [i for i in self.distancias if i[0] < i[1].radio + self.radio]

        if obj_in_rango_vision == []:
            #Aca definimos el movimiento aleatorio
            prob_doblar = random()
            if prob_doblar < 0.25:
                self.rotation += 22.5

            #Caminar sin apuro#Caminar
            transform = QTransform().rotate(self.rotation)
            self.nro_foto = (self.nro_foto[0], self.nro_foto[1] + 1)
            self.pixmap = QPixmap('Assets/enemigo/{} ({}).png'.format(str(self.nro_foto[0]), str(self.nro_foto[1])))
            pixmap = self.pixmap.transformed(transform)
            self.image.setPixmap(pixmap)
            self.image.show()

            self.position = (self.position[0] + 10 * math.cos(math.radians(self.rotation)),
                             self.position[1] + 10 * math.sin(math.radians(self.rotation)))

        #Dentro Rango Vision
        #escapa
        if len(obj_in_rango_vision) >= 1:
            #malo tiene  menor nivel
            if self.lvl_size < obj_in_rango_vision[0][1].lvl_size:
                dino = obj_in_rango_vision[0][1]
                while len(obj_in_rango_escape) > 0 and dino.parent.seguir and not self.muerto:
                    print('Escape_Mode')
                    #Persecución
                    dir_ataque = (math.atan2(dino.position[1] - self.position[1],
                                             dino.position[0] - self.position[0]))
                    self.rotation = dir_ataque
                    transform = QTransform().rotate(math.degrees(self.rotation) + 180)
                    pixmap = self.pixmap.transformed(transform)
                    self.image.setPixmap(pixmap)
                    self.image.show()
                    self.position = (self.position[0] + 10 * math.cos((self.rotation) + math.pi),
                                     self.position[1] + 10 * math.sin((self.rotation)+ math.pi))
                    self.distancias = [(distancia(self.pos_centro, i.pos_centro), i)
                                        for i in Dino.lista_threads_activos
                                        if i.muerto == False
                                        and i.foto == 'user']
                    obj_in_rango_vision = [i for i in self.distancias if i[0] < self.rango_vision]
                    obj_in_rango_escape = [i for i in self.distancias if i[0] < self.rango_escape]
                    obj_in_ataque = [i for i in self.distancias if i[0] < i[1].radio + self.radio]
                    QTest.qWait(1000)
                    self.check_crash()

                    #Caminar
                    self.nro_foto = (self.nro_foto[0], self.nro_foto[1] + 1)
                    self.pixmap = QPixmap('Assets/enemigo/{} ({}).png'.format(str(self.nro_foto[0]), str(self.nro_foto[1])))
                    pixmap = self.pixmap.transformed(transform)
                    self.image.setPixmap(pixmap)
                    self.image.show()

            #malo tiene Mayor nivel
            elif self.lvl_size > obj_in_rango_vision[0][1].lvl_size and not self.muerto:
                dino = obj_in_rango_vision[0][1]
                while len(obj_in_rango_escape) > 0 and dino.parent.seguir:
                    print('persuit mode')
                    #Persecución
                    dir_ataque = (math.atan2(dino.position[1] - self.position[1],
                                             dino.position[0] - self.position[0]))
                    self.rotation = dir_ataque
                    transform = QTransform().rotate(math.degrees(self.rotation))
                    pixmap = self.pixmap.transformed(transform)
                    self.image.setPixmap(pixmap)
                    self.image.show()

                    self.position = (self.position[0] + 10 * math.cos((self.rotation)),
                                    self.position[1] + 10 * math.sin((self.rotation)))
                    QTest.qWait(1000)
                    self.distancias = [(distancia(self.pos_centro, i.pos_centro), i)
                                        for i in Dino.lista_threads_activos
                                        if i.muerto == False
                                        and i.foto == 'user']
                    obj_in_rango_vision = [i for i in self.distancias if i[0] < self.rango_vision]
                    obj_in_rango_escape = [i for i in self.distancias if i[0] < self.rango_escape]
                    obj_in_ataque = [i for i in self.distancias if i[0] < i[1].radio + self.radio]
                    self.check_crash()
                    #Caminar
                    self.nro_foto = (self.nro_foto[0], self.nro_foto[1] + 1)
                    self.pixmap = QPixmap('Assets/enemigo/{} ({}).png'.format(str(self.nro_foto[0]), str(self.nro_foto[1])))
                    pixmap = self.pixmap.transformed(transform)
                    self.image.setPixmap(pixmap)
                    self.image.show()

            #Igual nivel
            elif self.lvl_size == obj_in_rango_vision[0][1].lvl_size and not self.muerto:
                deci = random()
                if deci > 0.5:
                    defensa = 1
                else:
                    defensa = 0
                #Si defensa es 1 defiende
                dino = obj_in_rango_vision[0][1]
                while len(obj_in_rango_escape) > 0 and dino.parent.seguir and not self.muerto:
                    if defensa == 0:
                        print('persuit mode')
                    else:
                        print('run_mode')
                    #Persecución
                    dir_ataque = (math.atan2(dino.position[1] - self.position[1],
                                             dino.position[0] - self.position[0]))
                    self.rotation = dir_ataque
                    transform = QTransform().rotate(math.degrees(self.rotation) + 180 * defensa)
                    pixmap = self.pixmap.transformed(transform)
                    self.image.setPixmap(pixmap)
                    self.image.show()

                    self.position = (self.position[0] + 10 * math.cos((self.rotation) + math.pi * defensa),
                                    self.position[1] + 10 * math.sin((self.rotation) + math.pi * defensa))
                    QTest.qWait(1000)
                    self.distancias = [(distancia(self.pos_centro, i.pos_centro), i)
                                        for i in Dino.lista_threads_activos
                                        if i.muerto == False
                                        and i.foto == 'user']
                    obj_in_rango_vision = [i for i in self.distancias if i[0] < self.rango_vision]
                    obj_in_rango_escape = [i for i in self.distancias if i[0] < self.rango_escape]
                    obj_in_ataque = [i for i in self.distancias if i[0] < i[1].radio + self.radio]
                    self.check_crash()
                    #Caminar
                    self.nro_foto = (self.nro_foto[0], self.nro_foto[1] + 1)
                    self.pixmap = QPixmap('Assets/enemigo/{} ({}).png'.format(str(self.nro_foto[0]), str(self.nro_foto[1])))
                    pixmap = self.pixmap.transformed(transform)
                    self.image.setPixmap(pixmap)
                    self.image.show()


    def run(self):
        while not self.muerto:
            if self.parent.seguir:
                self.cont += 1
                # self.largo_max = self.parent.pro_bar.Length()
                QTest.qWait(self.velocidad * 1000)
                #Calcula las distancias entre todos los centros con respecto al personaje principal
                #Le sumamos 15 para que el choque se vea más real
                if self.foto == 'user':
                    self.distancias = [(distancia(self.pos_centro, i.pos_centro), i)
                                       for i in Dino.lista_threads_activos
                                       if i.muerto == False
                                       and i != self]
                    self.ratio_vel_ataque = self.vel_ataque / self.velocidad
                    if self.cont > self.ratio_vel_ataque:
                        self.cont = 0
                        self.check_crash()
                    if not self.atacable:
                        self.image.hide()
                        #self.pro_bar.hide(), Este esconde también la barra de nivel, pero me gusta mas con
                    if self.atacable:
                        #self.pro_bar.show()
                        transform = QTransform().rotate(self.rotation)
                        pixmap = self.pixmap.transformed(transform)
                        self.image.setPixmap(pixmap)
                        self.image.show()

                    self.check_dir()
                    #Checkea si tiene que girar o moverse
                    #Se resetea la lista de movimientos
                    self.lista_mov = []

                if self.foto == 'malo':
                    self.malo_moverse()

        #Animación de la muerte
        if self.foto == 'user':
            carpeta = 'principal'
        else:
            carpeta = 'enemigo'

        for i in range(15):
            transform = QTransform().rotate(self.rotation)
            self.pixmap = QPixmap('Assets/{}/{} ({}).png'.format(carpeta, str('m'), str(i)))
            pixmap = self.pixmap.transformed(transform)
            self.image.setPixmap(pixmap)
            self.image.show()
            QTest.qWait(100)

        self.image.hide()
        self.pro_bar.hide()

    def __repr__(self):
        return self.foto

class Extras:

    def __init__(self, parent, x, y, elem):
        super().__init__()
        self.position = (x,y)
        self.image = QLabel(parent)
        self.parent = parent
        self.foto = 'extra'
        self.elem = elem
        self.muerto = False
        self.pos_centro = (x + 30, y + 30)
        self.radio = (2*30**2)**(1/2)
        self.pixmap = QPixmap('Assets/final/{}.png'.format(self.elem))
        self.image.setPixmap(self.pixmap)
        self.image.setGeometry(x, y, 60, 60)
        self.image.show()
        self.apretada = False
    #
    # def run(self):
    #     while not self.muerto:
    #         pass
    #
    #     self.image.hide()

    def __repr__(self):
        return self.elem
