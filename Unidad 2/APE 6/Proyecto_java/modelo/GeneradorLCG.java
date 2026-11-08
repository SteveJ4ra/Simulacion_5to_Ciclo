package modelo;

import java.math.BigInteger;

public final class GeneradorLCG {
    public final long semilla;
    public final long a;
    public final long c;
    public final long m;
    public final int cantidad;

    public GeneradorLCG(long semilla, long a, long c, long m, int cantidad) {
        if (m < 2 || m > (1L << 32)) {
            throw new IllegalArgumentException("El módulo debe estar entre 2 y 2^32.");
        }
        if (semilla < 0 || semilla >= m || a < 0 || a >= m || c < 0 || c >= m) {
            throw new IllegalArgumentException("Semilla, multiplicador e incremento deben estar entre 0 y m - 1.");
        }
        if (cantidad < 50 || cantidad > 1_000_000) {
            throw new IllegalArgumentException("La cantidad debe estar entre 50 y 1 000 000 (frecuencia esperada mínima: 5).");
        }
        this.semilla = semilla;
        this.a = a;
        this.c = c;
        this.m = m;
        this.cantidad = cantidad;
    }

    public long[] generar() {
        long[] valores = new long[cantidad];
        BigInteger estado = BigInteger.valueOf(semilla);
        BigInteger multiplicador = BigInteger.valueOf(a);
        BigInteger incremento = BigInteger.valueOf(c);
        BigInteger modulo = BigInteger.valueOf(m);
        // BigInteger evita desbordar long al multiplicar parámetros grandes.
        for (int i = 0; i < cantidad; i++) {
            estado = estado.multiply(multiplicador).add(incremento).mod(modulo);
            valores[i] = estado.longValueExact();
        }
        return valores;
    }
}
