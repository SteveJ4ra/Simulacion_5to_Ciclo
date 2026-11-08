package controlador;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Path;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.HashSet;
import java.util.Set;
import modelo.GeneradorLCG;
import modelo.Resultado;
import vista.Consola;
import vista.Exportacion;

public final class Controlador {
    private Controlador() { }

    public static Resultado analizar(long semilla, int cantidad) {
        long[] valores = new GeneradorLCG(semilla).generar(cantidad);
        double media = 0, acumulado = 0;
        Set<Long> distintos = new HashSet<>();
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            for (int i = 0; i < cantidad; i++) {
                double u = (double) valores[i] / GeneradorLCG.M;
                double delta = u - media;
                media += delta / (i + 1);
                acumulado += delta * (u - media);
                distintos.add(valores[i]);
                digest.update((Long.toString(valores[i]) + "\n").getBytes(StandardCharsets.US_ASCII));
            }
            StringBuilder huella = new StringBuilder();
            for (byte b : digest.digest()) huella.append(String.format("%02x", b & 0xff));
            return new Resultado(semilla, valores, media, acumulado/cantidad,
                                 cantidad-distintos.size(), huella.toString());
        } catch (NoSuchAlgorithmException error) {
            throw new IllegalStateException("SHA-256 no está disponible.", error);
        }
    }

    public static boolean periodoCompleto() {
        // Hull-Dobell para m=2^32: único factor primo 2 y m divisible por 4.
        return GeneradorLCG.C % 2 == 1 && (GeneradorLCG.A-1) % 2 == 0
            && (GeneradorLCG.A-1) % 4 == 0;
    }

    public static void ejecutar(long semilla, long otraSemilla, int cantidad, Path carpeta) throws IOException {
        Resultado[] resultados = {analizar(semilla,cantidad), analizar(otraSemilla,cantidad)};
        Consola.mostrar(resultados, periodoCompleto());
        if (carpeta != null) Exportacion.exportar(resultados,carpeta);
    }
}
