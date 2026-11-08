import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.InvalidPathException;
import controlador.Controlador;
import modelo.GeneradorLCG;

public final class Main {
    private Main() { }

    public static void main(String[] args) {
        long semilla = 12345;
        long a = 1664525;
        long c = 1013904223;
        long m = 1L << 32;
        int cantidad = 10000;
        Path salida = Path.of("resultados_java");
        try {
            for (int i = 0; i < args.length; i++) {
                String opcion = args[i];
                if (opcion.equals("--help")) {
                    System.out.println("--semilla N --a N --c N --m N --cantidad N --salida CARPETA");
                    System.out.println("Cantidad predeterminada: 10 000. La carpeta de salida reemplaza archivos del mismo nombre.");
                    return;
                }
                if (i + 1 >= args.length) {
                    throw new IllegalArgumentException("Falta el valor de " + opcion);
                }
                String valor = args[++i];
                switch (opcion) {
                    case "--semilla":
                        semilla = Long.parseLong(valor);
                        break;
                    case "--a":
                        a = Long.parseLong(valor);
                        break;
                    case "--c":
                        c = Long.parseLong(valor);
                        break;
                    case "--m":
                        m = Long.parseLong(valor);
                        break;
                    case "--cantidad":
                        cantidad = Integer.parseInt(valor);
                        break;
                    case "--salida":
                        salida = Path.of(valor);
                        break;
                    default:
                        throw new IllegalArgumentException("Opción desconocida: " + opcion);
                }
            }
            GeneradorLCG config = new GeneradorLCG(semilla, a, c, m, cantidad);
            Controlador.ejecutar(config, salida);
        } catch (NumberFormatException error) {
            System.err.println("Error: los parámetros numéricos deben ser enteros dentro del rango permitido.");
            System.exit(1);
        } catch (IllegalArgumentException error) {
            System.err.println("Configuración inválida: " + error.getMessage());
            System.exit(1);
        } catch (IOException | SecurityException error) {
            System.err.println("No se pudieron guardar los resultados: " + error.getMessage());
            System.exit(1);
        }
    }
}
