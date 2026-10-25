package modelo;

// Guarda los conteos de la población en un instante de la simulación.
public class Resultado {
    public final int tiempo;
    public final int susceptibles;
    public final int infectados;
    public final int recuperados;

    public Resultado(int tiempo, int susceptibles, int infectados, int recuperados) {
        this.tiempo = tiempo;
        this.susceptibles = susceptibles;
        this.infectados = infectados;
        this.recuperados = recuperados;
    }
}
