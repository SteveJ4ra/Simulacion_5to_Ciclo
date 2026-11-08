package modelo;

import java.util.Arrays;
import org.apache.commons.math3.special.Gamma;
import org.apache.commons.math3.stat.inference.KolmogorovSmirnovTest;

public final class Pruebas {
    public static final int INTERVALOS = 10;
    public static final double ALFA = 0.05;
    public final int[] frecuencias;
    public final double esperada;
    public final double chi;
    public final double pChi;
    public final double dMas;
    public final double dMenos;
    public final double d;
    public final double pKs;

    public Pruebas(long[] valores, long modulo) {
        validarMuestra(valores, modulo);
        int cantidad = valores.length;
        frecuencias = new int[INTERVALOS];
        for (long valor : valores) {
            int indice = (int) (valor * INTERVALOS / modulo);
            frecuencias[indice]++;
        }
        esperada = cantidad / (double) INTERVALOS;
        double suma = 0;
        for (int observada : frecuencias) {
            double diferencia = observada - esperada;
            suma += diferencia * diferencia / esperada;
        }
        chi = suma;
        // La cola superior de Chi-cuadrado se obtiene mediante gamma regularizada.
        pChi = Gamma.regularizedGammaQ((INTERVALOS - 1) / 2.0, chi / 2);

        long[] ordenados = valores.clone();
        Arrays.sort(ordenados);
        double mayorPositiva = 0;
        double mayorNegativa = 0;
        for (int i = 0; i < cantidad; i++) {
            double uniforme = (double) ordenados[i] / modulo;
            double diferenciaMas = (i + 1.0) / cantidad - uniforme;
            double diferenciaMenos = uniforme - (double) i / cantidad;
            mayorPositiva = Math.max(mayorPositiva, diferenciaMas);
            mayorNegativa = Math.max(mayorNegativa, diferenciaMenos);
        }
        dMas = mayorPositiva;
        dMenos = mayorNegativa;
        d = Math.max(dMas, dMenos);
        pKs = calcularValorPKs(Math.sqrt(cantidad) * d);
    }

    private static void validarMuestra(long[] valores, long modulo) {
        if (modulo < 2 || modulo > (1L << 32)) {
            throw new IllegalArgumentException("El módulo debe estar entre 2 y 2^32.");
        }
        if (valores == null || valores.length < 50 || valores.length > 1_000_000) {
            throw new IllegalArgumentException("Se necesitan entre 50 y 1 000 000 datos.");
        }
        for (long valor : valores) {
            if (valor < 0 || valor >= modulo) {
                throw new IllegalArgumentException("Cada valor debe estar entre 0 y m - 1.");
            }
        }
    }

    private static double calcularValorPKs(double z) {
        if (z < 0.1) {
            return 1.0;
        }
        if (z < 1.0) {
            double acumulada = new KolmogorovSmirnovTest().ksSum(z, 1e-12, 100000);
            return Math.max(0, Math.min(1, 1 - acumulada));
        }
        // Serie de Kolmogorov: calcular la cola directamente conserva valores p pequeños.
        double suma = 0;
        for (int i = 1; i <= 100000; i++) {
            double termino = Math.exp(-2.0 * i * i * z * z);
            if (i % 2 == 1) {
                suma += termino;
            } else {
                suma -= termino;
            }
            if (termino < 1e-16) {
                break;
            }
        }
        return Math.max(0, Math.min(1, 2 * suma));
    }

    public static String decidir(double valorP) {
        if (valorP >= ALFA) {
            return "No se rechaza H0";
        }
        return "Se rechaza H0";
    }
}
