import time

from controlador.estadisticas import error_relativo

VERDE = "\033[32m"
AZUL = "\033[34m"
AMARILLO = "\033[33m"
GRIS = "\033[90m"
NORMAL = "\033[0m"
BORRAR_HACIA_ABAJO = "\033[J"


def subir_lineas(cantidad):
    return f"\033[{cantidad}F"


def esperar(segundos):
    time.sleep(segundos)


def barra_progreso(actual, total, ancho=40):
    llenos = int(actual / total * ancho)
    porcentaje = actual / total * 100
    barra = VERDE + "█" * llenos + GRIS + "░" * (ancho - llenos) + NORMAL
    return f"  Progreso {barra} {porcentaje:5.1f}%  (minuto {actual:.0f} de {total})"


def dibujar_cola(foto, maximo):
    cola = ""
    for numero in foto.cola[:maximo]:
        cola = f"C{numero} " + cola
    if len(foto.cola) > maximo:
        cola = f"+{len(foto.cola) - maximo} " + cola

    servidor = "libre"
    if foto.en_servicio > 0:
        servidor = f"C{foto.en_servicio}"

    return f"  Llegan → [ {cola}] → [ Servidor: {servidor} ] → Salen"


def dibujar_barras(valores, referencia, alto):
    maximo = max(valores + [referencia, 1])
    lineas = []
    for fila in range(alto, 0, -1):
        nivel = maximo * fila / alto
        es_referencia = abs(nivel - referencia) <= maximo / alto / 2
        linea = f"  {nivel:6.1f} |"
        for valor in valores:
            if valor >= nivel:
                linea += "█"
            elif es_referencia:
                linea += AMARILLO + "·" + NORMAL
            else:
                linea += " "
        lineas.append(linea)
    lineas.append("         +" + "-" * len(valores))
    return "\n".join(lineas)


def barra_horizontal(valor, maximo, color, ancho=40):
    largo = int(valor / maximo * ancho)
    return color + "█" * largo + NORMAL + " " * (ancho - largo)


def armar_pantalla(resultado, foto, tamanos, config):
    t = resultado.teoricas
    maximo_wq = max(foto.espera_promedio, t.Wq) * 1.1

    pantalla = barra_progreso(foto.tiempo, config["MINUTOS_ANIMADOS"]) + "\n\n"
    pantalla += "COLA FIFO (el primero en llegar es el primero en ser atendido)\n"
    pantalla += dibujar_cola(foto, config["CLIENTES_VISIBLES"]) + "\n\n"
    pantalla += f"CLIENTES EN LA COLA ({AMARILLO}·····{NORMAL} = Lq teórico {t.Lq:.3f})\n"
    pantalla += dibujar_barras(tamanos, t.Lq, config["ALTO_GRAFICA"]) + "\n\n"
    pantalla += "TIEMPO PROMEDIO DE ESPERA EN LA COLA (Wq)\n"
    pantalla += f"  Simulado  {barra_horizontal(foto.espera_promedio, maximo_wq, AZUL)} {foto.espera_promedio:.3f}\n"
    pantalla += f"  Teórico   {barra_horizontal(t.Wq, maximo_wq, AMARILLO)} {t.Wq:.3f}"
    return pantalla


def animar(resultado, total, config):
    e = resultado.escenario
    print("=" * 78)
    print(f"ESCENARIO {e.numero} de {total}  |  λ = {e.lam}  μ = {e.mu}  ρ = {e.utilizacion():.3f}  |  {e.condicion}")
    print("=" * 78)

    if not resultado.fue_simulado():
        print("  ⚠ " + resultado.mensaje + "\n")
        return

    tamanos = []
    lineas_anteriores = 0
    for foto in resultado.fotos:
        tamanos.append(len(foto.cola))
        pantalla = armar_pantalla(resultado, foto, tamanos, config)

        if lineas_anteriores > 0:
            print(subir_lineas(lineas_anteriores) + BORRAR_HACIA_ABAJO, end="")
        print(pantalla, flush=True)

        lineas_anteriores = pantalla.count("\n") + 1
        esperar(config["SEGUNDOS_POR_PASO"])
    print()


def mostrar_resultados(resultado):
    if not resultado.fue_simulado():
        return
    t = resultado.teoricas
    s = resultado.simuladas
    print(f"RESULTADOS DE TODA LA SIMULACIÓN ({resultado.escenario.tiempo:,.0f} minutos)")
    print(f"  {'Métrica':<8}{'Teórico':>12}{'Simulado':>12}{'Error':>10}")
    imprimir_fila("ρ", t.rho, s.rho)
    imprimir_fila("L", t.L, s.L)
    imprimir_fila("Lq", t.Lq, s.Lq)
    imprimir_fila("W", t.W, s.W)
    imprimir_fila("Wq", t.Wq, s.Wq)


def imprimir_fila(nombre, teorico, simulado):
    error = error_relativo(teorico, simulado)
    print(f"  {nombre:<8}{teorico:>12.4f}{simulado:>12.4f}{error:>9.2f}%")


def mostrar_archivo(ruta):
    print(f"  Gráfica guardada en {ruta}\n")


def mostrar_comparacion(resultados):
    print("=" * 78)
    print("COMPARACIÓN DE ESCENARIOS")
    print(f"  {'#':<3}{'λ':>5}{'μ':>5}{'ρ':>8}{'Wq teo':>10}{'Wq sim':>10}{'Lq teo':>10}{'Lq sim':>10}")
    for resultado in resultados:
        e = resultado.escenario
        inicio = f"  {e.numero:<3}{e.lam:>5}{e.mu:>5}{e.utilizacion():>8.3f}"
        if resultado.fue_simulado():
            t = resultado.teoricas
            s = resultado.simuladas
            print(inicio + f"{t.Wq:>10.4f}{s.Wq:>10.4f}{t.Lq:>10.4f}{s.Lq:>10.4f}")
        else:
            print(inicio + "   " + resultado.mensaje)
    print("=" * 78)
