# APE 5 · Python

Implementación del generador congruencial lineal (LCG) con Python 3.10 o posterior. Usa la biblioteca estándar de Python.

## Instalación y ejecución

Desde la carpeta `APE 5`, ejecuta los comandos de tu sistema.

**Windows (PowerShell)**

```powershell
cd Proyecto_python
python -m venv .venv
.\.venv\Scripts\python.exe main.py --exportar ../resultados/python
```

**Linux y macOS**

```bash
cd Proyecto_python
python3 -m venv .venv
./.venv/bin/python main.py --exportar ../resultados/python
```

Por defecto, el programa genera 10 000 valores para cada semilla (`12345` y `54321`). Puedes cambiar estos valores con `--semilla`, `--comparar-semilla` y `--cantidad`. Ejecuta `main.py --help` con el mismo intérprete para ver las opciones.

Si omites `--exportar`, los resultados se muestran en la consola. Si ya hay una exportación con los mismos nombres, elige otra carpeta de salida. Las gráficas SVG se abren en el navegador.

## Estructura

- `main.py` recibe las opciones de consola.
- `modelo/` genera y guarda la secuencia.
- `controlador/` calcula las estadísticas y coordina la ejecución.
- `vista/` muestra y exporta los resultados.

[Bibliografía](../referencias.bib)
