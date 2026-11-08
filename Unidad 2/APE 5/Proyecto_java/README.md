# APE 5 · Java

Implementación del generador congruencial lineal (LCG) con JDK 11 o posterior y la biblioteca estándar de Java.

## Compilación y ejecución

Desde la carpeta `APE 5`, ejecuta los comandos de tu sistema.

**Windows (PowerShell)**

```powershell
cd Proyecto_java
$archivos = Get-ChildItem -Path Main.java, modelo, controlador, vista -Filter *.java -File -Recurse
javac -encoding UTF-8 -d bin $archivos.FullName
java -cp bin Main --exportar ../resultados/java
```

**Linux y macOS**

```bash
cd Proyecto_java
javac -encoding UTF-8 -d bin Main.java modelo/*.java controlador/*.java vista/*.java
java -cp bin Main --exportar ../resultados/java
```

Por defecto, el programa genera 10 000 valores para cada semilla (`12345` y `54321`). Usa `--semilla`, `--comparar-semilla` y `--cantidad` para cambiar la configuración. Consulta las opciones con `java -cp bin Main --help`.

Con `--exportar` se guardan el CSV y las gráficas SVG. Si la carpeta ya tiene archivos con esos nombres, elige otra para la nueva ejecución.

## Estructura

- `Main.java` recibe las opciones de consola.
- `modelo/` genera y guarda la secuencia.
- `controlador/` calcula las estadísticas y coordina la ejecución.
- `vista/` muestra y exporta los resultados.

[Bibliografía](../referencias.bib)
