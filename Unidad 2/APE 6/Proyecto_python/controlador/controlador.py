from modelo.generador import generar
from modelo.pruebas import evaluar


def ejecutar(config):
    valores = generar(config)
    resultado = evaluar(valores, config.m)
    return valores, resultado
