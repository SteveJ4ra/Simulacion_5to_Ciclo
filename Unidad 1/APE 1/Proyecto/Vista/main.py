import argparse
from pathlib import Path
import sys

import matplotlib.pyplot as plt
import pandas as pd

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from Controlador.controlador import ControladorSimulacion
from Vista.graficas import crear_grafica, crear_grafica_modelo


def mostrar_tablas(
    resultados: dict[str, pd.DataFrame],
    comparacion: pd.DataFrame,
    formulas: dict[str, str],
) -> None:
    for nombre, tabla in resultados.items():
        print(f"\nModelo {nombre.lower()}: {formulas[nombre]}")
        print(tabla.to_string(index=False, float_format=lambda valor: f"{valor:.4f}"))
        horas = tabla.loc[tabla["Estado"] == "Lluvia", "Hora"]
        print("Horas clasificadas como lluvia:", ", ".join(horas) or "Ninguna")
    print("\nComparación de modelos")
    print(comparacion.to_string(index=False, float_format=lambda valor: f"{valor:.4f}"))


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
    mostrar_tablas(
        resultados, comparacion,
        {"Original": controlador.original.ecuacion, "Ajustado": controlador.ajustado.ecuacion},
    )

    argumentos.salida.mkdir(parents=True, exist_ok=True)
    for nombre, tabla in resultados.items():
        tabla.to_csv(argumentos.salida / f"modelo_{nombre.lower()}.csv", index=False, encoding="utf-8-sig")
    comparacion.to_csv(argumentos.salida / "comparacion.csv", index=False, encoding="utf-8-sig")
    figuras = {"simulacion": crear_grafica(resultados)}
    for nombre, tabla in resultados.items():
        figuras[f"grafica_{nombre.lower()}"] = crear_grafica_modelo(nombre, tabla)
    for nombre, figura in figuras.items():
        figura.savefig(argumentos.salida / f"{nombre}.png", dpi=160)
    print(f"\nResultados guardados en: {argumentos.salida.resolve()}")
    if not argumentos.sin_ventana:
        plt.show()
    for figura in figuras.values():
        plt.close(figura)


if __name__ == "__main__":
    main()
