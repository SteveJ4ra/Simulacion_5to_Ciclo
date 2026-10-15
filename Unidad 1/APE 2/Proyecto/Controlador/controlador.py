from dataclasses import asdict, dataclass, replace
import json
from pathlib import Path

import numpy as np
import pandas as pd

from Modelo.calibracion import calibrar
from Modelo.modelos import Parametros, deterministico, discreto, estocastico, euler


@dataclass
class ResultadoSimulacion:
    parametros: Parametros
    comparacion: pd.DataFrame
    continuo: pd.DataFrame
    metricas: pd.DataFrame
    resumen_estocastico: pd.DataFrame
    trayectorias: np.ndarray
    tasas: pd.DataFrame
    pasos: pd.DataFrame
    ruido: dict[float, np.ndarray]


class ControladorSimulacion:
    def __init__(
        self,
        datos: list[float],
        paso: float = 0.1,
        semilla: int = 42,
        tasa: float | None = None,
        sigma: float | None = None,
        repeticiones: int = 300,
    ) -> None:
        if not 2 <= repeticiones <= 10_000:
            raise ValueError("Utiliza entre 2 y 10 000 repeticiones.")
        self.parametros = calibrar(datos, paso, semilla, tasa, sigma)
        self.observaciones = np.asarray(datos, dtype=float)
        self.repeticiones = repeticiones

    def ejecutar(self) -> ResultadoSimulacion:
        p = self.parametros
        tiempos = np.arange(p.periodos + 1)
        tiempo_euler, poblacion_euler = euler(p)
        trayectorias = estocastico(p, self.repeticiones)
        comparacion = pd.DataFrame({
            "Tiempo": tiempos,
            "Observado": self.observaciones,
            "Determinístico": deterministico(p, tiempos),
            "Discreto": discreto(p),
            "Estocástico": trayectorias[0],
            "Euler": np.interp(tiempos, tiempo_euler, poblacion_euler),
        })
        continuo = pd.DataFrame({
            "Tiempo": tiempo_euler,
            "Exacto": deterministico(p, tiempo_euler),
            "Euler": poblacion_euler,
        })
        metricas = pd.DataFrame([
            {
                "Modelo": nombre,
                "Población final": comparacion[nombre].iloc[-1],
                "RMSE frente a datos": np.sqrt(np.mean((comparacion[nombre] - self.observaciones) ** 2)),
            }
            for nombre in ("Determinístico", "Discreto", "Estocástico", "Euler")
        ])
        resumen = pd.DataFrame({
            "Tiempo": tiempos,
            "Media": trayectorias.mean(axis=0),
            "Desviación estándar": trayectorias.std(axis=0, ddof=1),
            "Percentil 5": np.quantile(trayectorias, 0.05, axis=0),
            "Percentil 95": np.quantile(trayectorias, 0.95, axis=0),
        })
        magnitud = max(abs(p.tasa), 0.1)
        tasas = pd.DataFrame({"Tiempo": continuo["Tiempo"]})
        for tasa in (-magnitud, 0.0, magnitud):
            tasas[f"r = {tasa:.5f}"] = deterministico(replace(p, tasa=tasa), tiempo_euler)
        pasos = []
        exacto_final = float(deterministico(p, np.array([p.periodos]))[0])
        for paso in (1.0, 0.5, 0.25, 0.1, 0.05):
            _, valores = euler(replace(p, paso=paso))
            pasos.append({
                "dt": paso,
                "Población final": valores[-1],
                "Error absoluto final": abs(valores[-1] - exacto_final),
            })
        escala = p.sigma if p.sigma > 0 else 1.0
        ruido = {
            sigma: estocastico(replace(p, sigma=sigma), self.repeticiones)
            for sigma in (0.0, escala, 2 * escala)
        }
        return ResultadoSimulacion(
            p, comparacion, continuo, metricas, resumen, trayectorias,
            tasas, pd.DataFrame(pasos), ruido,
        )

    @staticmethod
    def guardar(resultado: ResultadoSimulacion, salida: Path) -> None:
        salida.mkdir(parents=True, exist_ok=True)
        tablas = {
            "comparacion": resultado.comparacion,
            "continuo": resultado.continuo,
            "metricas": resultado.metricas,
            "resumen_estocastico": resultado.resumen_estocastico,
            "influencia_r": resultado.tasas,
            "influencia_dt": resultado.pasos,
        }
        for nombre, tabla in tablas.items():
            tabla.to_csv(salida / f"{nombre}.csv", index=False, encoding="utf-8-sig")
        parametros = asdict(resultado.parametros)
        parametros["repeticiones"] = resultado.trayectorias.shape[0]
        (salida / "parametros.json").write_text(
            json.dumps(parametros, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
