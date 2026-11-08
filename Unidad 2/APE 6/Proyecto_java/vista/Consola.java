package vista;

import java.util.Locale;
import modelo.GeneradorLCG;
import modelo.Pruebas;

public final class Consola {
    private Consola() { }

    public static void mostrar(GeneradorLCG config, long[] valores, Pruebas resultado) {
        System.out.printf("n=%d, semilla=%d, a=%d, c=%d, m=%d%n",
                config.cantidad, config.semilla, config.a, config.c, config.m);
        System.out.println("Primeros 20 valores (la secuencia comienza en X1):");
        for (int i = 0; i < Math.min(20, valores.length); i++) {
            System.out.printf(Locale.ROOT, "%4d X=%12d U=%.12f%n", i + 1, valores[i], (double) valores[i] / config.m);
        }
        System.out.printf("%-15s%12s%12s%n", "Intervalo", "Observada", "Esperada");
        for (int i = 0; i < Pruebas.INTERVALOS; i++) {
            String intervalo = String.format(Locale.ROOT, "[%.1f, %.1f)", i / 10.0, (i + 1) / 10.0);
            System.out.printf(Locale.ROOT, "%-15s%12d%12.2f%n", intervalo, resultado.frecuencias[i], resultado.esperada);
        }
        imprimirPrueba("Chi-cuadrado (gl=9)", resultado.chi, resultado.pChi);
        imprimirPrueba("KS bilateral", resultado.d, resultado.pKs);
        System.out.printf(Locale.ROOT, "D+=%.8f, D-=%.8f%n", resultado.dMas, resultado.dMenos);
        System.out.println("KS usa un valor p asintótico (aproximado), especialmente apropiado para la muestra de 10 000 datos.");
        System.out.println("Las pruebas contrastan uniformidad con una referencia continua; no prueban independencia ni aleatoriedad.");
    }

    private static void imprimirPrueba(String nombre, double estadistico, double valorP) {
        System.out.printf(Locale.ROOT, "%s: estadístico=%.8f, p=%.8g, %s (alfa=0.05)%n",
                nombre, estadistico, valorP, Pruebas.decidir(valorP));
    }
}
