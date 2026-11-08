package vista;

import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Arrays;
import java.util.Locale;
import modelo.GeneradorLCG;
import modelo.Pruebas;

public final class Exportacion {
    private Exportacion() { }

    public static void guardar(GeneradorLCG config, long[] valores, Pruebas resultado, Path carpeta) throws IOException {
        Files.createDirectories(carpeta);
        guardarSecuencia(config, valores, carpeta);
        guardarFrecuencias(resultado, carpeta);
        guardarPruebas(resultado, carpeta);
        guardarGrafica(config, valores, carpeta);
        System.out.println("Resultados guardados en: " + carpeta.toAbsolutePath());
    }

    private static void guardarSecuencia(GeneradorLCG config, long[] valores, Path carpeta) throws IOException {
        Path archivo = carpeta.resolve("secuencia_java.csv");
        try (BufferedWriter escritor = Files.newBufferedWriter(archivo, StandardCharsets.UTF_8)) {
            escritor.write("n,X,U\n");
            for (int i = 0; i < valores.length; i++) {
                escritor.write(String.format(Locale.ROOT, "%d,%d,%.17g%n", i + 1, valores[i], (double) valores[i] / config.m));
            }
        }
    }

    private static void guardarFrecuencias(Pruebas resultado, Path carpeta) throws IOException {
        try (BufferedWriter escritor = Files.newBufferedWriter(carpeta.resolve("frecuencias_java.csv"), StandardCharsets.UTF_8)) {
            escritor.write("desde,hasta_excluido,observada,esperada\n");
            for (int i = 0; i < Pruebas.INTERVALOS; i++) {
                escritor.write(String.format(Locale.ROOT, "%.1f,%.1f,%d,%.1f%n", i / 10.0, (i + 1) / 10.0, resultado.frecuencias[i], resultado.esperada));
            }
        }
    }

    private static void guardarPruebas(Pruebas resultado, Path carpeta) throws IOException {
        try (BufferedWriter escritor = Files.newBufferedWriter(carpeta.resolve("pruebas_java.csv"), StandardCharsets.UTF_8)) {
            escritor.write("prueba,estadistico,valor_p,alfa,decision\n");
            escritor.write(String.format(Locale.ROOT, "Chi-cuadrado,%.17g,%.17g,0.05,%s%n", resultado.chi, resultado.pChi, Pruebas.decidir(resultado.pChi)));
            escritor.write(String.format(Locale.ROOT, "KS asintotico,%.17g,%.17g,0.05,%s%n", resultado.d, resultado.pKs, Pruebas.decidir(resultado.pKs)));
        }
    }

    private static void guardarGrafica(GeneradorLCG config, long[] valores, Path carpeta) throws IOException {
        long[] ordenados = valores.clone();
        Arrays.sort(ordenados);
        StringBuilder svg = new StringBuilder();
        svg.append("<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 900 500\">\n");
        svg.append("<rect width=\"900\" height=\"500\" fill=\"white\"/>\n");
        svg.append("<g font-family=\"sans-serif\" font-size=\"16\">\n");
        svg.append("<text x=\"180\" y=\"25\">Distribución acumulada: empírica y uniforme</text>\n");
        svg.append("<text x=\"65\" y=\"460\">0</text><text x=\"840\" y=\"460\">1</text>\n");
        svg.append("<text x=\"20\" y=\"45\">1</text><text x=\"20\" y=\"430\">0</text>\n");
        svg.append("<text x=\"440\" y=\"490\">U</text><text x=\"15\" y=\"230\">F(U)</text>\n");
        svg.append("<text x=\"620\" y=\"60\" fill=\"red\">Uniforme teórica</text>\n");
        svg.append("<text x=\"620\" y=\"80\" fill=\"blue\">Empírica</text></g>\n");
        svg.append("<path d=\"M70 40 V430 H850\" fill=\"none\" stroke=\"black\"/>\n");
        svg.append("<path d=\"M70 430 L850 40\" stroke=\"red\" stroke-dasharray=\"5 5\"/>\n");
        svg.append("<path fill=\"none\" stroke=\"blue\" d=\"M70 430 ");
        for (int i = 0; i < ordenados.length; i++) {
            double x = 70 + 780.0 * ordenados[i] / config.m;
            double y = 430 - 390.0 * (i + 1) / ordenados.length;
            svg.append(String.format(Locale.ROOT, "H%.3f V%.3f ", x, y));
        }
        svg.append("H850\"/></svg>\n");
        Files.writeString(carpeta.resolve("ks_java.svg"), svg, StandardCharsets.UTF_8);
    }
}
