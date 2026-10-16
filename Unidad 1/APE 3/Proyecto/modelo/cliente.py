class Cliente:
    def __init__(self, numero, llegada):
        self.numero = numero
        self.llegada = llegada
        self.inicio_servicio = None
        self.salida = None

    def tiempo_espera(self):
        return self.inicio_servicio - self.llegada

    def tiempo_en_sistema(self):
        return self.salida - self.llegada
