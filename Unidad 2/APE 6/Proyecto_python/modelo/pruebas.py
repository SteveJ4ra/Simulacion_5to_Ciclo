import math

import numpy as np
from scipy.stats import chi2, kstwobign

INTERVALOS = 10
ALFA = 0.05


def validar_muestra(valores, modulo):
    if type(modulo) is not int or not 2 <= modulo <= 2**32:
        raise ValueError("El módulo debe estar entre 2 y 2^32.")
    if not 50 <= len(valores) <= 1_000_000:
        raise ValueError("Se necesitan entre 50 y 1 000 000 datos.")
    for valor in valores:
        if not isinstance(valor, (int, np.integer)) or isinstance(valor, bool):
            raise ValueError("La muestra debe contener enteros.")
        if valor < 0 or valor >= modulo:
            raise ValueError("Cada valor debe estar entre 0 y m - 1.")


def calcular_chi(valores, modulo):
    observadas = [0] * INTERVALOS
    for valor in valores:
        indice = valor * INTERVALOS // modulo
        observadas[indice] += 1
    esperada = len(valores) / INTERVALOS
    estadistico = 0.0
    for observada in observadas:
        estadistico += (observada - esperada) ** 2 / esperada
    valor_p = float(chi2.sf(estadistico, INTERVALOS - 1))
    return observadas, esperada, estadistico, valor_p


def calcular_ks(valores, modulo):
    ordenados = np.sort(np.asarray(valores, dtype=np.int64))
    cantidad = len(ordenados)
    d_mas = 0.0
    d_menos = 0.0
    for posicion, entero in enumerate(ordenados, 1):
        uniforme = entero / modulo
        diferencia_mas = posicion / cantidad - uniforme
        diferencia_menos = uniforme - (posicion - 1) / cantidad
        d_mas = max(d_mas, diferencia_mas)
        d_menos = max(d_menos, diferencia_menos)
    estadistico = max(d_mas, d_menos)
    valor_p = float(kstwobign.sf(math.sqrt(cantidad) * estadistico))
    return d_mas, d_menos, estadistico, valor_p


def evaluar(valores, modulo):
    validar_muestra(valores, modulo)
    observadas, esperada, chi, p_chi = calcular_chi(valores, modulo)
    d_mas, d_menos, d, p_ks = calcular_ks(valores, modulo)
    return {
        "frecuencias": observadas,
        "esperada": esperada,
        "chi": chi,
        "p_chi": p_chi,
        "d_mas": d_mas,
        "d_menos": d_menos,
        "d": d,
        "p_ks": p_ks,
    }


def decidir(valor_p):
    if valor_p >= ALFA:
        return "No se rechaza H0"
    return "Se rechaza H0"
