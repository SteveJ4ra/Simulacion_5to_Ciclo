# Simulación SIR en Java y visualización en NetLogo — APE 4

Práctica de Simulación de la Universidad Nacional de Loja. Java calcula la
evolución de susceptibles, infectados y recuperados, exporta los conteos a CSV
y NetLogo permite reproducirlos mediante figuras, monitores y una gráfica SIR.

## Requisitos

- **JDK 11 o superior**, con `java` y `javac` disponibles en la terminal.
- **NetLogo 7.0.4** para abrir el archivo `modelo_sir.nlogox` incluido.

Se utiliza únicamente la biblioteca estándar de Java. No se necesita
`requirements.txt`, un entorno virtual, Maven ni Gradle. El modelo NetLogo
utiliza su extensión CSV.

## Compilar y ejecutar

Los comandos parten de la carpeta `APE 4`, donde está este README.

### Windows con PowerShell

```powershell
cd Proyecto
New-Item -ItemType Directory -Force out | Out-Null
$fuentes = Get-ChildItem -Path src -Recurse -Filter *.java | Select-Object -ExpandProperty FullName
javac -encoding UTF-8 -d out $fuentes
java -cp out Main
```

### Linux o macOS

```bash
cd Proyecto
mkdir -p out
javac -encoding UTF-8 -d out src/Main.java src/modelo/*.java src/controlador/*.java
java -cp out Main
```

Se genera `Proyecto/resultados/resultados_java.csv`. La carpeta se crea
automáticamente si no existe y cada ejecución reemplaza ese archivo.

Para usar otra semilla, desde `Proyecto`:

```bash
java -cp out Main 123
```

La semilla predeterminada es **42**. Con los mismos parámetros, semilla y código,
una nueva ejecución reproduce los mismos resultados.

## Visualizar en NetLogo

1. Abrir `Proyecto/resultados/modelo_sir.nlogox` con NetLogo 7.0.4.
2. Pulsar **Cargar CSV** y seleccionar `resultados_java.csv` en esa misma carpeta.
3. Usar **Avanzar un paso** o **Reproducir / Pausar** para recorrer los registros.
4. Pausar antes de pulsar **Reiniciar**, que vuelve al primer registro y limpia
   la gráfica.

Azul representa susceptibles; rojo, infectados; y verde, recuperados. La velocidad
de reproducción no cambia los valores calculados por Java.

NetLogo **visualiza los resultados generados por Java**: no ejecuta una segunda
simulación epidemiológica independiente. Cada figura representa una persona del
conteo; el CSV no guarda identidades, contactos ni posiciones individuales.

Se incluyen el modelo y el CSV de referencia para abrir la visualización sin
compilar primero. Si se cambian los parámetros en Java, hay que compilar, ejecutar
y cargar nuevamente el CSV actualizado en NetLogo.

## Estructura del proyecto

```text
APE 4/
├── .gitignore
├── README.md
├── referencias.bib
└── Proyecto/
    ├── src/
    │   ├── Main.java
    │   ├── modelo/
    │   │   ├── Estado.java
    │   │   ├── ModeloSIR.java
    │   │   └── Resultado.java
    │   └── controlador/
    │       ├── ControladorSimulacion.java
    │       └── ExportadorCSV.java
    ├── resultados/
    │   ├── modelo_sir.nlogox
    │   └── resultados_java.csv
    └── out/                         Generado al compilar; no se versiona
```

### Responsabilidades

- **Modelo:** `Estado`, `Resultado` y `ModeloSIR` guardan los estados, los conteos
  de cada instante y los parámetros.
- **Controlador:** `ControladorSimulacion` valida los parámetros, crea la población,
  simula los pasos y cuenta los estados. `ExportadorCSV` guarda los resultados.
- **Entrada:** `Main` configura el experimento, inicia el controlador y comunica
  si el archivo se generó o si ocurrió un error.
- **Visualización:** el modelo NetLogo carga el CSV y actualiza sus figuras,
  monitores y trazos.

## Parámetros y reglas

Los parámetros editables están al inicio de `main`, en `Proyecto/src/Main.java`.
Allí también se configuran la semilla y la ruta del CSV.

| Parámetro | Valor de referencia |
| --- | --- |
| Población | 100 |
| Susceptibles iniciales | 95 |
| Infectados iniciales | 5 |
| Recuperados iniciales | 0 |
| Beta: transmisión | 0,30 |
| Gamma: recuperación por paso | 0,10 |
| Pasos de simulación | 100 |
| Semilla | 42 |

Las fórmulas están separadas en dos métodos del controlador:

- `calcularContagiosEsperados(S, I)`: `beta * S * I / N`.
- `calcularRecuperacionesEsperadas(I)`: `gamma * I`.

Se usa un paso de tiempo de una unidad. Los valores esperados se dividen por el
tamaño del grupo para obtener las probabilidades individuales:
`p(contagio) = beta * I / N` y `p(recuperación) = gamma`.
Se sortea cada cambio de estado; los grupos vacíos se manejan sin dividir entre cero.

Se lee la población al inicio del paso y se escriben los cambios en una copia.
Un nuevo infectado comienza a contagiar y puede recuperarse desde el siguiente
paso. Un infectado que se recupera todavía puede transmitir durante ese paso.
Los recuperados no vuelven a infectarse.

Es una simulación aleatoria de individuos con actualización simultánea de estados,
no una integración numérica de ecuaciones diferenciales. Los conteos son enteros
y se conserva `S + I + R = 100` en la configuración de referencia.

La interfaz incluida representa 100 personas y tiempos de 0 a 100. Si se cambia
esa configuración, también deben revisarse los rótulos, los límites de la gráfica
y la distribución visual en NetLogo.

## Datos exportados y resultados de referencia

```csv
tiempo,susceptibles,infectados,recuperados
0,95,5,0
1,94,5,1
2,90,9,1
```

El CSV usa UTF-8 y comas como separadores. Contiene un encabezado y **101 filas de
datos**, del tiempo 0 al 100. Se registra el estado inicial y después de cada paso.
Aunque no queden infectados, el registro continúa hasta el tiempo configurado.

| Tiempo | Susceptibles | Infectados | Recuperados |
| --- | --- | --- | --- |
| 0 | 95 | 5 | 0 |
| 15 | 32 | 45 | 23 |
| 16 | 29 | 45 | 26 |
| 57 | 2 | 0 | 98 |
| 100 | 2 | 0 | 98 |

El máximo de infectados es 45 en los tiempos 15 y 16. Desde el tiempo 57 no quedan
infectados en esta ejecución.

## Referencias

Las fuentes se incluyen en [`referencias.bib`](referencias.bib):

- [Oracle: java.util.Random, Java SE 21](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/Random.html).
- [NetLogo: Programming Guide](https://docs.netlogo.org/programming.html).
- [NetLogo: CSV Extension](https://docs.netlogo.org/csv.html).

Uso académico para la asignatura Simulación, carrera de Computación, ciclo 5.
