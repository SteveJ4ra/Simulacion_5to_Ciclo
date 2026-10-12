import pandas as pd

from Modelo.modelo import ModeloLluvia


class ControladorSimulacion:
    def __init__(self) -> None:
        self.original = ModeloLluvia()
        self.ajustado = ModeloLluvia(0.45, 0.40, 0.15)

    def simular(self) -> dict[str, pd.DataFrame]:
        datos = pd.DataFrame(
            [
                ("06:00", 65, 40, 14),
                ("08:00", 70, 50, 16),
                ("10:00", 68, 45, 18),
                ("12:00", 60, 30, 22),
                ("14:00", 75, 70, 20),
                ("16:00", 85, 85, 18),
                ("18:00", 92, 95, 16),
                ("20:00", 88, 90, 17),
                ("22:00", 80, 75, 15),
            ],
            columns=["Hora", "Humedad", "Nubosidad", "Temperatura"],
        )
        return {
            "Original": self.original.evaluar(datos),
            "Ajustado": self.ajustado.evaluar(datos),
        }

    @staticmethod
    def comparar(resultados: dict[str, pd.DataFrame]) -> pd.DataFrame:
        original = resultados["Original"]
        ajustado = resultados["Ajustado"]
        return pd.DataFrame(
            {
                "Hora": original["Hora"],
                "Índice original": original["Índice"],
                "Índice ajustado": ajustado["Índice"],
                "Diferencia": ajustado["Índice"] - original["Índice"],
                "Estado original": original["Estado"],
                "Estado ajustado": ajustado["Estado"],
            }
        )
