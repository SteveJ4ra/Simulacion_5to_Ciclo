from dataclasses import dataclass


@dataclass(frozen=True)
class Configuracion:
    semilla: int = 12345
    a: int = 1664525
    c: int = 1013904223
    m: int = 2**32
    cantidad: int = 10000

    def validar(self):
        for nombre in ("semilla", "a", "c", "m", "cantidad"):
            if type(getattr(self, nombre)) is not int:
                raise ValueError(f"{nombre} debe ser un entero.")
        if not 2 <= self.m <= 2**32:
            raise ValueError("El módulo debe estar entre 2 y 2^32.")
        for nombre in ("semilla", "a", "c"):
            valor = getattr(self, nombre)
            if valor < 0 or valor >= self.m:
                raise ValueError(f"{nombre} debe estar entre 0 y m - 1.")
        if not 50 <= self.cantidad <= 1_000_000:
            raise ValueError("La cantidad debe estar entre 50 y 1 000 000 (frecuencia esperada mínima: 5).")


def generar(config):
    config.validar()
    estado = config.semilla
    valores = []
    for _ in range(config.cantidad):
        estado = (config.a * estado + config.c) % config.m
        valores.append(estado)
    return valores
