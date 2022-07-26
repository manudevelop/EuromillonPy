from datetime import datetime

class Sorteo:
    id = 0
    numero1 = 0
    numero2 = 0
    numero3 = 0
    numero4 = 0
    numero5 = 0
    estrella1 = 0
    estrella2 = 0
    fecha = datetime.now()
    premio = 0
    bote = 0
    recaudacion = 0
    premios = 0
    escrutinio = []

    def numeros(self):
        return [self.numero1,self.numero2,self.numero3,self.numero4,self.numero5]
    def estrellas(self):
        return [self.estrella1,self.estrella2]   

