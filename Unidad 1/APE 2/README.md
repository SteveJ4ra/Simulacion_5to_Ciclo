# APE 2 - Comparación de modelos de crecimiento poblacional

## Descripción del proyecto

Compara cuatro formulaciones del crecimiento poblacional: solución exponencial determinística, recurrencia discreta, recurrencia estocástica con ruido normal aditivo y aproximación de la ecuación continua mediante Euler. El arreglo de entrada es `[1000, 1100, 1250, 1400, 1600, 1850, 2100]`.

Se supone una unidad de tiempo entre observaciones: siete valores representan seis intervalos. El programa calcula los parámetros, compara los resultados con los datos y genera escenarios para observar el efecto de `r`, `sigma` y `dt`.

## Tecnologías utilizadas

- Python 3.13.
- NumPy 2.5.4 para los cálculos y el generador aleatorio.
- pandas 2.3.3 para las tablas y los archivos CSV.
- Matplotlib 3.11.2 para las gráficas.

La estructura utiliza Modelo Vista Controlador (MVC), con el ejecutable en `Proyecto/Vista/main.py`.

## Instalación

Se necesita Python 3.13 y Git. Si ya tienes el repositorio, abre una consola en `Unidad 1/APE 2` y continúa con la creación del entorno.

### Windows (PowerShell)

```powershell
git clone https://github.com/SteveJ4ra/Simulacion_5to_Ciclo.git
cd "Simulacion_5to_Ciclo\Unidad 1\APE 2"
python -m venv Proyecto\.venv
.\Proyecto\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### Linux y macOS (Bash o Zsh)

Comprueba que `python3 --version` corresponde a Python 3.13. Si tienes varias versiones, utiliza `python3.13` para crear el entorno.

```bash
git clone https://github.com/SteveJ4ra/Simulacion_5to_Ciclo.git
cd "Simulacion_5to_Ciclo/Unidad 1/APE 2"
python3 -m venv Proyecto/.venv
./Proyecto/.venv/bin/python -m pip install -r requirements.txt
```

En Linux, Python debe incluir el soporte de `venv` de la versión utilizada. Si falta ese componente, instálalo con el gestor de paquetes de tu distribución.

## Configuración

Los datos predeterminados están en `Proyecto/Modelo/calibracion.py`. También puedes enviar un arreglo distinto mediante `--datos`.

| Parámetro | Obtención o valor predeterminado |
| --- | --- |
| `P0` | Primer valor del arreglo. |
| Tiempo total | Cantidad de observaciones menos uno. |
| `r` | Media de los incrementos logarítmicos: `ln(Pfinal/P0) / tiempo`. |
| `sigma` | Desviación estándar muestral de los residuos `P[t+1] - (1+r)P[t]`. |
| `dt` | `0.1`, paso de Euler. |
| Semilla | `42`, para repetir las mismas realizaciones aleatorias. |
| Repeticiones | `300`, para comparar la dispersión del modelo estocástico. |

`r` se expresa por unidad de tiempo; `sigma`, en unidades de población. La tasa estimada depende de los extremos del arreglo y de su duración. Los valores intermedios intervienen en la estimación de `sigma` y la comparación con los datos.

Si se indican `--r` o `--sigma`, se utilizan esos valores. Si solo se cambia `--r`, `sigma` se estima con los residuos de esa tasa. Los datos deben contener al menos tres valores finitos y positivos.

## Uso

Todos los comandos se ejecutan desde la carpeta general del APE y utilizan directamente el Python del entorno virtual.

### Windows (PowerShell)

Ejecutar los datos de la guía:

```powershell
.\Proyecto\.venv\Scripts\python.exe .\Proyecto\Vista\main.py
```

Generar archivos sin abrir ventanas:

```powershell
.\Proyecto\.venv\Scripts\python.exe .\Proyecto\Vista\main.py --sin-ventana
```

Cambiar los datos y el paso:

```powershell
.\Proyecto\.venv\Scripts\python.exe .\Proyecto\Vista\main.py --datos 500 530 580 640 720 --dt 0.05 --sin-ventana
```

Cambiar la tasa, el ruido, la semilla y la carpeta de salida:

```powershell
.\Proyecto\.venv\Scripts\python.exe .\Proyecto\Vista\main.py --r -0.1 --sigma 20 --semilla 7 --repeticiones 500 --sin-ventana --salida ".\Proyecto\resultados\decrecimiento"
```

Consultar las opciones:

```powershell
.\Proyecto\.venv\Scripts\python.exe .\Proyecto\Vista\main.py --help
```

### Linux y macOS (Bash o Zsh)

Ejecutar los datos de la guía:

```bash
./Proyecto/.venv/bin/python ./Proyecto/Vista/main.py
```

Generar archivos sin abrir ventanas:

```bash
./Proyecto/.venv/bin/python ./Proyecto/Vista/main.py --sin-ventana
```

Cambiar los datos y el paso:

```bash
./Proyecto/.venv/bin/python ./Proyecto/Vista/main.py --datos 500 530 580 640 720 --dt 0.05 --sin-ventana
```

Cambiar la tasa, el ruido, la semilla y la carpeta de salida:

```bash
./Proyecto/.venv/bin/python ./Proyecto/Vista/main.py --r -0.1 --sigma 20 --semilla 7 --repeticiones 500 --sin-ventana --salida "./Proyecto/resultados/decrecimiento"
```

Consultar las opciones:

```bash
./Proyecto/.venv/bin/python ./Proyecto/Vista/main.py --help
```

## Estructura del proyecto

```text
APE 2/
├── Proyecto/
│   ├── Modelo/
│   │   ├── modelos.py
│   │   └── calibracion.py
│   ├── Controlador/
│   │   └── controlador.py
│   ├── Vista/
│   │   ├── main.py
│   │   └── graficas.py
│   ├── .venv/             # Entorno local, excluido de Git
│   └── resultados/        # Se genera al ejecutar el programa
├── JumboSteven_APE_2_U1.pdf
├── referencias.bib
├── requirements.txt
└── README.md
```

- `modelos.py`: parámetros y ecuaciones de los cuatro modelos.
- `calibracion.py`: validación de las observaciones y estimación de parámetros.
- `controlador.py`: ejecución de los escenarios, comparación y exportación de las tablas.
- `main.py`: opciones de consola y presentación de los resultados.
- `graficas.py`: representación de los modelos y las sensibilidades.

## Información adicional

Se generan seis tablas CSV (`comparacion`, `continuo`, `metricas`, `resumen_estocastico`, `influencia_r` e `influencia_dt`), un archivo `parametros.json` y cuatro gráficas PNG (`comparacion`, `influencia_r`, `influencia_sigma` e `influencia_dt`).

El modelo determinístico exacto y Euler describen la misma ecuación continua; Euler la aproxima con pasos finitos. La recurrencia discreta coincide con Euler cuando `dt = 1`. El modelo estocástico también evoluciona en tiempo discreto: incorpora ruido normal independiente en cada paso y limita la población a cero cuando un incremento la volvería negativa.

La banda entre los percentiles 5 y 95 resume las simulaciones con parámetros fijos. No es un intervalo de confianza de los parámetros. El RMSE se calcula sobre los mismos datos usados para estimar los parámetros y no equivale a una validación predictiva.

El desarrollo de la práctica está en [JumboSteven_APE_2_U1.pdf](JumboSteven_APE_2_U1.pdf) y sus fuentes en [referencias.bib](referencias.bib).

Para comparar el ruido se usa sigma igual a cero, el valor configurado y su doble. Si el valor configurado es cero, los escenarios ilustrativos utilizan 0, 1 y 2 unidades de población. Al comparar distintas intensidades se conserva la misma semilla.

Si un tiempo observado queda entre dos pasos de Euler, la tabla de consola y el CSV usan interpolación lineal de la aproximación. El último paso se ajusta para terminar exactamente en el tiempo total.

El entorno virtual y los archivos de `resultados/` están excluidos por el `.gitignore` del repositorio.

## Declaración de uso de IA

Para la presente actividad se ha usado el modelo de inteligencia artificial, GPT 6.1 Sol (Open AI), para acelerar el proceso de investigación de fuentes de calidad para responder las preguntas de control, en conjunto con NotebookLM (Google).

A su vez, se ha utilizado GPT, para entender la sintaxis aplicada en python, para aplicar el patrón arquitectónico "Modelo Vista Controlador (MVC)".

### Prompts utilizado

1. Investiga fuentes de investigación científica que contengan información clave para responder las siguientes preguntas de control presentadas en el documento "ape_guia simulacion semana 2-firmado-signed.pdf". Estas fuentes solo pueden ser de base científica, como papers, revistas, conferencias, congresos, libros, etc.
2. Muestrame un ejemplo básico de como se aplica el patrón Modelo Vista Controlador (MVC).
