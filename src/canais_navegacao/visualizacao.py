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


def calcular_direcao_secao(
    secoes: list[SecaoBatimetrica],
    indice: int,
) -> tuple[float, float]:
    """Calcula a direção local do eixo do canal em uma seção."""
    if len(secoes) < 2:
        raise ValueError("Sao necessarias pelo menos duas secoes.")

    if indice == 0:
        dx = secoes[1].x - secoes[0].x
        dy = secoes[1].y - secoes[0].y
    elif indice == len(secoes) - 1:
        dx = secoes[-1].x - secoes[-2].x
        dy = secoes[-1].y - secoes[-2].y
    else:
        dx = secoes[indice + 1].x - secoes[indice - 1].x
        dy = secoes[indice + 1].y - secoes[indice - 1].y

    comprimento = (dx ** 2 + dy ** 2) ** 0.5

    if comprimento == 0:
        raise ValueError("Nao foi possivel determinar a direcao do canal.")

    return (
        dx / comprimento,
        dy / comprimento,
    )


def plotar_planta_canal(
    secoes: list[SecaoBatimetrica],
    largura_requerida: float,
    diagnostico: list[tuple],
) -> None:
    """Plota o eixo, os limites e o diagnóstico do canal em planta."""
    for secao in secoes:
        if secao.x is None or secao.y is None:
            raise ValueError(
                "Todas as secoes devem possuir coordenadas X/Y."
            )

    if len(diagnostico) != len(secoes):
        raise ValueError(
            "O diagnostico deve possuir um resultado para cada secao."
        )

    coordenadas_x = [secao.x for secao in secoes]
    coordenadas_y = [secao.y for secao in secoes]

    limite_esquerdo_x = []
    limite_esquerdo_y = []
    limite_direito_x = []
    limite_direito_y = []

    meia_largura = largura_requerida / 2

    for indice, secao in enumerate(secoes):
        direcao_x, direcao_y = calcular_direcao_secao(
            secoes=secoes,
            indice=indice,
        )

        perpendicular_x = -direcao_y
        perpendicular_y = direcao_x

        esquerdo_x = secao.x + perpendicular_x * meia_largura
        esquerdo_y = secao.y + perpendicular_y * meia_largura

        direito_x = secao.x - perpendicular_x * meia_largura
        direito_y = secao.y - perpendicular_y * meia_largura

        limite_esquerdo_x.append(esquerdo_x)
        limite_esquerdo_y.append(esquerdo_y)
        limite_direito_x.append(direito_x)
        limite_direito_y.append(direito_y)

        plt.plot(
            [esquerdo_x, direito_x],
            [esquerdo_y, direito_y],
            linestyle="--",
        )

        atende = diagnostico[indice][10]
        situacao = "ATENDE" if atende else "NAO ATENDE"
        marcador = "o" if atende else "x"

        plt.scatter(
            secao.x,
            secao.y,
            marker=marcador,
        )

        plt.text(
            secao.x,
            secao.y,
            f" {secao.identificacao}\n {situacao}",
        )

    plt.plot(
        coordenadas_x,
        coordenadas_y,
        label="Eixo do canal",
    )

    plt.plot(
        limite_esquerdo_x,
        limite_esquerdo_y,
        label="Limite esquerdo",
    )

    plt.plot(
        limite_direito_x,
        limite_direito_y,
        label="Limite direito",
    )

    plt.xlabel("X (m)")
    plt.ylabel("Y (m)")
    plt.title("Planta do canal")
    plt.legend()
    plt.grid()
    plt.axis("equal")
    plt.tight_layout()
    plt.show()