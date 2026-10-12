import argparse
from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from Controlador.controlador import ControladorSimulacion


def mostrar_tablas(resultados: dict[str, pd.DataFrame], comparacion: pd.DataFrame) -> None:
    formulas = {
        "Original": "I = 0.50H + 0.30N + 0.20Tf",
        "Ajustado": "I = 0.45H + 0.40N + 0.15Tf",
    }
    for nombre, tabla in resultados.items():
        print(f"\nModelo {nombre.lower()}: {formulas[nombre]}")
        print(tabla.to_string(index=False, float_format=lambda valor: f"{valor:.4f}"))
        horas = tabla.loc[tabla["Estado"] == "Lluvia", "Hora"]
        print("Horas clasificadas como lluvia:", ", ".join(horas) or "Ninguna")
    print("\nComparación de modelos")
    print(comparacion.to_string(index=False, float_format=lambda valor: f"{valor:.4f}"))


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


def main() -> None:
    parser = argparse.ArgumentParser(description="Simulación del índice de lluvia del APE 1.")
    parser.add_argument("--sin-ventana", action="store_true", help="Guardar la gráfica sin abrir una ventana.")
    parser.add_argument(
        "--salida", type=Path, default=Path(__file__).resolve().parents[1] / "resultados",
        help="Carpeta para las tablas CSV y la gráfica.",
    )
    argumentos = parser.parse_args()
    if argumentos.sin_ventana:
        plt.switch_backend("Agg")

    controlador = ControladorSimulacion()
    resultados = controlador.simular()
    comparacion = controlador.comparar(resultados)
    mostrar_tablas(resultados, comparacion)

    argumentos.salida.mkdir(parents=True, exist_ok=True)
    for nombre, tabla in resultados.items():
        tabla.to_csv(argumentos.salida / f"modelo_{nombre.lower()}.csv", index=False, encoding="utf-8-sig")
    comparacion.to_csv(argumentos.salida / "comparacion.csv", index=False, encoding="utf-8-sig")
    figura = crear_grafica(resultados)
    figura.savefig(argumentos.salida / "simulacion.png", dpi=160)
    print(f"\nResultados guardados en: {argumentos.salida.resolve()}")
    if not argumentos.sin_ventana:
        plt.show()
    plt.close(figura)


if __name__ == "__main__":
    main()
