class Funcionalidad_Tienda:
    def __init__(self, puntaje, comprar, correr, vida, atacar, bonus):
        self.puntaje = round(float(puntaje))
        self.comprar = comprar
        self.correr = int(correr)
        self.vida = int(vida)
        self.atacar = int(atacar)
        self.precio_correr = 250
        self.precio_vida = 750
        self.precio_atacar = 500
        self.init_correr = int(bonus[0])
        self.init_vida = int(bonus[1])
        self.init_atacar = int(bonus[2])


    def check_condiciones(self):
        suma = self.correr + self.vida + self.atacar
        if suma > 4:
            return False
        elif self.comprar == 'correr':
            if self.puntaje >= self.precio_correr:
                return True
        elif self.comprar == 'vida':
            if self.puntaje >= self.precio_vida:
                return True
        elif self.comprar == 'atacar':
            if self.puntaje >= self.precio_atacar:
                return True



