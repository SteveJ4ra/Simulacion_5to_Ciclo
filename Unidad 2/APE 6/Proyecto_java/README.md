# APE 6 · Java

Genera números pseudoaleatorios con un generador congruencial lineal (LCG) y comprueba su ajuste a la distribución uniforme con Chi-cuadrado y Kolmogorov-Smirnov (KS).

## Tecnologías

JDK 21 y Apache Commons Math 3.6.1. El JAR de la librería está incluido en `lib/`.

## Compilación y uso

Ejecuta estos comandos desde la carpeta `APE 6`.

**Windows (PowerShell)**

```powershell
cd Proyecto_java
$archivosJava = Get-ChildItem -Path Main.java, modelo, controlador, vista -Filter *.java -File -Recurse
javac -encoding UTF-8 -cp "lib/commons-math3-3.6.1.jar" -d out $archivosJava.FullName
java -cp "out;lib/commons-math3-3.6.1.jar" Main
```

**Linux y macOS**

```bash
cd Proyecto_java
javac -encoding UTF-8 -cp "lib/commons-math3-3.6.1.jar" -d out Main.java modelo/*.java controlador/*.java vista/*.java
java -cp "out:lib/commons-math3-3.6.1.jar" Main
```

La ejecución usa la semilla `12345` y genera `10000` valores. Añade `--semilla 42 --cantidad 5000` al comando de ejecución para probar otra muestra. Con `--help` puedes ver todas las opciones.

En `resultados_java/` se guardan tres CSV con la secuencia, las frecuencias y los resultados de las pruebas. Abre `ks_java.svg` en el navegador para comparar la distribución acumulada de la muestra con la uniforme.

## Estructura

- `Main.java`: recibe las opciones de la consola.
- `modelo/`: genera la secuencia y aplica las pruebas.
- `controlador/`: coordina la ejecución.
- `vista/`: muestra los resultados y exporta los archivos.

Las fuentes de la práctica están en [referencias.bib](../referencias.bib).
