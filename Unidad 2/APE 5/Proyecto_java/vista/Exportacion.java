package vista;

import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;
import java.util.Locale;
import modelo.GeneradorLCG;
import modelo.Resultado;

/** Exportación opcional usando únicamente la biblioteca estándar. */
public final class Exportacion {
    private Exportacion() { }

    public static void exportar(Resultado[] resultados, Path carpeta) throws IOException {
        Path[] nombres = {carpeta.resolve("secuencias_java.csv"),
            carpeta.resolve("secuencia_java_1_semilla_" + resultados[0].semilla + ".svg"),
            carpeta.resolve("secuencia_java_2_semilla_" + resultados[1].semilla + ".svg")};
        for (Path p : nombres) if (Files.exists(p))
            throw new IOException("Ya existen resultados en esa carpeta. Elige otra carpeta.");
        Files.createDirectories(carpeta);
        Resultado a = resultados[0], b = resultados[1];
        try (BufferedWriter archivo = Files.newBufferedWriter(nombres[0], StandardCharsets.UTF_8,
                StandardOpenOption.CREATE_NEW)) {
            archivo.write("n,X_semilla_" + a.semilla + ",U_semilla_" + a.semilla
                          + ",X_semilla_" + b.semilla + ",U_semilla_" + b.semilla + "\n");
            for (int i = 0; i < a.valores.length; i++) {
                long x = a.valores[i], y = b.valores[i];
                archivo.write(String.format(Locale.ROOT,"%d,%d,%.12f,%d,%.12f\n",i+1,
                    x,(double)x/GeneradorLCG.M,y,(double)y/GeneradorLCG.M));
            }
        }
        for (int i = 0; i < resultados.length; i++)
            Files.writeString(nombres[i+1],graficaSvg(resultados[i]),StandardCharsets.UTF_8,
                              StandardOpenOption.CREATE_NEW);
        System.out.println("CSV y gráficas SVG guardados en: " + carpeta.toAbsolutePath());
    }

    public static String graficaSvg(Resultado r) {
        StringBuilder puntos = new StringBuilder();
        for (int i = 0; i < r.valores.length; i++)
            puntos.append(String.format(Locale.ROOT,"%.3f,%.3f ",
                70+i*880.0/Math.max(1,r.valores.length-1),350-(double)r.valores[i]/GeneradorLCG.M*280));
        return "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 1000 430\">"
            + "<rect width=\"1000\" height=\"430\" fill=\"white\"/>"
            + "<g font-family=\"sans-serif\" font-size=\"16\" fill=\"#172b4d\">"
            + "<text x=\"70\" y=\"30\">LCG: semilla " + r.semilla + ", " + r.valores.length + " observaciones</text>"
            + "<text x=\"15\" y=\"65\">U(n)</text><text x=\"38\" y=\"76\">1</text>"
            + "<text x=\"38\" y=\"355\">0</text><text x=\"70\" y=\"380\">1</text>"
            + "<text x=\"925\" y=\"380\">" + r.valores.length + "</text>"
            + "<text x=\"440\" y=\"410\">Observación n</text></g>"
            + "<path d=\"M70 70 V350 H950\" fill=\"none\" stroke=\"#172b4d\"/>"
            + "<polyline points=\"" + puntos + "\" fill=\"none\" stroke=\"#2463b4\" stroke-width=\"0.6\"/></svg>";
    }
}
