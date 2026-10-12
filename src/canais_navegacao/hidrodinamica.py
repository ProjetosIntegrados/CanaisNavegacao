import math


GRAVIDADE = 9.81


def numero_froude_profundidade(velocidade: float, profundidade: float) -> float:
    """Calcula o número de Froude de profundidade."""
    return velocidade / math.sqrt(GRAVIDADE * profundidade)


def relacao_profundidade_calado(profundidade: float, calado: float) -> float:
    """Calcula a relação entre a profundidade da água e o calado da embarcação."""
    return profundidade / calado


def area_secao_canal(largura: float, profundidade: float) -> float:
    """Calcula a área da seção transversal de um canal retangular."""
    return largura * profundidade

def fator_bloqueio(area_navio: float, area_canal: float) -> float:
    """Calcula o fator de bloqueio entre a embarcação e o canal."""
    return area_navio / area_canal


def squat_barrass3(
    velocidade_nos: float,
    cb: float,
    bloqueio: float,
) -> float:
    """Calcula o squat máximo pelo método Barrass3."""
    k = 5.74 * bloqueio**0.76
    return cb * velocidade_nos**2 * k / 100


def verificar_validade_barrass3(
    relacao_ht: float,
    bloqueio: float,
    cb: float,
) -> bool:
    """Verifica se os parâmetros estão nos limites de validade do método Barrass3."""
    return (
        1.1 <= relacao_ht <= 1.4
        and 0.10 <= bloqueio <= 0.25
        and 0.50 <= cb <= 0.85
    )