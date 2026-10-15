import argparse
from pathlib import Path
import sys

import matplotlib.pyplot as plt

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from Controlador.controlador import ControladorSimulacion
from Modelo.calibracion import DATOS_INICIALES
from Vista.graficas import crear_graficas


def main() -> None:
    parser = argparse.ArgumentParser(description="Comparación de modelos de crecimiento poblacional del APE 2.")
    parser.add_argument("--datos", nargs="+", type=float, default=list(DATOS_INICIALES), help="Observaciones en intervalos de una unidad de tiempo.")
    parser.add_argument("--r", type=float, default=None, help="Tasa de crecimiento; por defecto se estima de los datos.")
    parser.add_argument("--sigma", type=float, default=None, help="Desviación estándar del ruido; por defecto se estima de los residuos.")
    parser.add_argument("--dt", type=float, default=0.1, help="Paso de Euler (por defecto: 0.1).")
    parser.add_argument("--semilla", type=int, default=42, help="Semilla del generador aleatorio.")
    parser.add_argument("--repeticiones", type=int, default=300, help="Número de repeticiones del modelo estocástico.")
    parser.add_argument("--sin-ventana", action="store_true", help="Guardar las gráficas sin abrir ventanas.")
    parser.add_argument("--salida", type=Path, default=Path(__file__).resolve().parents[1] / "resultados", help="Carpeta de resultados.")
    argumentos = parser.parse_args()
    if argumentos.sin_ventana:
        plt.switch_backend("Agg")
    try:
        controlador = ControladorSimulacion(
            argumentos.datos, argumentos.dt, argumentos.semilla,
            argumentos.r, argumentos.sigma, argumentos.repeticiones,
        )
        resultado = controlador.ejecutar()
    except ValueError as error:
        parser.error(str(error))

    p = resultado.parametros
    print(f"P0 = {p.poblacion_inicial:g}; r = {p.tasa:.8f}; sigma = {p.sigma:.6f}")
    print(f"Tiempo = {p.periodos}; dt = {p.paso:g}; semilla = {p.semilla}")
    print("\nComparación en los tiempos observados")
    print(resultado.comparacion.to_string(index=False, float_format=lambda valor: f"{valor:.4f}"))
    print("\nComparación con los datos de entrada")
    print(resultado.metricas.to_string(index=False, float_format=lambda valor: f"{valor:.4f}"))
    print("\nInfluencia del paso de Euler")
    print(resultado.pasos.to_string(index=False, float_format=lambda valor: f"{valor:.6f}"))

    controlador.guardar(resultado, argumentos.salida)
    figuras = crear_graficas(resultado)
    for nombre, figura in figuras.items():
        figura.savefig(argumentos.salida / f"{nombre}.png", dpi=160)
    print(f"\nResultados guardados en: {argumentos.salida.resolve()}")
    if not argumentos.sin_ventana:
        plt.show()
    for figura in figuras.values():
        plt.close(figura)


if __name__ == "__main__":
    main()
