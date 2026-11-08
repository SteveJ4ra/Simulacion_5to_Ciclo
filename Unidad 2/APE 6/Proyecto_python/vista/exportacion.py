import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from modelo.pruebas import decidir


def exportar(config, valores, resultado, salida):
    carpeta = Path(salida)
    carpeta.mkdir(parents=True, exist_ok=True)
    with (carpeta / "secuencia_python.csv").open("w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["n", "X", "U"])
        for posicion, valor in enumerate(valores, 1):
            escritor.writerow([posicion, valor, format(valor / config.m, ".17g")])
    with (carpeta / "frecuencias_python.csv").open("w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["desde", "hasta_excluido", "observada", "esperada"])
        for indice, frecuencia in enumerate(resultado["frecuencias"]):
            escritor.writerow([indice / 10, (indice + 1) / 10, frecuencia, resultado["esperada"]])
    with (carpeta / "pruebas_python.csv").open("w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["prueba", "estadistico", "valor_p", "alfa", "decision"])
        escritor.writerow(["Chi-cuadrado", resultado["chi"], resultado["p_chi"], 0.05, decidir(resultado["p_chi"])])
        escritor.writerow(["KS asintotico", resultado["d"], resultado["p_ks"], 0.05, decidir(resultado["p_ks"])])
    guardar_grafica(config, valores, resultado, carpeta)
    print(f"Resultados guardados en: {carpeta.resolve()}")


def guardar_grafica(config, valores, resultado, carpeta):
    uniformes = sorted(valor / config.m for valor in valores)
    # Incluimos los extremos y cada salto de la distribución empírica.
    tiempos = [0.0]
    acumuladas = [0.0]
    cantidad = len(uniformes)
    for posicion, uniforme in enumerate(uniformes, 1):
        tiempos.append(uniforme)
        acumuladas.append(posicion / cantidad)
    tiempos.append(1.0)
    acumuladas.append(1.0)
    figura, (frecuencias, distribucion) = plt.subplots(1, 2, figsize=(12, 5), layout="constrained")
    try:
        frecuencias.bar(range(10), resultado["frecuencias"], label="Observada")
        frecuencias.axhline(resultado["esperada"], color="red", linestyle="--", label="Esperada")
        frecuencias.set(title="Chi-cuadrado: frecuencias", xlabel="Intervalo (0 a 9)", ylabel="Frecuencia")
        frecuencias.legend()
        distribucion.step(tiempos, acumuladas, where="post", label="Empírica")
        distribucion.plot([0, 1], [0, 1], "--", label="Uniforme teórica")
        distribucion.set(title="KS: distribución acumulada", xlabel="U", ylabel="F(U)", xlim=(0, 1), ylim=(0, 1))
        distribucion.legend()
        figura.savefig(carpeta / "pruebas_python.png", dpi=150)
    finally:
        plt.close(figura)
