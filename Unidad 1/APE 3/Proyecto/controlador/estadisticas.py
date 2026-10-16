from modelo.metricas import Metricas


def promedio(lista):
    if len(lista) == 0:
        return 0
    return sum(lista) / len(lista)


def promedio_en_el_tiempo(tiempos, valores, inicio, fin):
    area = 0
    for i in range(len(tiempos)):
        desde = tiempos[i]
        if i + 1 < len(tiempos):
            hasta = tiempos[i + 1]
        else:
            hasta = fin

        if desde < inicio:
            desde = inicio
        if hasta > fin:
            hasta = fin

        if hasta > desde:
            area = area + (hasta - desde) * valores[i]

    return area / (fin - inicio)


def calcular_simuladas(clientes, estados, calentamiento, fin):
    esperas = []
    tiempos_en_sistema = []
    for cliente in clientes:
        if cliente.llegada < calentamiento:
            continue
        if cliente.inicio_servicio is not None:
            esperas.append(cliente.tiempo_espera())
        if cliente.salida is not None:
            tiempos_en_sistema.append(cliente.tiempo_en_sistema())

    tiempos = []
    en_cola = []
    en_sistema = []
    servidor_ocupado = []
    for estado in estados:
        tiempos.append(estado.tiempo)
        en_cola.append(estado.en_cola)
        en_sistema.append(estado.en_sistema)
        if estado.en_sistema > 0:
            servidor_ocupado.append(1)
        else:
            servidor_ocupado.append(0)

    rho = promedio_en_el_tiempo(tiempos, servidor_ocupado, calentamiento, fin)
    L = promedio_en_el_tiempo(tiempos, en_sistema, calentamiento, fin)
    Lq = promedio_en_el_tiempo(tiempos, en_cola, calentamiento, fin)
    W = promedio(tiempos_en_sistema)
    Wq = promedio(esperas)

    return Metricas(rho, L, Lq, W, Wq)


def error_relativo(teorico, simulado):
    if teorico == 0:
        return 0
    return abs(simulado - teorico) / teorico * 100
