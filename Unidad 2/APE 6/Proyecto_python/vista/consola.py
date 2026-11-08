from modelo.pruebas import decidir


def mostrar(config, valores, resultado):
    print(f"n={config.cantidad}, semilla={config.semilla}, a={config.a}, c={config.c}, m={config.m}")
    print("Primeros 20 valores (la secuencia comienza en X1):")
    for posicion, valor in enumerate(valores[:20], 1):
        print(f"{posicion:4d} X={valor:12d} U={valor / config.m:.12f}")
    print(f"{'Intervalo':<15}{'Observada':>12}{'Esperada':>12}")
    for indice, frecuencia in enumerate(resultado["frecuencias"]):
        intervalo = f"[{indice / 10:.1f}, {(indice + 1) / 10:.1f})"
        print(f"{intervalo:<15}{frecuencia:12d}{resultado['esperada']:12.2f}")
    imprimir_prueba("Chi-cuadrado (gl=9)", resultado["chi"], resultado["p_chi"])
    imprimir_prueba("KS bilateral", resultado["d"], resultado["p_ks"])
    print(f"D+={resultado['d_mas']:.8f}, D-={resultado['d_menos']:.8f}")
    print("KS usa un valor p asintótico (aproximado), especialmente apropiado para la muestra de 10 000 datos.")
    print("Las pruebas contrastan uniformidad con una referencia continua; no prueban independencia ni aleatoriedad.")


def imprimir_prueba(nombre, estadistico, valor_p):
    decision = decidir(valor_p)
    print(f"{nombre}: estadístico={estadistico:.8f}, p={valor_p:.8g}, {decision} (alfa=0.05)")
