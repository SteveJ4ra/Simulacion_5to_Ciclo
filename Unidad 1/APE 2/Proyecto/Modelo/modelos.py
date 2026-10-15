from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Parametros:
    poblacion_inicial: float
    tasa: float
    sigma: float
    periodos: int
    paso: float = 0.1
    semilla: int = 42

    def __post_init__(self) -> None:
        valores = [self.poblacion_inicial, self.tasa, self.sigma, self.paso]
        if not np.isfinite(valores).all():
            raise ValueError("Los parámetros deben ser números finitos.")
        if self.poblacion_inicial <= 0 or self.sigma < 0 or self.paso <= 0:
            raise ValueError("P0 y dt deben ser positivos; sigma no puede ser negativo.")
        if self.periodos < 1 or self.periodos != int(self.periodos):
            raise ValueError("El tiempo total debe ser un número entero positivo.")
        if self.semilla < 0:
            raise ValueError("La semilla no puede ser negativa.")
        if self.periodos / self.paso > 100_000:
            raise ValueError("El paso solicitado produce más de 100 000 intervalos.")


def malla_tiempo(periodos: int, paso: float) -> np.ndarray:
    tiempos = np.arange(0.0, periodos, paso)
    return np.append(tiempos, float(periodos))


def deterministico(parametros: Parametros, tiempos: np.ndarray) -> np.ndarray:
    return parametros.poblacion_inicial * np.exp(parametros.tasa * tiempos)


def discreto(parametros: Parametros) -> np.ndarray:
    if parametros.tasa < -1:
        raise ValueError("El modelo discreto requiere r >= -1 para conservar una población no negativa.")
    poblacion = np.empty(parametros.periodos + 1)
    poblacion[0] = parametros.poblacion_inicial
    for i in range(parametros.periodos):
        poblacion[i + 1] = poblacion[i] * (1 + parametros.tasa)
    return poblacion


def estocastico(parametros: Parametros, repeticiones: int = 1) -> np.ndarray:
    if repeticiones < 1:
        raise ValueError("Se requiere al menos una repetición.")
    generador = np.random.default_rng(parametros.semilla)
    ruido = generador.normal(0, parametros.sigma, (repeticiones, parametros.periodos))
    poblacion = np.empty((repeticiones, parametros.periodos + 1))
    poblacion[:, 0] = parametros.poblacion_inicial
    for i in range(parametros.periodos):
        poblacion[:, i + 1] = np.maximum(
            0, poblacion[:, i] * (1 + parametros.tasa) + ruido[:, i]
        )
    return poblacion


def euler(parametros: Parametros) -> tuple[np.ndarray, np.ndarray]:
    tiempos = malla_tiempo(parametros.periodos, parametros.paso)
    pasos = np.diff(tiempos)
    if (1 + parametros.tasa * pasos < 0).any():
        raise ValueError("El paso de Euler genera poblaciones negativas; utiliza un dt menor.")
    poblacion = np.empty(len(tiempos))
    poblacion[0] = parametros.poblacion_inicial
    for i, paso in enumerate(pasos):
        poblacion[i + 1] = poblacion[i] * (1 + paso * parametros.tasa)
    return tiempos, poblacion
