from modelo.generador import A, C, M


def mostrar(resultados, completo):
    a, b = resultados
    print("GENERADOR CONGRUENCIAL LINEAL - PYTHON")
    print(f"a={A}; c={C}; m={M}; U(n)=X(n)/m. La tabla comienza en X1.")
    print(f"Semillas: {a.semilla} y {b.semilla}")
    print(f"{'n':>4} {'X primera semilla':>20} {'U':>16} {'X segunda semilla':>20} {'U':>16}")
    for i, (x, y) in enumerate(zip(a.valores[:20], b.valores[:20]), 1):
        print(f"{i:4d} {x:20d} {x/M:16.12f} {y:20d} {y/M:16.12f}")
    for r in resultados:
        print(f"\nSemilla: {r.semilla}; observaciones: {len(r.valores)}")
        print(f"Media: {r.media:.12f}; varianza poblacional: {r.varianza:.12f}")
        print(f"Mínimo U: {min(r.valores)/M:.12f}; máximo U: {max(r.valores)/M:.12f}")
        print(f"Repetidos en la muestra: {r.repetidos}\nSHA-256: {r.huella}")
    iguales = sum(x == y for x, y in zip(a.valores, b.valores))
    print(f"\nCoincidencias en la misma posición entre semillas: {iguales}")
    print("Referencia uniforme [0,1): media 0.5; varianza 1/12 = 0.083333333333.")
    if completo:
        print(f"Período teórico: {M} (Hull-Dobell: c impar y a-1 múltiplo de 4).")
    print("Una muestra sin repeticiones no demuestra el período ni la independencia.")
    print("Compara los enteros y SHA-256 con Java usando las mismas semillas y cantidad.")
