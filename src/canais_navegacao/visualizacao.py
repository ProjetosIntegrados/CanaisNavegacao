import matplotlib.pyplot as plt

from canais_navegacao.batimetria import (
    SecaoBatimetrica,
    calcular_area_dragagem_secao,
    inserir_pontos_mudanca,
    pontos_mudanca_secao_projeto,
    profundidade_secao_projeto,
)


def plotar_secao_transversal(
    secao: SecaoBatimetrica,
    largura: float,
    profundidade: float,
    talude: float,
) -> None:
    """Plota a batimetria, a seção de projeto e a área de dragagem."""
    pontos_mudanca = pontos_mudanca_secao_projeto(
        largura=largura,
        profundidade=profundidade,
        talude=talude,
    )

    pontos = inserir_pontos_mudanca(
        pontos=secao.pontos,
        pontos_mudanca=pontos_mudanca,
    )

    offsets = [ponto.offset for ponto in pontos]
    profundidades = [ponto.profundidade for ponto in pontos]

    profundidades_projeto = [
        profundidade_secao_projeto(
            offset=offset,
            largura=largura,
            profundidade=profundidade,
            talude=talude,
        )
        for offset in offsets
    ]

    area_dragagem = calcular_area_dragagem_secao(
        secao=secao,
        largura=largura,
        profundidade=profundidade,
        talude=talude,
    )

    plt.plot(
        offsets,
        profundidades,
        label="Batimetria existente",
    )

    plt.plot(
        offsets,
        profundidades_projeto,
        label="Seção de projeto",
    )

    plt.fill_between(
        offsets,
        profundidades,
        profundidades_projeto,
        where=[
            projeto > existente
            for existente, projeto in zip(
                profundidades,
                profundidades_projeto,
            )
        ],
        interpolate=True,
        alpha=0.3,
        label="Área de dragagem",
    )

    plt.xlabel("Offset (m)")
    plt.ylabel("Profundidade (m)")
    plt.title(
        f"Seção transversal - {secao.identificacao}\n"
        f"Área de dragagem: {area_dragagem:.2f} m²"
    )
    plt.legend()
    plt.grid()

    plt.gca().invert_yaxis()

    plt.show()
    
