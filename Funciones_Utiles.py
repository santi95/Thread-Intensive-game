from random import expovariate, randint, choice
import numpy

def distancia(pos1, pos2):
    x = pos1[0]
    y = pos1[1]
    z = pos2[0]
    k = pos2[1]
    distancia = (((z-x)**2 + (k-y)**2 ) **(1/2))

    return distancia

def prox_apar(parent):
    if parent.nivel == 1:
        prox_apari = expovariate(1/10)
    elif parent.nivel == 2:
        prox_apari = expovariate(1/8)
    elif parent.nivel == 3:
        prox_apari = expovariate(1/6)
    elif parent.nivel == 4:
        prox_apari = expovariate(1/4)
    elif parent.nivel == 5:
        prox_apari = expovariate(1/2)

    parent.prox_apari += prox_apari

def prox_extra(parent):

    tiempo = randint(1,30)  #En realidad es cada 30
    parent.prox_extra = (parent.prox_extra[0] + tiempo, choice(['bomba', 'puntaje_extra', 'vida_extra']))
    print(parent.prox_extra)
    #Falta agregarle el safezone a la lista

def retornar_tamano(parent):
    if parent.nivel == 1: tamano = numpy.random.triangular(1, 1, 5)     #1,1,5
    if parent.nivel == 2: tamano = numpy.random.triangular(1, 3, 6)
    if parent.nivel == 3: tamano = numpy.random.triangular(3, 5, 7)
    if parent.nivel == 4: tamano = numpy.random.triangular(5, 7, 9)
    if parent.nivel == 5: tamano = numpy.random.triangular(7, 9, 10)

    return round(tamano)


