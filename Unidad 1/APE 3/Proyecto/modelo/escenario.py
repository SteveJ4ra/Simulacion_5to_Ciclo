class Escenario:
    def __init__(self, numero, lam, mu, tiempo, condicion):
        self.numero = numero
        self.lam = lam
        self.mu = mu
        self.tiempo = tiempo
        self.condicion = condicion

    def utilizacion(self):
        return self.lam / self.mu

    def es_estable(self):
        if self.lam > 0 and self.lam < self.mu:
            return True
        return False
