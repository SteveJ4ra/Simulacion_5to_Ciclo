package modelo;

public final class Resultado {
    public final long semilla;
    public final long[] valores;
    public final double media, varianza;
    public final int repetidos;
    public final String huella;

    public Resultado(long semilla, long[] valores, double media, double varianza,
                     int repetidos, String huella) {
        this.semilla = semilla;
        this.valores = valores;
        this.media = media;
        this.varianza = varianza;
        this.repetidos = repetidos;
        this.huella = huella;
    }
}
