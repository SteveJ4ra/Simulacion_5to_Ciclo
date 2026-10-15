import numpy as np

from Modelo.modelos import Parametros


DATOS_INICIALES = (1000, 1100, 1250, 1400, 1600, 1850, 2100)


def calibrar(
    datos: list[float],
    paso: float = 0.1,
    semilla: int = 42,
    tasa: float | None = None,
    sigma: float | None = None,
) -> Parametros:
    valores = np.asarray(datos, dtype=float)
    if valores.ndim != 1 or len(valores) < 3:
        raise ValueError("Ingresa al menos tres observaciones de población.")
    if not np.isfinite(valores).all() or (valores <= 0).any():
        raise ValueError("Las observaciones deben ser finitas y mayores que cero.")

    # Se supone una unidad de tiempo entre observaciones consecutivas.
    tasa_estimada = float(np.mean(np.diff(np.log(valores))))
    tasa_modelo = tasa_estimada if tasa is None else tasa
    residuos = valores[1:] - valores[:-1] * (1 + tasa_modelo)
    sigma_estimada = float(np.std(residuos, ddof=1))
    return Parametros(
        poblacion_inicial=float(valores[0]),
        tasa=tasa_modelo,
        sigma=sigma_estimada if sigma is None else sigma,
        periodos=len(valores) - 1,
        paso=paso,
        semilla=semilla,
    )
