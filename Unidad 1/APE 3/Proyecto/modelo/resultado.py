class Resultado:
    def __init__(self, escenario):
        self.escenario = escenario
        self.teoricas = None
        self.simuladas = None
        self.clientes = []
        self.estados = []
        self.fotos = []
        self.mensaje = ""

    def fue_simulado(self):
        return self.simuladas is not None
