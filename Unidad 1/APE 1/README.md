# APE 1 - Construcción y simulación computacional de un modelo matemático

## Descripción del proyecto

Simulación de un índice de lluvia a partir de la humedad, la nubosidad y la temperatura. Utiliza las nueve mediciones de la guía, entre las 06:00 y las 22:00, para comparar el modelo original con uno ajustado y observar cómo cambian los resultados.

| Modelo | Ecuación |
| --- | --- |
| Original | `I = 0.50H + 0.30N + 0.20Tf` |
| Ajustado | `I = 0.45H + 0.40N + 0.15Tf` |

`H` y `N` son la humedad y la nubosidad divididas para 100. `Tf` se obtiene de la tabla de temperatura de la práctica; para valores intermedios se aplica interpolación lineal. En ambos modelos los pesos suman 1.

## Tecnologías utilizadas

| Tecnología | Versión | Uso |
| --- | --- | --- |
| Python | 3.13 | Lenguaje de programación. |
| NumPy | 2.5.4 | Cálculos numéricos e interpolación. |
| pandas | 2.3.3 | Tablas de resultados y exportación a CSV. |
| Matplotlib | 3.11.2 | Gráficas de los índices y las mediciones. |

El código utiliza el patrón arquitectónico Modelo Vista Controlador (MVC). El entorno virtual se crea con `venv`, incluido en Python.

## Instalación

Se necesita Python 3.13 y Git para clonar el repositorio. Si ya lo tienes, abre la consola dentro de `Unidad 1/APE 1` y continúa con la creación del entorno.

### Windows (PowerShell)

```powershell
git clone https://github.com/SteveJ4ra/Simulacion_5to_Ciclo.git
cd "Simulacion_5to_Ciclo\Unidad 1\APE 1"
python -m venv Proyecto\.venv
.\Proyecto\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### Linux y macOS (Bash o Zsh)

Comprueba que `python3 --version` corresponde a Python 3.13. Si tienes varias versiones, utiliza `python3.13` para crear el entorno.

```bash
git clone https://github.com/SteveJ4ra/Simulacion_5to_Ciclo.git
cd "Simulacion_5to_Ciclo/Unidad 1/APE 1"
python3 -m venv Proyecto/.venv
./Proyecto/.venv/bin/python -m pip install -r requirements.txt
```

En Linux, la instalación de Python debe incluir el soporte de `venv` de la versión utilizada. Si el comando de creación indica que falta ese componente, instálalo con el gestor de paquetes de tu distribución.

Los comandos siguientes utilizan directamente el Python del entorno virtual; puedes ejecutarlos sin activar el entorno.

## Configuración

Las mediciones están definidas en `Proyecto/Controlador/controlador.py`. En ese archivo también se configuran los pesos del modelo ajustado mediante `ModeloLluvia(0.45, 0.40, 0.15)`, en el orden humedad, nubosidad y temperatura.

Los pesos deben ser no negativos y sumar 1. La humedad y la nubosidad deben estar entre 0 y 100. Los cálculos, la interpolación y las reglas de clasificación están en `Proyecto/Modelo/modelo.py`.

## Uso

Todos los comandos se ejecutan desde la carpeta del APE. El programa muestra en consola las tablas de ambos modelos, su comparación y las horas clasificadas como lluvia. También abre las ventanas con las gráficas y guarda los resultados en `Proyecto/resultados/`.

### Windows (PowerShell)

Ejecutar con las ventanas de las gráficas:

```powershell
.\Proyecto\.venv\Scripts\python.exe .\Proyecto\Vista\main.py
```

Generar los resultados sin abrir ventanas:

```powershell
.\Proyecto\.venv\Scripts\python.exe .\Proyecto\Vista\main.py --sin-ventana
```

Elegir otra carpeta de salida:

```powershell
.\Proyecto\.venv\Scripts\python.exe .\Proyecto\Vista\main.py --sin-ventana --salida ".\Proyecto\resultados\comparacion"
```

Consultar las opciones:

```powershell
.\Proyecto\.venv\Scripts\python.exe .\Proyecto\Vista\main.py --help
```

### Linux y macOS (Bash o Zsh)

Ejecutar con las ventanas de las gráficas:

```bash
./Proyecto/.venv/bin/python ./Proyecto/Vista/main.py
```

Generar los resultados sin abrir ventanas, por ejemplo en una sesión sin escritorio gráfico:

```bash
./Proyecto/.venv/bin/python ./Proyecto/Vista/main.py --sin-ventana
```

Elegir otra carpeta de salida:

```bash
./Proyecto/.venv/bin/python ./Proyecto/Vista/main.py --sin-ventana --salida "./Proyecto/resultados/comparacion"
```

Consultar las opciones:

```bash
./Proyecto/.venv/bin/python ./Proyecto/Vista/main.py --help
```

## Estructura del proyecto

```text
APE 1/
├── Proyecto/
│   ├── Controlador/
│   │   └── controlador.py
│   ├── Modelo/
│   │   └── modelo.py
│   ├── Vista/
│   │   ├── main.py
│   │   └── graficas.py
│   ├── .venv/             # Entorno local, excluido de Git
│   └── resultados/        # Se genera al ejecutar el programa
├── JumboSteven_APE_1_U1.pdf
├── referencias.bib
├── requirements.txt
└── README.md
```

- **Modelo:** valida los datos y calcula el índice y el estado de lluvia.
- **Controlador:** prepara las mediciones y compara los dos modelos.
- **Vista:** contiene el ejecutable, muestra las tablas, dibuja las gráficas y guarda los archivos.

El desarrollo de la guía está en [JumboSteven_APE_1_U1.pdf](JumboSteven_APE_1_U1.pdf). Las fuentes citadas están disponibles en [referencias.bib](referencias.bib).

## Información adicional

Cada ejecución genera tres tablas (`modelo_original.csv`, `modelo_ajustado.csv` y `comparacion.csv`) y tres imágenes: `grafica_original.png`, `grafica_ajustado.png` y `simulacion.png`. Las dos primeras muestran cada modelo por separado; la última compara los índices e incluye la evolución de las mediciones atmosféricas.

| Índice | Clasificación |
| --- | --- |
| `I < 0.40` | Sin lluvia |
| `0.40 ≤ I < 0.60` | Baja posibilidad |
| `0.60 ≤ I < 0.75` | Lluvia probable |
| `I ≥ 0.75` | Lluvia |

El índice corresponde al modelo didáctico de la guía y no representa una probabilidad meteorológica calibrada. El `.gitignore` de la raíz del repositorio excluye el entorno virtual, la caché de Python y los resultados generados.

## Declaración de uso de IA

Para la presente actividad se ha usado el modelo de inteligencia artificial, GPT 6.1 Sol (Open AI), para acelerar el proceso de investigación de fuentes de calidad para responder las preguntas de control, en conjunto con NotebookLM (Google).

A su vez, se ha utilizado GPT, para entender la sintaxis aplicada en python, para aplicar el patrón arquitectónico "Modelo Vista Controlador (MVC)".

### Prompts utilizado

1. Investiga fuentes de investigación científica que contengan información clave para responder las siguientes preguntas de control presentadas en el documento "ape_guia simulacion semana 1-firmado-signed.pdf". Estas fuentes solo pueden ser de base científica, como papers, revistas, conferencias, congresos, libros, etc.
2. Muestrame un ejemplo básico de como se aplica el patrón Modelo Vista Controlador (MVC).
