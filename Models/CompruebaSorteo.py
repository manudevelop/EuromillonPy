class CompruebaSorteo:
    Numeros = []
    Estrellas = []
    Sorteo = None
    Escrutinio = None
    Categoria = 0

    def __init__(self, sorteo = None):
        self.Numeros = []
        self.Estrellas = []
        self.Escrutinio = None
        self.Sorteo = sorteo