import matplotlib.pyplot as plt

from canais_navegacao.batimetria import (
    SecaoBatimetrica,
    calcular_area_dragagem_secao,
    calcular_profundidade_disponivel,
    calcular_volume_total_dragagem,
    calcular_volumes_dragagem_por_trecho,
    inserir_pontos_mudanca,
    pontos_mudanca_secao_projeto,
    preparar_secoes_para_calculo_volume,
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


def plotar_perfil_longitudinal(
    secoes: list[SecaoBatimetrica],
    largura: float,
    profundidade_requerida: float,
) -> None:
    """Plota o perfil longitudinal de profundidade do canal."""
    distancias = []
    profundidades_disponiveis = []

    for secao in secoes:
        profundidade_disponivel = calcular_profundidade_disponivel(
            secao=secao,
            largura=largura,
        )

        distancias.append(secao.distancia)
        profundidades_disponiveis.append(profundidade_disponivel)

    profundidades_requeridas = [
        profundidade_requerida
        for _ in secoes
    ]

    plt.plot(
        distancias,
        profundidades_disponiveis,
        marker="o",
        label="Profundidade disponível",
    )

    plt.plot(
        distancias,
        profundidades_requeridas,
        label="Profundidade requerida",
    )

    plt.fill_between(
        distancias,
        profundidades_disponiveis,
        profundidades_requeridas,
        where=[
            disponivel < profundidade_requerida
            for disponivel in profundidades_disponiveis
        ],
        interpolate=True,
        alpha=0.3,
        label="Deficiência de profundidade",
    )

    plt.xlabel("Distância ao longo do canal (m)")
    
    plt.xticks(
    distancias,
    [
        f"{secao.identificacao}\n{secao.distancia:.0f} m"
        for secao in secoes
    ],
)
    
    plt.ylabel("Profundidade (m)")
    plt.title("Perfil longitudinal do canal")
    plt.legend()
    plt.grid()

    plt.gca().invert_yaxis()

    plt.show()


def plotar_volumes_dragagem(
    resultados_secoes: list[
        tuple[str, float, float, float, float, bool, float]
    ],
) -> None:
    """Plota os volumes de dragagem por trecho e acumulado."""
    secoes_volume = preparar_secoes_para_calculo_volume(
        resultados=resultados_secoes,
    )

    volumes_trechos = calcular_volumes_dragagem_por_trecho(
        secoes=secoes_volume,
    )

    volume_total = calcular_volume_total_dragagem(
        secoes=secoes_volume,
    )

    volumes = []
    volumes_acumulados = []
    rotulos = []
    acumulado = 0.0

    for indice, trecho in enumerate(volumes_trechos):
        volume = trecho[5]
        acumulado += volume

        volumes.append(volume)
        volumes_acumulados.append(acumulado)

        rotulos.append(
            f"{resultados_secoes[indice][0]} - "
            f"{resultados_secoes[indice + 1][0]}"
        )

    posicoes = range(len(volumes))

    plt.bar(
        posicoes,
        volumes,
        label="Volume por trecho",
    )

    plt.plot(
        posicoes,
        volumes_acumulados,
        marker="o",
        label="Volume acumulado",
    )

    plt.xticks(
        posicoes,
        rotulos,
        rotation=45,
        ha="right",
    )

    plt.xlabel("Trecho do canal")
    plt.ylabel("Volume de dragagem (m³)")
    plt.title(
        "Volumes de dragagem do canal\n"
        f"Volume total: {volume_total:.2f} m³"
    )
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()
    