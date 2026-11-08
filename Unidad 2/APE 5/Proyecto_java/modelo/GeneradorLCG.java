package modelo;

/** La semilla es X0. La primera observación devuelta es X1. */
public final class GeneradorLCG {
    public static final long A = 1664525L, C = 1013904223L, M = 1L << 32;
    public static final int MAX_CANTIDAD = 1_000_000;
    private long estado;

    public GeneradorLCG(long semilla) {
        if (semilla < 0 || semilla >= M)
            throw new IllegalArgumentException("La semilla debe estar entre 0 y " + (M-1) + ".");
        estado = semilla;
    }

    public long siguiente() {
        // El producto máximo cabe en long; se evita el desbordamiento de int.
        estado = (A * estado + C) % M;
        return estado;
    }

    public long[] generar(int cantidad) {
        if (cantidad < 1 || cantidad > MAX_CANTIDAD)
            throw new IllegalArgumentException("La cantidad debe estar entre 1 y " + MAX_CANTIDAD + ".");
        long[] valores = new long[cantidad];
        for (int i = 0; i < cantidad; i++) valores[i] = siguiente();
        return valores;
    }
}
