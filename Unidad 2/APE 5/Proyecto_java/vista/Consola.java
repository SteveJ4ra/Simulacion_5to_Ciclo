package vista;

import java.util.Locale;
import modelo.GeneradorLCG;
import modelo.Resultado;

public final class Consola {
    private Consola() { }

    public static void mostrar(Resultado[] resultados, boolean completo) {
        Resultado a = resultados[0], b = resultados[1];
        System.out.println("GENERADOR CONGRUENCIAL LINEAL - JAVA");
        System.out.printf("a=%d; c=%d; m=%d; U(n)=X(n)/m. La tabla comienza en X1.%n",
                          GeneradorLCG.A, GeneradorLCG.C, GeneradorLCG.M);
        System.out.printf("Semillas: %d y %d%n", a.semilla, b.semilla);
        System.out.printf("%4s %20s %16s %20s %16s%n", "n", "X primera semilla", "U", "X segunda semilla", "U");
        for (int i = 0; i < Math.min(20,a.valores.length); i++) {
            long x = a.valores[i], y = b.valores[i];
            System.out.printf(Locale.ROOT, "%4d %20d %16.12f %20d %16.12f%n", i+1,
                x, (double)x/GeneradorLCG.M, y, (double)y/GeneradorLCG.M);
        }
        for (Resultado r : resultados) {
            long minimo = r.valores[0], maximo = r.valores[0];
            for (long x : r.valores) { minimo = Math.min(minimo,x); maximo = Math.max(maximo,x); }
            System.out.printf("%nSemilla: %d; observaciones: %d%n",r.semilla,r.valores.length);
            System.out.printf(Locale.ROOT,"Media: %.12f; varianza poblacional: %.12f%n",r.media,r.varianza);
            System.out.printf(Locale.ROOT,"Mínimo U: %.12f; máximo U: %.12f%n",
                              (double)minimo/GeneradorLCG.M,(double)maximo/GeneradorLCG.M);
            System.out.println("Repetidos en la muestra: " + r.repetidos + "\nSHA-256: " + r.huella);
        }
        int iguales = 0;
        for (int i = 0; i < a.valores.length; i++) if (a.valores[i] == b.valores[i]) iguales++;
        System.out.println("\nCoincidencias en la misma posición entre semillas: " + iguales);
        System.out.println("Referencia uniforme [0,1): media 0.5; varianza 1/12 = 0.083333333333.");
        if (completo) System.out.println("Período teórico: " + GeneradorLCG.M
            + " (Hull-Dobell: c impar y a-1 múltiplo de 4).");
        System.out.println("Una muestra sin repeticiones no demuestra el período ni la independencia.");
        System.out.println("Compara los enteros y SHA-256 con Python usando las mismas semillas y cantidad.");
    }
}
