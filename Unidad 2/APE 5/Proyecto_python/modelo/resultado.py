from dataclasses import dataclass


@dataclass
class Resultado:
    semilla: int
    valores: list[int]
    media: float
    varianza: float
    repetidos: int
    huella: str
