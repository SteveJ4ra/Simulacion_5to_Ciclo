from modelo.metricas import Metricas


def calcular_teoricas(escenario):
    lam = escenario.lam
    mu = escenario.mu

    rho = lam / mu
    L = lam / (mu - lam)
    Lq = (lam ** 2) / (mu * (mu - lam))
    W = 1 / (mu - lam)
    Wq = lam / (mu * (mu - lam))

    return Metricas(rho, L, Lq, W, Wq)
