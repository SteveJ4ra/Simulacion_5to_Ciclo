import controlador.Controlador;
import java.io.IOException;
import java.nio.file.Path;

/**
 * JDK 11+. Desde Proyecto_java:
 * javac -encoding UTF-8 -d bin Main.java modelo/*.java controlador/*.java vista/*.java
 * java -cp bin Main
 * Opciones: --semilla 12345 --comparar-semilla 54321 --cantidad 10000
 * --exportar CARPETA guarda CSV y gráficas SVG. No requiere bibliotecas externas.
 */
public final class Main {
    private Main() { }
    public static void main(String[] args) {
        long semilla = 12345, otraSemilla = 54321;
        int cantidad = 10_000;
        Path carpeta = null;
        try {
            for (int i = 0; i < args.length; i++) {
                String opcion = args[i];
                if (opcion.equals("--help") || opcion.equals("--ayuda")) {
                    System.out.println("Uso: java -cp bin Main [--semilla N] [--comparar-semilla N]"
                        + " [--cantidad N] [--exportar CARPETA]");
                    return;
                }
                if (i+1 >= args.length) throw new IllegalArgumentException("Falta el valor de " + opcion);
                String valor = args[++i];
                switch (opcion) {
                    case "--semilla": semilla = Long.parseLong(valor); break;
                    case "--comparar-semilla": otraSemilla = Long.parseLong(valor); break;
                    case "--cantidad": cantidad = Integer.parseInt(valor); break;
                    case "--exportar": carpeta = Path.of(valor); break;
                    default: throw new IllegalArgumentException("Opción desconocida: " + opcion);
                }
            }
            Controlador.ejecutar(semilla,otraSemilla,cantidad,carpeta);
        } catch (IllegalArgumentException | IOException error) {
            System.err.println("Error: " + error.getMessage());
            System.exit(1);
        }
    }
}
