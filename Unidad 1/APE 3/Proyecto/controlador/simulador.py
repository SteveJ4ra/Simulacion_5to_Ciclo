import numpy as np
import simpy

from modelo.cliente import Cliente
from modelo.estado import Estado
from modelo.foto import Foto


class SimuladorMM1:
    def __init__(self, escenario, semilla):
        self.lam = escenario.lam
        self.mu = escenario.mu
        self.tiempo_simulacion = escenario.tiempo
        self.aleatorio = np.random.default_rng(semilla)

        self.entorno = simpy.Environment()

        self.servidor = simpy.Resource(self.entorno, capacity=1)

        self.clientes = []

        self.estados = [Estado(0, 0, 0)]

        self.cola = []
        self.en_servicio = None
        self.en_sistema = 0

        self.fotos = []
        self.suma_esperas = 0
        self.atendidos = 0

    def registrar_estado(self):
        estado = Estado(self.entorno.now, len(self.cola), self.en_sistema)
        self.estados.append(estado)

    def generar_clientes(self):
        numero = 0
        while True:
            tiempo_entre_llegadas = self.aleatorio.exponential(1 / self.lam)

            yield self.entorno.timeout(tiempo_entre_llegadas)

            numero = numero + 1
            cliente = Cliente(numero, self.entorno.now)
            self.clientes.append(cliente)

            self.entorno.process(self.atender_cliente(cliente))

    def atender_cliente(self, cliente):
        self.cola.append(cliente)
        self.en_sistema = self.en_sistema + 1

        turno = self.servidor.request()
        self.registrar_estado()

        yield turno

        self.cola.remove(cliente)
        self.en_servicio = cliente

        cliente.inicio_servicio = self.entorno.now
        self.suma_esperas = self.suma_esperas + cliente.tiempo_espera()
        self.atendidos = self.atendidos + 1
        self.registrar_estado()

        tiempo_servicio = self.aleatorio.exponential(1 / self.mu)

        yield self.entorno.timeout(tiempo_servicio)

        self.servidor.release(turno)
        self.en_servicio = None
        cliente.salida = self.entorno.now
        self.en_sistema = self.en_sistema - 1
        self.registrar_estado()

    def tomar_fotos(self, duracion, paso):
        while self.entorno.now <= duracion:
            numeros_en_cola = []
            for cliente in self.cola:
                numeros_en_cola.append(cliente.numero)

            en_servicio = 0
            if self.en_servicio is not None:
                en_servicio = self.en_servicio.numero

            espera_promedio = 0
            if self.atendidos > 0:
                espera_promedio = self.suma_esperas / self.atendidos

            self.fotos.append(Foto(self.entorno.now, en_servicio, numeros_en_cola, espera_promedio))
            yield self.entorno.timeout(paso)

    def ejecutar(self, duracion_fotos, paso_fotos):
        self.entorno.process(self.generar_clientes())
        self.entorno.process(self.tomar_fotos(duracion_fotos, paso_fotos))
        self.entorno.run(until=self.tiempo_simulacion)
