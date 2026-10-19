class PontoBatimetrico:
    """Representa um ponto de uma seção batimétrica."""

    def __init__(
        self,
        offset: float,
        profundidade: float,
    ) -> None:
        self.offset = offset
        self.profundidade = profundidade


class SecaoBatimetrica:
    """Representa uma seção transversal com seus pontos batimétricos."""

    def __init__(
        self,
        identificacao: str,
        distancia: float,
        pontos: list[PontoBatimetrico],
    ) -> None:
        self.identificacao = identificacao
        self.distancia = distancia
        self.pontos = pontos


def profundidade_secao_projeto(
    offset: float,
    largura: float,
    profundidade: float,
    talude: float,
) -> float:
    """Calcula a profundidade da seção de projeto em um determinado offset."""
    distancia_eixo = abs(offset)
    metade_largura = largura / 2

    if distancia_eixo <= metade_largura:
        return profundidade

    distancia_talude = distancia_eixo - metade_largura
    profundidade_talude = profundidade - distancia_talude / talude

    return max(0.0, profundidade_talude)


def interpolar_profundidade(
    offset: float,
    offset_inicial: float,
    profundidade_inicial: float,
    offset_final: float,
    profundidade_final: float,
) -> float:
    """Interpola linearmente a profundidade entre dois pontos batimétricos."""
    return profundidade_inicial + (
        (profundidade_final - profundidade_inicial)
        / (offset_final - offset_inicial)
        * (offset - offset_inicial)
    )


def encontrar_intersecao(
    offset_inicial: float,
    diferenca_inicial: float,
    offset_final: float,
    diferenca_final: float,
) -> float:
    """Calcula o offset de interseção entre os perfis."""
    return offset_inicial + (
        diferenca_inicial
        / (diferenca_inicial - diferenca_final)
        * (offset_final - offset_inicial)
    )

def area_dragagem_intervalo(
    offset_inicial: float,
    diferenca_inicial: float,
    offset_final: float,
    diferenca_final: float,
) -> float:
    """Calcula a área de dragagem entre dois offsets consecutivos."""
    largura_intervalo = offset_final - offset_inicial

    if diferenca_inicial <= 0 and diferenca_final <= 0:
        return 0.0

    if diferenca_inicial >= 0 and diferenca_final >= 0:
        return (
            (diferenca_inicial + diferenca_final)
            / 2
            * largura_intervalo
        )

    offset_intersecao = encontrar_intersecao(
        offset_inicial,
        diferenca_inicial,
        offset_final,
        diferenca_final,
    )

    if diferenca_inicial > 0:
        return (
            diferenca_inicial
            * (offset_intersecao - offset_inicial)
            / 2
        )

    return (
        diferenca_final
        * (offset_final - offset_intersecao)
        / 2
    )


def calcular_area_dragagem_secao(
    secao: SecaoBatimetrica,
    largura: float,
    profundidade: float,
    talude: float,
) -> float:
    """Calcula a área de dragagem de uma seção batimétrica."""
    area_total = 0.0

    for indice in range(len(secao.pontos) - 1):
        ponto_inicial = secao.pontos[indice]
        ponto_final = secao.pontos[indice + 1]

        projeto_inicial = profundidade_secao_projeto(
            ponto_inicial.offset,
            largura,
            profundidade,
            talude,
        )

        projeto_final = profundidade_secao_projeto(
            ponto_final.offset,
            largura,
            profundidade,
            talude,
        )

        diferenca_inicial = (
            projeto_inicial - ponto_inicial.profundidade
        )
        diferenca_final = (
            projeto_final - ponto_final.profundidade
        )

        area_total += area_dragagem_intervalo(
            ponto_inicial.offset,
            diferenca_inicial,
            ponto_final.offset,
            diferenca_final,
        )

    return area_total
