import math


GRAVIDADE = 9.81


def numero_froude_profundidade(velocidade: float, profundidade: float) -> float:
    """Calcula o número de Froude de profundidade."""
    return velocidade / math.sqrt(GRAVIDADE * profundidade)


def relacao_profundidade_calado(profundidade: float, calado: float) -> float:
    """Calcula a relação entre a profundidade da água e o calado da embarcação."""
    return profundidade / calado