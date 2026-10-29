from canais_navegacao.batimetria import (
    SecaoBatimetrica,
    analisar_secao_horizontal,
    analisar_secao_vertical,
)


def diagnosticar_secao(
    secao: SecaoBatimetrica,
    largura_requerida: float,
    profundidade_requerida: float,
) -> tuple:
    """Integra as análises vertical e horizontal de uma seção."""
    resultado_vertical = analisar_secao_vertical(
        secao=secao,
        largura=largura_requerida,
        profundidade_requerida=profundidade_requerida,
    )

    resultado_horizontal = analisar_secao_horizontal(
        secao=secao,
        profundidade_requerida=profundidade_requerida,
        largura_requerida=largura_requerida,
    )

    atende_vertical = not resultado_vertical[5]
    atende_horizontal = resultado_horizontal[5]
    atende_geral = atende_vertical and atende_horizontal

    return (
        secao.identificacao,
        secao.distancia,
        resultado_vertical[2],
        profundidade_requerida,
        resultado_vertical[4],
        atende_vertical,
        resultado_horizontal[2],
        largura_requerida,
        resultado_horizontal[4],
        atende_horizontal,
        atende_geral,
    )


def diagnosticar_canal(
    secoes: list[SecaoBatimetrica],
    largura_requerida: float,
    profundidade_requerida: float,
) -> list[tuple]:
    """Executa o diagnóstico integrado das seções do canal."""
    resultados = []

    for secao in secoes:
        resultado = diagnosticar_secao(
            secao=secao,
            largura_requerida=largura_requerida,
            profundidade_requerida=profundidade_requerida,
        )

        resultados.append(resultado)

    return resultados
