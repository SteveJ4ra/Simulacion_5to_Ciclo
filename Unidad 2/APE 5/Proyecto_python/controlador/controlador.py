import hashlib
from modelo.generador import A, C, M, GeneradorLCG
from modelo.resultado import Resultado


def analizar(semilla, cantidad):
    valores = GeneradorLCG(semilla).generar(cantidad)
    media = acumulado = 0.0
    huella = hashlib.sha256()
    # Welford: varianza poblacional de los valores normalizados.
    for n, x in enumerate(valores, 1):
        u = x / M
        delta = u - media
        media += delta / n
        acumulado += delta * (u - media)
        # Igual que Java: enteros ASCII separados por LF.
        huella.update(f"{x}\n".encode("ascii"))
    return Resultado(semilla, valores, media, acumulado/cantidad,
                     cantidad-len(set(valores)), huella.hexdigest())


def periodo_completo():
    # Hull-Dobell para m=2^32: su único factor primo es 2.
    return C % 2 == 1 and (A-1) % 2 == 0 and (A-1) % 4 == 0


def ejecutar(semilla, otra_semilla, cantidad, carpeta=None):
    from vista.consola import mostrar
    from vista.exportacion import exportar
    resultados = [analizar(s, cantidad) for s in (semilla, otra_semilla)]
    mostrar(resultados, periodo_completo())
    if carpeta is not None:
        exportar(resultados, carpeta)
