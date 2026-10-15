from dataclasses import replace

import matplotlib.pyplot as plt
import numpy as np

from Controlador.controlador import ResultadoSimulacion
from Modelo.modelos import euler


def crear_graficas(resultado: ResultadoSimulacion) -> dict[str, plt.Figure]:
    figuras = {}
    tabla = resultado.comparacion
    continuo = resultado.continuo
    figura, eje = plt.subplots(figsize=(10, 6), layout="constrained")
    eje.plot(continuo["Tiempo"], continuo["Exacto"], label="Determinístico exacto", linewidth=2)
    eje.step(tabla["Tiempo"], tabla["Discreto"], where="post", label="Discreto", linestyle="--")
    eje.plot(tabla["Tiempo"], tabla["Estocástico"], "o-", label="Estocástico (una realización)")
    eje.plot(continuo["Tiempo"], continuo["Euler"], label=f"Euler, dt={resultado.parametros.paso:g}", linestyle=":", linewidth=2)
    eje.scatter(tabla["Tiempo"], tabla["Observado"], color="black", marker="x", label="Datos de entrada", zorder=5)
    eje.set(title="Comparación de los cuatro modelos", xlabel="Tiempo (unidades)", ylabel="Población")
    eje.legend()
    eje.grid(alpha=0.25)
    figuras["comparacion"] = figura

    figura, eje = plt.subplots(figsize=(10, 5), layout="constrained")
    for nombre in resultado.tasas.columns[1:]:
        eje.plot(resultado.tasas["Tiempo"], resultado.tasas[nombre], label=nombre)
    eje.set(title="Influencia de la tasa de crecimiento", xlabel="Tiempo (unidades)", ylabel="Población")
    eje.legend()
    eje.grid(alpha=0.25)
    figuras["influencia_r"] = figura

    figura, ejes = plt.subplots(1, 3, figsize=(13, 4.8), sharex=True, sharey=True, layout="constrained")
    for eje, (sigma, trayectorias) in zip(ejes, resultado.ruido.items()):
        for valores in trayectorias[:20]:
            eje.plot(tabla["Tiempo"], valores, color="#2878b5", alpha=0.18, linewidth=0.8)
        inferior, superior = np.quantile(trayectorias, [0.05, 0.95], axis=0)
        eje.fill_between(tabla["Tiempo"], inferior, superior, alpha=0.2, label="Percentiles 5-95")
        eje.plot(tabla["Tiempo"], trayectorias.mean(axis=0), color="#b34a28", linewidth=2, label="Media")
        eje.set(title=f"sigma = {sigma:.3f}", xlabel="Tiempo (unidades)")
        eje.grid(alpha=0.25)
    ejes[0].set_ylabel("Población")
    ejes[-1].legend(fontsize=8)
    figura.suptitle(f"Efecto del ruido: {resultado.trayectorias.shape[0]} repeticiones por escenario")
    figuras["influencia_sigma"] = figura

    figura, (eje, eje_error) = plt.subplots(1, 2, figsize=(12, 5), layout="constrained")
    eje.plot(continuo["Tiempo"], continuo["Exacto"], color="black", linewidth=2, label="Exacto")
    for paso in resultado.pasos["dt"]:
        tiempos, poblacion = euler(replace(resultado.parametros, paso=float(paso)))
        eje.plot(tiempos, poblacion, label=f"dt = {paso:g}", alpha=0.8)
    eje.set(title="Aproximación de Euler", xlabel="Tiempo (unidades)", ylabel="Población")
    eje.legend(fontsize=8)
    eje.grid(alpha=0.25)
    pasos = resultado.pasos.sort_values("dt")
    eje_error.plot(pasos["dt"], pasos["Error absoluto final"], "o-")
    eje_error.set(title="Error respecto a la solución exacta", xlabel="dt", ylabel="Error absoluto al final")
    eje_error.grid(alpha=0.25)
    figuras["influencia_dt"] = figura
    return figuras
