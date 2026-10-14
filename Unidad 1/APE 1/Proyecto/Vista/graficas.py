import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def crear_grafica(resultados: dict[str, pd.DataFrame]) -> plt.Figure:
    datos = resultados["Original"]
    horas = datos["Hora"].tolist()
    posiciones = np.arange(len(horas))
    figura, (ax_indice, ax_variables) = plt.subplots(
        2, 1, figsize=(11, 8), sharex=True, layout="constrained"
    )
    intervalos = [
        (0.0, 0.40, "#e4f0e2", "Sin lluvia"),
        (0.40, 0.60, "#fff5cf", "Baja posibilidad"),
        (0.60, 0.75, "#ffe1be", "Lluvia probable"),
        (0.75, 1.0, "#d8e8fa", "Lluvia"),
    ]
    for inferior, superior, color, estado in intervalos:
        ax_indice.axhspan(inferior, superior, color=color, alpha=0.7)
        ax_indice.text(
            0.99, (inferior + superior) / 2, estado,
            transform=ax_indice.get_yaxis_transform(), ha="right", fontsize=9,
        )
    for nombre, tabla in resultados.items():
        ax_indice.plot(posiciones, tabla["Índice"], marker="o", label=nombre)
    for limite in (0.40, 0.60, 0.75):
        ax_indice.axhline(limite, color="gray", linestyle="--", linewidth=0.7)
    ax_indice.set(title="Posibilidad de lluvia: modelo original y ajustado", ylabel="Índice I", ylim=(0, 1))
    ax_indice.legend(loc="upper left")

    ax_variables.plot(posiciones, datos["Humedad"], "o-", label="Humedad (%)", color="#2878b5")
    ax_variables.plot(posiciones, datos["Nubosidad"], "s-", label="Nubosidad (%)", color="#6b51a3")
    ax_variables.set(ylabel="Porcentaje", ylim=(0, 100), xlabel="Hora", title="Mediciones atmosféricas")
    ax_temperatura = ax_variables.twinx()
    ax_temperatura.plot(posiciones, datos["Temperatura"], "^-", label="Temperatura (°C)", color="#b84a3c")
    ax_temperatura.set(ylabel="Temperatura (°C)", ylim=(10, 28))
    lineas = ax_variables.get_lines() + ax_temperatura.get_lines()
    ax_variables.legend(lineas, [linea.get_label() for linea in lineas], loc="upper left")
    ax_variables.set_xticks(posiciones, horas)
    ax_indice.grid(axis="x", alpha=0.2)
    ax_variables.grid(alpha=0.2)
    return figura



def crear_grafica_modelo(nombre: str, tabla: pd.DataFrame) -> plt.Figure:
    figura, eje = plt.subplots(figsize=(10, 4.5), layout="constrained")
    for inferior, superior, color in (
        (0, 0.40, "#e4f0e2"),
        (0.40, 0.60, "#fff5cf"),
        (0.60, 0.75, "#ffe1be"),
        (0.75, 1, "#d8e8fa"),
    ):
        eje.axhspan(inferior, superior, color=color, alpha=0.7)
    color = "#2878b5" if nombre == "Original" else "#c46b16"
    eje.plot(tabla["Hora"], tabla["Índice"], "o-", color=color)
    for hora, indice in zip(tabla["Hora"], tabla["Índice"]):
        eje.annotate(f"{indice:.4f}", (hora, indice), xytext=(0, 8),
                     textcoords="offset points", ha="center", fontsize=9)
    for limite in (0.40, 0.60, 0.75):
        eje.axhline(limite, color="gray", linestyle="--", linewidth=0.7)
    eje.set(title=f"Modelo {nombre.lower()}", xlabel="Hora", ylabel="Índice I", ylim=(0, 1))
    eje.grid(axis="x", alpha=0.2)
    return figura
