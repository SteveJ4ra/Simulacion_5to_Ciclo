import argparse
import sys

from controlador.controlador import ejecutar
from modelo.generador import Configuracion
from vista.consola import mostrar
from vista.exportacion import exportar


def main():
    # Evita errores por símbolos al redirigir la salida en Windows.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Uniformidad de un LCG mediante Chi-cuadrado y KS.")
    parser.add_argument("--semilla", type=int, default=12345, help="Estado inicial X0.")
    parser.add_argument("--a", type=int, default=1664525, help="Multiplicador.")
    parser.add_argument("--c", type=int, default=1013904223, help="Incremento.")
    parser.add_argument("--m", type=int, default=2**32, help="Módulo.")
    parser.add_argument("--cantidad", type=int, default=10000, help="Entre 50 y 1 000 000 datos.")
    parser.add_argument("--salida", default="resultados_python", help="Carpeta de CSV y gráfica; reemplaza archivos del mismo nombre.")
    args = parser.parse_args()
    try:
        config = Configuracion(args.semilla, args.a, args.c, args.m, args.cantidad)
        valores, resultado = ejecutar(config)
        mostrar(config, valores, resultado)
        exportar(config, valores, resultado, args.salida)
    except (ValueError, OSError) as error:
        parser.exit(1, f"Error: {error}\n")
    except KeyboardInterrupt:
        print("\nEjecución cancelada.")


if __name__ == "__main__":
    main()
