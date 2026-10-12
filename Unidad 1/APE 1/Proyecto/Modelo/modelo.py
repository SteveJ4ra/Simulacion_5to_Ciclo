from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class ModeloLluvia:
    peso_humedad: float = 0.5
    peso_nubosidad: float = 0.3
    peso_temperatura: float = 0.2

    def __post_init__(self) -> None:
        pesos = np.array(
            [self.peso_humedad, self.peso_nubosidad, self.peso_temperatura],
            dtype=float,
        )
        if not np.isfinite(pesos).all() or (pesos < 0).any():
            raise ValueError("Los pesos deben ser finitos y no negativos.")
        if not np.isclose(pesos.sum(), 1.0, rtol=0, atol=1e-12):
            raise ValueError("Los pesos deben sumar 1.")

    def evaluar(self, datos: pd.DataFrame) -> pd.DataFrame:
        columnas = ["Humedad", "Nubosidad", "Temperatura"]
        if not {"Hora", *columnas}.issubset(datos.columns):
            raise ValueError("Faltan columnas en las mediciones.")
        if datos.empty:
            raise ValueError("Se necesita al menos una medición.")

        valores = datos[columnas].to_numpy(dtype=float)
        if not np.isfinite(valores).all():
            raise ValueError("Las mediciones deben ser números finitos.")
        if ((valores[:, :2] < 0) | (valores[:, :2] > 100)).any():
            raise ValueError("La humedad y la nubosidad deben estar entre 0 y 100.")

        resultado = datos.copy()
        resultado[columnas] = valores
        resultado["H"] = valores[:, 0] / 100
        resultado["N"] = valores[:, 1] / 100
        # Entre los valores de la tabla se interpola; fuera se usan sus límites.
        resultado["Tf"] = np.interp(
            valores[:, 2],
            np.arange(10, 29, 2),
            np.linspace(1.0, 0.1, 10),
        )
        resultado["Índice"] = (
            self.peso_humedad * resultado["H"]
            + self.peso_nubosidad * resultado["N"]
            + self.peso_temperatura * resultado["Tf"]
        ).clip(0, 1)
        indice = resultado["Índice"].to_numpy()
        resultado["Estado"] = np.select(
            [indice < 0.40, indice < 0.60, indice < 0.75],
            ["Sin lluvia", "Baja posibilidad", "Lluvia probable"],
            default="Lluvia",
        )
        return resultado
