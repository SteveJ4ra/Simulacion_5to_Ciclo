"""Python 3.10+, sin dependencias externas. Ejecutar: python main.py

Opciones: --semilla 12345 --comparar-semilla 54321 --cantidad 10000
--exportar CARPETA guarda CSV y gráficas SVG solo cuando se solicita.
"""
import argparse
from controlador.controlador import ejecutar


def iniciar():
    parser = argparse.ArgumentParser(description="Práctica 05: generador congruencial lineal.")
    parser.add_argument('--semilla', type=int, default=12345)
    parser.add_argument('--comparar-semilla', type=int, default=54321)
    parser.add_argument('--cantidad', type=int, default=10_000)
    parser.add_argument('--exportar', metavar='CARPETA')
    args = parser.parse_args()
    try:
        ejecutar(args.semilla, args.comparar_semilla, args.cantidad, args.exportar)
    except (ValueError, OSError) as error:
        parser.exit(1, f'Error: {error}\n')


if __name__ == '__main__':
    iniciar()
