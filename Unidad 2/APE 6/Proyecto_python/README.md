# APE 6 · Python

Genera una secuencia pseudoaleatoria con el método congruencial lineal (LCG) y evalúa su ajuste a la distribución uniforme con Chi-cuadrado y Kolmogorov-Smirnov (KS).

## Tecnologías

Python 3.13, NumPy, SciPy y Matplotlib. Las versiones de las dependencias están en [requirements.txt](../requirements.txt).

## Instalación y uso

Ejecuta estos comandos desde la carpeta `APE 6`.

**Windows (PowerShell)**

```powershell
cd Proyecto_python
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r ..\requirements.txt
.\.venv\Scripts\python.exe main.py
```

**Linux y macOS**

```bash
cd Proyecto_python
python3 -m venv .venv
./.venv/bin/python -m pip install -r ../requirements.txt
./.venv/bin/python main.py
```

La ejecución usa la semilla `12345` y genera `10000` valores. Añade `--semilla 42 --cantidad 5000` al comando de ejecución para probar otra muestra. Con `--help` puedes ver todas las opciones.

En `resultados_python/` se guardan tres CSV con la secuencia, las frecuencias y los resultados de las pruebas. Abre `pruebas_python.png` para ver las frecuencias por intervalo y la comparación de las distribuciones acumuladas.

## Estructura

- `main.py`: recibe las opciones de la consola.
- `modelo/`: genera la secuencia y aplica las pruebas.
- `controlador/`: coordina la ejecución.
- `vista/`: muestra los resultados y exporta los archivos.

Las fuentes de la práctica están en [referencias.bib](../referencias.bib).
