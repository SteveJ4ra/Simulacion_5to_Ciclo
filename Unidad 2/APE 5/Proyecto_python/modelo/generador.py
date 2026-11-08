"""Generador congruencial lineal: X0 es la semilla; la salida empieza en X1."""
A, C, M = 1664525, 1013904223, 2**32
MAX_CANTIDAD = 1_000_000


class GeneradorLCG:
    def __init__(self, semilla):
        if type(semilla) is not int or not 0 <= semilla < M:
            raise ValueError(f"La semilla debe ser un entero entre 0 y {M-1}.")
        self.estado = semilla

    def siguiente(self):
        self.estado = (A * self.estado + C) % M
        return self.estado

    def generar(self, cantidad):
        if type(cantidad) is not int or not 1 <= cantidad <= MAX_CANTIDAD:
            raise ValueError(f"La cantidad debe estar entre 1 y {MAX_CANTIDAD}.")
        return [self.siguiente() for _ in range(cantidad)]
