package controlador;

import java.io.IOException;
import java.nio.file.Path;
import modelo.GeneradorLCG;
import modelo.Pruebas;
import vista.Consola;
import vista.Exportacion;

public final class Controlador {
    private Controlador() { }

    public static void ejecutar(GeneradorLCG config, Path salida) throws IOException {
        long[] valores = config.generar();
        Pruebas resultado = new Pruebas(valores, config.m);
        Consola.mostrar(config, valores, resultado);
        Exportacion.guardar(config, valores, resultado, salida);
    }
}
