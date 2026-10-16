# Simulación de una cola M/M/1

Proyecto del APE 3 de Simulación. Representa las llegadas de clientes, su espera en una cola FIFO y la atención mediante un único servidor. Compara tres escenarios con sus valores teóricos y muestra una animación en consola.

## Tecnologías utilizadas

Se ejecutó con Python 3.13.14 y estas bibliotecas:

| Biblioteca | Versión utilizada | Uso |
| --- | --- | --- |
| SimPy | 4.1.2 | Procesos de llegada y atención del servidor |
| NumPy | 2.5.4 | Generación de tiempos exponenciales |
| Matplotlib | 3.11.2 | Gráficas de cada escenario y comparación |

`threading`, `queue`, `time` y `os` pertenecen a la biblioteca estándar de Python.

## Instalación

El código está en `Unidad 1/APE 3/Proyecto`. Abre una terminal en la carpeta general `APE 3` para instalar las dependencias.

### Windows (PowerShell)

```powershell
cd "$env:USERPROFILE\Desktop\Simulación\Unidad 1\APE 3"
py -3.13 -m venv Proyecto\.venv
.\Proyecto\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### Linux y macOS (Bash o Zsh)

Cambia `/ruta/Simulación` por la ubicación del repositorio. Con Python 3.13 instalado:

```bash
cd "/ruta/Simulación/Unidad 1/APE 3"
python3.13 -m venv Proyecto/.venv
Proyecto/.venv/bin/python -m pip install -r requirements.txt
```

Las dependencias tienen versiones exactas en `requirements.txt`. El entorno se crea en `Proyecto/.venv` y queda excluido por `.gitignore`. Los comandos utilizan directamente su intérprete; no hace falta activarlo. La animación necesita una terminal con soporte para colores ANSI, como la terminal integrada de VS Code o Windows Terminal.

## Configuración

Los parámetros se encuentran en `main.py`:

| Parámetro | Valor | Descripción |
| --- | ---: | --- |
| `TIEMPO_SIMULACION` | 20 000 | Minutos simulados por escenario |
| `TIEMPO_CALENTAMIENTO` | 500 | Período inicial excluido de las métricas |
| `SEMILLA` | 2026 | Semilla del generador aleatorio |
| `MINUTOS_ANIMADOS` | 120 | Primeros minutos reproducidos en consola |
| `MINUTOS_POR_PASO` | 1 | Avance entre fotografías de la cola |
| `SEGUNDOS_POR_PASO` | 0.15 | Pausa real entre fotogramas |
| `SEGUNDOS_ENTRE_ESCENARIOS` | 2 | Pausa entre escenarios |
| `VENTANA_GRAFICA_COLA` | 200 | Minutos mostrados después del calentamiento |

`ALTO_GRAFICA` controla las filas de las barras de consola y `CLIENTES_VISIBLES`, la cantidad de clientes dibujados. `CARPETA_GRAFICAS` indica dónde se guardan las imágenes; por defecto es `graficas`.

Se utilizan los siguientes escenarios, con tasas en clientes por minuto:

| Escenario | Llegada λ | Servicio μ | Utilización teórica ρ |
| --- | ---: | ---: | ---: |
| 1: sistema estable | 2.0 | 3.0 | 0.6667 |
| 2: mayor utilización | 2.5 | 3.0 | 0.8333 |
| 3: cerca de saturación | 2.9 | 3.0 | 0.9667 |

Puedes modificar `ESCENARIOS` y los parámetros en `main.py`. Para las fórmulas de equilibrio deben cumplirse tasas positivas y λ < μ. El calentamiento debe ser menor que la duración total.

## Uso

Desde la carpeta general `APE 3`, entra en `Proyecto` y ejecuta el programa.

Windows:

```powershell
cd Proyecto
.\.venv\Scripts\python.exe main.py
```

Linux y macOS:

```bash
cd Proyecto
.venv/bin/python main.py
```

El programa recorre los tres escenarios automáticamente. Muestra la cola FIFO, el servidor y las barras de espera en consola; después imprime la tabla teórica y simulada y guarda las gráficas. Para detenerlo, utiliza `Ctrl + C`.

La animación reproduce los primeros 120 minutos, mientras que las métricas finales se calculan entre los minutos 500 y 20 000. El promedio mostrado durante la animación corresponde a esa etapa inicial y puede diferir del resultado final.

En `Proyecto/graficas/` se generan las siguientes imágenes; esta carpeta queda excluida de Git:

- `escenario_1.png`, `escenario_2.png` y `escenario_3.png`: evolución de la cola entre los minutos 500 y 700, histograma de esperas y promedio acumulado de Wq.
- `comparacion.png`: comparación teórica y simulada de Wq y Lq para los tres casos.

## Estructura del proyecto

```text
APE 3/
├── Proyecto/
│   ├── main.py
│   ├── modelo/
│   │   ├── escenario.py
│   │   ├── cliente.py
│   │   ├── estado.py
│   │   ├── foto.py
│   │   ├── metricas.py
│   │   └── resultado.py
│   ├── controlador/
│   │   ├── controlador.py
│   │   ├── simulador.py
│   │   ├── estadisticas.py
│   │   └── teoria.py
│   ├── vista/
│   │   ├── consola.py
│   │   └── graficas.py
│   ├── .venv/       (local)
│   └── graficas/    (generada al ejecutar)
├── README.md
├── requirements.txt
├── referencias.bib
└── .gitignore
```

El proyecto utiliza MVC. Modelo contiene las clases de datos; Controlador administra la simulación y los cálculos; Vista presenta las tablas, la animación y las imágenes. `main.py` configura e inicia la ejecución.

Un hilo calcula los escenarios y entrega los resultados mediante `queue.Queue`. El hilo principal reproduce las fotografías y presenta las salidas.

## Información adicional

Con la semilla 2026 se obtuvieron estos resultados:

| Escenario | Wq teórico (min) | Wq simulado (min) | Lq teórico | Lq simulado |
| --- | ---: | ---: | ---: | ---: |
| 1 | 0.6667 | 0.6582 | 1.3333 | 1.3193 |
| 2 | 1.6667 | 1.5192 | 4.1667 | 3.7968 |
| 3 | 9.6667 | 11.9953 | 28.0333 | 35.1865 |

L y Lq se calculan con promedios ponderados por tiempo. Wq utiliza clientes que llegaron desde el minuto 500 e iniciaron servicio; W utiliza quienes también registraron su salida.

El programa se detiene al minuto 20 000. Quienes siguen esperando no aportan una espera completa a Wq y quienes aún no han salido no aportan su permanencia a W. La ejecución utiliza una corrida por escenario, sin intervalos de confianza. En el tercero, el error relativo de Wq fue del 24.09 %; el promedio acumulado todavía presenta variaciones.

Para reproducir los valores se deben conservar la semilla, los parámetros y las versiones utilizadas. La semilla permite repetir la secuencia; no elimina la variabilidad del modelo.
