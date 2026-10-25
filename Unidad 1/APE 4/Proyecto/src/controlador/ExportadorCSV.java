package controlador;

import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import modelo.Resultado;

public class ExportadorCSV {
    public void exportar(List<Resultado> resultados, Path archivo) throws IOException {
        Path carpeta = archivo.toAbsolutePath().getParent();
        Files.createDirectories(carpeta);
        try (BufferedWriter escritor = Files.newBufferedWriter(archivo, StandardCharsets.UTF_8)) {
            escritor.write("tiempo,susceptibles,infectados,recuperados");
            escritor.newLine();
            for (Resultado resultado : resultados) {
                escritor.write(resultado.tiempo + "," + resultado.susceptibles + ","
                        + resultado.infectados + "," + resultado.recuperados);
                escritor.newLine();
            }
        }
    }
}
