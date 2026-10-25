import controlador.ControladorSimulacion;
import modelo.ModeloSIR;
import java.io.IOException;
import java.nio.file.Path;

public class Main {
    public static void main(String[] args) {
        // CONFIGURACIÓN: cambia estos valores para otro experimento.
        int poblacion = 100;
        int infectadosIniciales = 5;
        double beta = 0.30;
        double gamma = 0.10;
        int tiempoSimulacion = 100;
        long semillaPredeterminada = 42L;
        Path archivo = Path.of("resultados", "resultados_java.csv");

        if (args.length > 1) {
            System.err.println("Uso: java -cp out Main [semilla_entera]");
            System.exit(1);
        }
        try {
            // Una semilla fija permite repetir el experimento.
            long semilla = args.length == 1 ? Long.parseLong(args[0]) : semillaPredeterminada;
            ModeloSIR parametros = new ModeloSIR(poblacion, infectadosIniciales,
                    beta, gamma, tiempoSimulacion);
            new ControladorSimulacion().ejecutar(parametros, semilla, archivo);
            System.out.println("CSV generado: " + archivo.toAbsolutePath());
            System.out.println("Semilla utilizada: " + semilla);
        } catch (NumberFormatException e) {
            System.err.println("La semilla debe ser un número entero válido de tipo long.");
            System.exit(1);
        } catch (IllegalArgumentException e) {
            System.err.println("Configuración inválida: " + e.getMessage());
            System.exit(1);
        } catch (IOException e) {
            System.err.println("No se pudo guardar el CSV: " + e.getMessage());
            System.exit(1);
        }
    }
}
