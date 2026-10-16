import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

AZUL = "#2a78d6"
NARANJA = "#eb6834"


def guardar_escenario(resultado, config):
    e = resultado.escenario
    t = resultado.teoricas
    calentamiento = config["TIEMPO_CALENTAMIENTO"]
    fin_ventana = calentamiento + config["VENTANA_GRAFICA_COLA"]

    tiempos = []
    tamanos = []
    for estado in resultado.estados:
        if estado.tiempo >= calentamiento and estado.tiempo <= fin_ventana:
            tiempos.append(estado.tiempo)
            tamanos.append(estado.en_cola)

    esperas = []
    promedios = []
    suma = 0
    for cliente in resultado.clientes:
        if cliente.llegada >= calentamiento and cliente.inicio_servicio is not None:
            esperas.append(cliente.tiempo_espera())
            suma = suma + cliente.tiempo_espera()
            promedios.append(suma / len(esperas))

    figura, (eje1, eje2, eje3) = plt.subplots(1, 3, figsize=(17, 4.5))
    figura.suptitle(f"Escenario {e.numero}: λ = {e.lam}, μ = {e.mu}, ρ = {t.rho:.3f} ({e.condicion})")

    eje1.step(tiempos, tamanos, where="post", color=AZUL, label="Simulado")
    eje1.axhline(t.Lq, color=NARANJA, linestyle="--", label=f"Lq teórico = {t.Lq:.3f}")
    eje1.set_title("Tamaño de la cola en el tiempo")
    eje1.set_xlabel("Tiempo (minutos)")
    eje1.set_ylabel("Clientes en cola")
    eje1.legend()

    eje2.hist(esperas, bins=40, color=AZUL, edgecolor="white")
    eje2.axvline(t.Wq, color=NARANJA, linestyle="--", label=f"Wq teórico = {t.Wq:.3f}")
    eje2.set_title("Distribución de los tiempos de espera")
    eje2.set_xlabel("Tiempo de espera (minutos)")
    eje2.set_ylabel("Clientes")
    eje2.legend()

    eje3.plot(promedios, color=AZUL, label="Wq simulado (promedio acumulado)")
    eje3.axhline(t.Wq, color=NARANJA, linestyle="--", label="Wq teórico")
    eje3.set_title("Convergencia del tiempo de espera")
    eje3.set_xlabel("Clientes atendidos")
    eje3.set_ylabel("Espera promedio (minutos)")
    eje3.set_ylim(bottom=0)
    eje3.legend()

    return guardar(figura, config, f"escenario_{e.numero}.png")


def guardar_comparacion(resultados, config):
    nombres = []
    wq_teo, wq_sim, lq_teo, lq_sim = [], [], [], []
    for resultado in resultados:
        if not resultado.fue_simulado():
            continue
        nombres.append(f"Escenario {resultado.escenario.numero}")
        wq_teo.append(resultado.teoricas.Wq)
        wq_sim.append(resultado.simuladas.Wq)
        lq_teo.append(resultado.teoricas.Lq)
        lq_sim.append(resultado.simuladas.Lq)

    posiciones = []
    izquierda = []
    derecha = []
    for i in range(len(nombres)):
        posiciones.append(i)
        izquierda.append(i - 0.2)
        derecha.append(i + 0.2)

    figura, (eje1, eje2) = plt.subplots(1, 2, figsize=(12, 4.5))

    eje1.bar(izquierda, wq_teo, 0.4, color=NARANJA, label="Teórico")
    eje1.bar(derecha, wq_sim, 0.4, color=AZUL, label="Simulado")
    eje1.set_xticks(posiciones, nombres)
    eje1.set_title("Tiempo promedio de espera en la cola (Wq)")
    eje1.legend()

    eje2.bar(izquierda, lq_teo, 0.4, color=NARANJA, label="Teórico")
    eje2.bar(derecha, lq_sim, 0.4, color=AZUL, label="Simulado")
    eje2.set_xticks(posiciones, nombres)
    eje2.set_title("Clientes promedio en la cola (Lq)")
    eje2.legend()

    return guardar(figura, config, "comparacion.png")


def guardar(figura, config, nombre):
    carpeta = config["CARPETA_GRAFICAS"]
    os.makedirs(carpeta, exist_ok=True)
    ruta = os.path.join(carpeta, nombre)
    figura.savefig(ruta, dpi=100, bbox_inches="tight")
    plt.close(figura)
    return ruta
