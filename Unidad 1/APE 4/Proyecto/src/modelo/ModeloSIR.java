package modelo;

// Solo almacena los parámetros definidos en Main.
public class ModeloSIR {
    public final int poblacion;
    public final int infectadosIniciales;
    public final double beta;
    public final double gamma;
    public final int tiempoSimulacion;

    public ModeloSIR(int poblacion, int infectadosIniciales, double beta,
                     double gamma, int tiempoSimulacion) {
        this.poblacion = poblacion;
        this.infectadosIniciales = infectadosIniciales;
        this.beta = beta;
        this.gamma = gamma;
        this.tiempoSimulacion = tiempoSimulacion;
    }
}
