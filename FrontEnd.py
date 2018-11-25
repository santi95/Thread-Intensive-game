import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QProgressBar
from PyQt5.QtGui import QIcon, QPixmap, QTransform
from PyQt5.Qt import QTimer, QTest, QFrame, QDrag, QApplication, QLabel
from PyQt5.QtCore import Qt, QMimeData
from BackEnd import Dino, Extras
from random import randint
from Funciones_Utiles import prox_apar, distancia, prox_extra
import constantes
from time import sleep
from BackendTienda import Funcionalidad_Tienda

main = uic.loadUiType('Main.ui')
store = uic.loadUiType('Tienda.ui')
game = uic.loadUiType('Game.ui')


class MainWindows(main[0], main[1]):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.push_button0.clicked.connect(self.juego)
        self.setObjectName('main')
        self.setStyleSheet(
            "#main {background-image: url(Assets/Main.png); background-attachment: fixed;}    ")
        puntajes = []
        try:
            with open('Highscores.txt', 'r') as file:
                for line in file:
                    puntajes.append(float(line.strip()))
            puntajes.sort(reverse=True)
        except:
            with open('Highscores.txt', 'w') as file:
                for line in file:
                    puntajes.append(float(line.strip()))
            puntajes.sort(reverse=True)
        try:
            self.high1.setText(str(round(puntajes[0])))
        except:
            self.high1.setText('El primero de 1 sigue siendo el ganador')
        try:
            self.high2.setText(str(round(puntajes[1])))
        except:
            self.high2.setText('El segundo de 2 sigue siendo segundo')
        try:
            self.high3.setText(str(round(puntajes[2])))
        except:
            self.high3.setText(
                'El tercero de tres sigue siendo tercero, no último')

    def juego(self):
        self.hide()
        self.cambio = Game()
        self.cambio.show()


''' Las clases que intenté usar para el draggable que no pude alfinal :(
class DropBox(QFrame):
    def __init__(self, parent):
        super().__init__()
        self.acceptDrops()
        self.setAcceptDrops(True)
        self.setStyleSheet('background-color : black; color: white')

    def dragEnterEvent(self, event):
        event.acceptProposedAction()
        print(2, 'aprete un click')
        print(event)

    def dropEvent(self, event):
        print('me está intentando shegar algo')
        pos = event.pos()
        self.label = event.source()
        self.label.setParent(self)
        self.label.show()
        event.acceptProposedAction()
        print(3)

class DraggableLabel(QLabel):
    def __init__(self, parent):
        super().__init__()
        self.setStyleSheet('background-color: black; color: white')


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()
        print(4, 'real aprete un click')
        print(event)

    def mouseMoveEvent(self, event):
        if not (event.buttons() and Qt.LeftButton):
            return

        if ((event.pos() - self.drag_start_position).manhattanLength() <
                QApplication.startDragDistance()):
            return

        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setText(self.text())
        drag.setMimeData(mime_data)
        self.drop_action = drag.exec(Qt.CopyAction | Qt.MoveAction)
'''


class Store(store[0], store[1]):
    def __init__(self, puntos, main, bonus):
        super().__init__()
        self.mainwindow = main
        self.setupUi(self)
        self.score = str(puntos)
        self.puntos.setText(self.score)
        self.back_but.clicked.connect(self.back)
        self.sub_correr.clicked.connect(self.sub_correr1)
        self.dis_correr.clicked.connect(self.dis_correr1)
        self.sub_vida.clicked.connect(self.sub_vida1)
        self.dis_vida.clicked.connect(self.dis_vida1)
        self.sub_atacar.clicked.connect(self.sub_atacar1)
        self.dis_atacar.clicked.connect(self.dis_atacar1)
        self.bonus = bonus
        self.cant_correr.setText(str(bonus[0]))
        self.cant_vida.setText(str(bonus[1]))
        self.cant_atacar.setText(str(bonus[2]))
        self.setObjectName('fondo')
        self.setStyleSheet(
            "#fondo {background-image: url(Assets/Tienda.jpg);"
            " background-attachment: fixed;}")

    def sub_correr1(self):
        datos = Funcionalidad_Tienda(self.score, 'correr',
                                     int(self.cant_correr.text()),
                                     int(self.cant_vida.text()),
                                     int(self.cant_atacar.text()), self.bonus)
        nivel = self.cant_correr.text()
        if datos.check_condiciones() == True:
            self.cant_correr.setText(str(int(nivel) + 1))
            self.mainwindow.mover.velocidad /= 1.1
            self.mainwindow.mover.bonus_correr += 1
            self.mainwindow.puntaje -= 250
            self.score = str(round(float(self.score)) - 250)
            self.puntos.setText(self.score)

    def sub_atacar1(self):
        datos = Funcionalidad_Tienda(self.score, 'atacar',
                                     int(self.cant_correr.text()),
                                     int(self.cant_vida.text()),
                                     int(self.cant_atacar.text()), self.bonus)
        nivel = self.cant_atacar.text()
        if datos.check_condiciones() == True:
            self.cant_atacar.setText(str(int(nivel) + 1))
            self.mainwindow.mover.vel_ataque /= 1.15
            self.mainwindow.mover.bonus_atacar += 1
            self.mainwindow.puntaje -= 500
            self.score = str(round(float(self.score)) - 500)
            self.puntos.setText(self.score)

    def sub_vida1(self):
        datos = Funcionalidad_Tienda(self.score, 'vida',
                                     int(self.cant_correr.text()),
                                     int(self.cant_vida.text()),
                                     int(self.cant_atacar.text()), self.bonus)
        nivel = self.cant_vida.text()
        if datos.check_condiciones() == True:
            self.cant_vida.setText(str(int(nivel) + 1))
            self.mainwindow.mover.vida_max *= 1.2
            self.mainwindow.mover.bonus_vida += 1
            self.mainwindow.puntaje -= 750
            self.score = str(round(float(self.score)) - 750)
            self.puntos.setText(self.score)

    def dis_correr1(self):
        nivel = self.cant_correr.text()
        if nivel != '0':
            self.cant_correr.setText(str(int(nivel) - 1))
            self.mainwindow.mover.velocidad *= 1.1
            self.mainwindow.mover.bonus_correr -= 1

    def dis_atacar1(self):
        nivel = self.cant_atacar.text()
        if nivel != '0':
            self.cant_atacar.setText(str(int(nivel) - 1))
            self.mainwindow.mover.vel_ataque *= 1.15
            self.mainwindow.mover.bonus_atacar -= 1

    def dis_vida1(self):
        nivel = self.cant_vida.text()
        if nivel != '0':
            self.cant_vida.setText(str(int(nivel) - 1))
            self.mainwindow.mover.vida_max /= 1.1
            self.mainwindow.mover.bonus_vida -= 1

        '''Intento de hacerlo draggable, pero no me salió nuncaaaa :((((
            Por lo tanto lo haré con botones, no quiero dejarlo no funcional
        # self.drag1 = DraggableLabel(self)
        # self.drag2 = DraggableLabel(self)
        # self.drag3 = DraggableLabel(self)
        # self.inv1 = DropBox(self)
        # self.inv2 = DropBox(self)
        # self.inv3 = DropBox(self)
        # self.inv4 = DropBox(self)
        # self.inv5 = DropBox(self)
        # self.inv1.setGeometry(self.box1.geometry())
        # self.inv2.setGeometry(self.box2.geometry())
        # self.inv3.setGeometry(self.box3.geometry())
        # self.inv4.setGeometry(self.box4.geometry())
        # self.inv5.setGeometry(self.box5.geometry())
        # self.box1.lower()
        # self.box2.lower()
        # self.box3.lower()
        # self.box4.lower()
        # self.box5.lower()
'''

    def back(self, MainWindow):
        self.mainwindow.pausa_total()
        '''Hacer todo lo que tiene que ver con agregar la velocidad + vida al mono'''
        self.hide()


class Game(game[0], game[1]):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.centralwidget.setStyleSheet(
            "background-image: url(Assets/Tienda.jpg); background-attachment: scroll; ")

        self._puntaje = constantes.PUNTAJE_INICIO
        self.puntaje_tiempo = constantes.PUNTAJE_TIEMPO
        self.puntaje_enemigo = constantes.PUNTAJE_ENEMIGO
        self.puntaje_nivel = constantes.PUNTAJE_NIVEL

        self.score.setText(str(self.puntaje))
        self.score.setStyleSheet('color : white')

        self.pausa.clicked.connect(self.pausa_total)
        self.tienda.clicked.connect(self.abrir_tienda_temporal)
        self.salir.clicked.connect(self.game_over)

        self.label_pausa.hide()
        self.label_game_over.hide()

        self.setGeometry(500, 50, 600, 600)
        self.setWindowTitle('Mejor que LOL')
        # self.setAutoFillBackground(True)

        self._avance_barra_nivel = 0
        self.nivel = 1
        self.label_2.setText(str(self.nivel))
        self.label_2.setStyleSheet("color: rgb(255, 255, 255)")
        self.pro_bar.setValue(self.avance_barra_nivel)
        self.show()

        alto = self.centralwidget.size().height()
        ancho = self.centralwidget.size().width()

        # Tiempo para la próxima aparición
        self.prox_apari = 0
        self.prox_extra = (0, '')
        # para que parta en la mitad de la ventana sin contar la barra de nivel superior
        self.mover = Dino(self, alto / 2, ancho / 2,
                          'user')  # AQUí está la creación de DINO
        Dino.lista_threads_activos.append(self.mover)
        self.mover.start()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.time)
        self.timer.start()
        self.tiempo = 0

        self.seguir = True
        self.keylist = []

    # Se encarga de ir creando los monstruos
    def time(self):
        '''Self.seguir genera la pausa'''
        if self.seguir:
            self.tiempo += 1
            QTest.qWait(1000)
            self.puntaje += self.puntaje_tiempo
            ancho = self.centralwidget.size().width() - 50
            largo = self.centralwidget.size().height() - 29
            pro_bar = self.pro_bar.size().height() + 10
            if round(self.tiempo) > round(
                    self.prox_apari) and self.prox_apari != 0:
                # Es mas 60 ya que la posición de estos elementos es el centro de la imagen
                enemigo = Dino(self, randint(0, ancho) + 60,
                               randint(pro_bar, largo) + 60, 'malo')
                enemigo.start()
                Dino.lista_threads_activos.append(enemigo)
                prox_apar(self)

            if round(self.tiempo) > round(self.prox_extra[0]):
                if self.prox_extra[0] != 0:
                    elem = self.prox_extra[1]
                    extra = Extras(self, randint(0, ancho),
                                   randint(pro_bar, largo), elem)
                    Dino.lista_threads_activos.append(extra)
                prox_extra(self)

    @property
    def puntaje(self):
        return self._puntaje

    @puntaje.setter
    def puntaje(self, value):
        self.score.setText(str(value))
        self._puntaje = value

    @property
    def avance_barra_nivel(self):
        return self._avance_barra_nivel

    @avance_barra_nivel.setter
    def avance_barra_nivel(self, value):
        # Dino crece cada 50% de la barra de nivel
        if value >= 50 and not self.mover.crecio_este_nivel and value < 100:
            self.mover.crece()
            # El drag crece
            self.mover.crecio_este_nivel = True
            # actualiza el tamaño del prgress bar del avance cada segundo
            self.pro_bar.setValue(value)
            # Actualiza el nivel del juego cada segundo
            # Llama al personaje principal a atacar o ser atacado

        if value >= 100 and self.nivel < 5:
            self._avance_barra_nivel = 0
            self.nivel += 1
            # El dragon cree cuando pasa de nivel
            self.mover.crece()
            self.crecio_este_nivel = False
            self.pro_bar.setValue(0)
            # Actualiza el nivel del juego cada segundo
            self.label_2.setText(str(self.nivel))
            # Llama al personaje principal a atacar o ser atacado
            self.puntaje += 1500 + self.puntaje_nivel * self.nivel

        elif value >= 100 and self.nivel == 5:
            self.game_over()

        else:
            self._avance_barra_nivel = value
            self.pro_bar.setValue(value)

    @staticmethod
    def actualizar_imagen(myImageEvent):
        label = myImageEvent.image
        label.move(myImageEvent.x, myImageEvent.y)

    @staticmethod
    def agrandar_imagen(myImageEvent):
        label = myImageEvent.image
        label.setGeometry(myImageEvent.x,
                          myImageEvent.y,
                          myImageEvent.sizex,
                          myImageEvent.sizey)

    @staticmethod
    def atacar(Atacar):
        # Mono 1 realiza el ataque, mono2 lo recibe
        mono1 = Atacar.obj1
        mono2 = Atacar.obj2
        mono1a = mono1.ataque
        mono2.vida -= mono1a

        if mono1.muerto and mono1.foto == 'user':
            mono1.parent.game_over()
            mono1.pro_bar.setValue(0)
        if mono2.muerto and mono2.foto == 'user':
            mono2.pro_bar.setValue(0)
            mono2.parent.game_over()
        if not mono1.muerto and mono1.atacable:
            mono1.pro_bar.setValue(mono1.vida / mono1.vida_max * 100)
        if not mono2.muerto:
            mono2.pro_bar.setValue((mono2.vida / mono2.vida_max) * 100)
        if mono2.muerto and mono2.foto == 'malo' and mono1.atacable:
            mono1.parent.avance_barra_nivel += (
            1000 / (100 * max([mono2.lvl_size - mono1.lvl_size + 3, 1])))
            mono1.parent.puntaje += 1000 + mono1.parent.puntaje_enemigo * (
            mono2.lvl_size - mono1.lvl_size)
            pos = Dino.lista_threads_activos.index(mono2)
            Dino.lista_threads_activos.pop(pos)
            mono2.pro_bar.setValue(0)

    @staticmethod
    def bonuses(Bonus):
        obj = Bonus.obj
        dino = Bonus.dino
        elem = obj.elem

        if elem == 'bomba' and not obj.apretada:
            obj.apretada = True
            obj.image.setStyleSheet('color: white; font:20pt MS Shell Dlg 2')
            obj.image.setText('3')
            QTest.qWait(1000)
            obj.image.setText('2')
            QTest.qWait(1000)
            obj.image.setText('1')
            QTest.qWait(1000)
            # Aquí hacemos que explote y mate a la gente de alrededor mio :D
            obj_mueren = [(distancia(obj.pos_centro, i.pos_centro), i)
                          for i in Dino.lista_threads_activos
                          if i.muerto == False
                          if i.foto != 'extra']
            for i in obj_mueren:
                # Le puse 20 pq 10 unidades era muy poco
                if i[0] < 10 + i[1].radio:
                    i[1].muerto = True
                    if i[1].muerto and i[1].foto == 'user':
                        i[1].parent.game_over()
            obj.image.hide()
            obj.muerto = True

        if elem == 'puntaje_extra':
            dino.parent.puntaje += 1000
            obj.image.hide()
            pos = Dino.lista_threads_activos.index(obj)
            Dino.lista_threads_activos.pop(pos)
            obj.muerto = True

        if elem == 'vida_extra':
            dino.vida = dino.vida_max
            dino.pro_bar.setValue(100)
            obj.image.hide()
            pos = Dino.lista_threads_activos.index(obj)
            Dino.lista_threads_activos.pop(pos)
            obj.muerto = True

    def keyPressEvent(self, event):
        self.firstrelease = True
        # Para agarrar el multikeys
        astr = event.key()
        self.keylist.append(astr)

    def keyReleaseEvent(self, event):
        if self.firstrelease == True:
            self.processmultikeys(self.keylist)

        self.firstrelease = False
        del self.keylist[-1]

    def processmultikeys(self, keyspressed):
        if ord('W') in keyspressed:
            self.mover.lista_mov.append('up')
        if ord('D') in keyspressed:
            self.mover.lista_mov.append('right')
        if ord('A') in keyspressed:
            self.mover.lista_mov.append('left')
        if ord('S') in keyspressed:
            self.mover.lista_mov.append('down')
        if ord('C') in keyspressed:
            self.mover.crece()
            self.mover.pro_bar.setValue(
                self.mover.vida / self.mover.vida_max * 100)
        if ord('F') in keyspressed:
            # Se va o regresa de FullScreen
            if not self.isFullScreen():
                self.showFullScreen()
            else:
                self.showNormal()

        if 16777249 in keyspressed and ord('S') in keyspressed:
            self.pausa_total()

        if 16777249 in keyspressed and ord('T') in keyspressed:
            self.abrir_tienda_temporal()

    def abrir_tienda_temporal(self):
        self.pausa_total()
        bonus = (self.mover.bonus_correr, self.mover.bonus_vida,
                 self.mover.bonus_atacar)
        self.cambio = Store(puntos=self.puntaje, main=self, bonus=bonus)
        self.cambio.show()

    def pausa_total(self):
        ancho = self.centralwidget.size().width() - 50
        largo = self.centralwidget.size().height() - 29

        if self.seguir:
            self.seguir = False
            self.label_pausa.setGeometry(ancho / 2, largo / 2, 200, 200)
            self.label_pausa.show()
        else:
            self.label_pausa.hide()
            self.seguir = True

    def game_over(self):
        '''Hacer todo lo que se hace cuando se pierde'''
        self.seguir = False
        for i in Dino.lista_threads_activos:
            i.muerto = True
        self.label_game_over.show()
        try:
            with open('Highscores.txt', 'r') as file:
                print(self.puntaje, file=file)
        except:
            with open('Highscores.txt', 'a') as file:
                file.write(str(self.puntaje) + '\n')

        QTest.qWait(4000)
        self.hide()
        self.cambio = MainWindows()
        self.cambio.show()


if __name__ == '__main__':
    app = QApplication([])
    form = MainWindows()
    form.show()
    sys.exit(app.exec_())
