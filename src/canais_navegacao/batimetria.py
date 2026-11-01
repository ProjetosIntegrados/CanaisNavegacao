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
        x: float | None = None,
        y: float | None = None,
    ) -> None:
        self.identificacao = identificacao
        self.distancia = distancia
        self.pontos = pontos
        self.x = x
        self.y = y


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


def pontos_mudanca_secao_projeto(
    largura: float,
    profundidade: float,
    talude: float,
) -> list[float]:
    """Calcula os offsets dos pontos de mudança da seção de projeto."""
    metade_largura = largura / 2
    limite_talude = metade_largura + talude * profundidade

    return [
        -limite_talude,
        -metade_largura,
        metade_largura,
        limite_talude,
    ]


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


def inserir_pontos_mudanca(
    pontos: list[PontoBatimetrico],
    pontos_mudanca: list[float],
) -> list[PontoBatimetrico]:
    """Insere pontos de mudança da seção de projeto na batimetria."""
    novos_pontos = []

    for indice in range(len(pontos) - 1):
        ponto_inicial = pontos[indice]
        ponto_final = pontos[indice + 1]

        novos_pontos.append(ponto_inicial)

        for offset in pontos_mudanca:
            if ponto_inicial.offset < offset < ponto_final.offset:
                profundidade = interpolar_profundidade(
                    offset=offset,
                    offset_inicial=ponto_inicial.offset,
                    profundidade_inicial=ponto_inicial.profundidade,
                    offset_final=ponto_final.offset,
                    profundidade_final=ponto_final.profundidade,
                )

                novos_pontos.append(
                    PontoBatimetrico(
                        offset=offset,
                        profundidade=profundidade,
                    )
                )

    novos_pontos.append(pontos[-1])

    return novos_pontos


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

    pontos_mudanca = pontos_mudanca_secao_projeto(
        largura=largura,
        profundidade=profundidade,
        talude=talude,
    )

    pontos = inserir_pontos_mudanca(
        pontos=secao.pontos,
        pontos_mudanca=pontos_mudanca,
    )

    for indice in range(len(pontos) - 1):
        ponto_inicial = pontos[indice]
        ponto_final = pontos[indice + 1]

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


def calcular_volume_dragagem_entre_secoes(
    area_inicial: float,
    area_final: float,
    distancia: float,
) -> float:
    """Calcula o volume de dragagem entre duas seções consecutivas."""
    return (
        (area_inicial + area_final)
        / 2
        * distancia
    )

def calcular_volume_total_dragagem(
    secoes: list[tuple[float, float]],
) -> float:
    """Calcula o volume total de dragagem ao longo do canal."""
    volume_total = 0.0


    for indice in range(len(secoes) - 1):
        distancia_inicial, area_inicial = secoes[indice]
        distancia_final, area_final = secoes[indice + 1]

        distancia = distancia_final - distancia_inicial  

        volume = calcular_volume_dragagem_entre_secoes(
            area_inicial=area_inicial,
            area_final=area_final,
            distancia=distancia,
        )  
        
        volume_total += volume

    return volume_total


def calcular_volumes_dragagem_por_trecho(
    secoes: list[tuple[float, float]],
) -> list[tuple[float, float, float, float, float, float]]:
    """Calcula os volumes de dragagem por trecho do canal."""
    resultados = []

    for indice in range(len(secoes) - 1):
        distancia_inicial, area_inicial = secoes[indice]
        distancia_final, area_final = secoes[indice + 1]

        distancia = distancia_final - distancia_inicial

        volume = calcular_volume_dragagem_entre_secoes(
            area_inicial=area_inicial,
            area_final=area_final,
            distancia=distancia,
        )

        resultados.append(
            (
                distancia_inicial,
                distancia_final,
                area_inicial,
                area_final,
                distancia,
                volume,
            )
        )

    return resultados    


def identificar_trechos_dragagem(
    resultados: list[tuple[float, float, float, float, float, float]],
) -> list[tuple[float, float, bool]]:
    """Identifica os trechos que necessitam de dragagem."""
    trechos = []

    for resultado in resultados:
        distancia_inicial = resultado[0]
        distancia_final = resultado[1]
        volume = resultado[5]

        necessita_dragagem = volume > 0

        trechos.append(
            (
                distancia_inicial,
                distancia_final,
                necessita_dragagem,
            )
        )
    return trechos


def calcular_deficit_profundidade(
    profundidade_disponivel: float,
    profundidade_requerida: float,
) -> float:
    """Calcula o déficit de profundidade da seção."""
    return max(
        0.0,
        profundidade_requerida - profundidade_disponivel,
    )


def ponto_dentro_largura_navegavel(
    offset: float,
    largura: float,
) -> bool:
    """Verifica se um ponto está dentro da largura navegável."""
    metade_largura = largura / 2

    return -metade_largura <= offset <= metade_largura


def calcular_profundidade_disponivel(
    secao: SecaoBatimetrica,
    largura: float,
) -> float:
    """Calcula a menor profundidade dentro da largura navegável."""
    metade_largura = largura / 2

    pontos = inserir_pontos_mudanca(
        pontos=secao.pontos,
        pontos_mudanca=[
            -metade_largura,
            metade_largura,
        ],
    )

    profundidades = []

    for ponto in pontos:
        if ponto_dentro_largura_navegavel(
            offset=ponto.offset,
            largura=largura,
        ):
            profundidades.append(ponto.profundidade)

    return min(profundidades)


def analisar_secao_vertical(
    secao: SecaoBatimetrica,
    largura: float,
    profundidade_requerida: float,
) -> tuple[str, float, float, float, float, bool]:
    """Analisa a condição vertical de uma seção batimétrica."""
    profundidade_disponivel = calcular_profundidade_disponivel(
        secao=secao,
        largura=largura,
    )

    deficit = calcular_deficit_profundidade(
        profundidade_disponivel=profundidade_disponivel,
        profundidade_requerida=profundidade_requerida,
    )

    necessita_dragagem = deficit > 0

    return (
        secao.identificacao,
        secao.distancia,
        profundidade_disponivel,
        profundidade_requerida,
        deficit,
        necessita_dragagem,
    )


def analisar_secoes_verticais(
    secoes: list[SecaoBatimetrica],
    largura: float,
    profundidade_requerida: float,
) -> list[tuple[str, float, float, float, float, bool]]:
    """Analisa a condição vertical das seções ao longo do canal."""
    resultados = []

    for secao in secoes:
        resultado = analisar_secao_vertical(
            secao=secao,
            largura=largura,
            profundidade_requerida=profundidade_requerida,
        )

        resultados.append(resultado)

    return resultados


def identificar_secao_critica(
    resultados: list[tuple[str, float, float, float, float, bool]],
) -> tuple[str, float, float, float, float, bool]:
    """Identifica a seção com o maior déficit de profundidade."""
    return max(
        resultados,
        key=lambda resultado: resultado[4],
    )


def analisar_secao_vertical_completa(
    secao: SecaoBatimetrica,
    largura: float,
    profundidade_requerida: float,
    talude: float,
) -> tuple[str, float, float, float, float, bool, float]:
    """Analisa a condição vertical e a área de dragagem da seção."""
    resultado = analisar_secao_vertical(
        secao=secao,
        largura=largura,
        profundidade_requerida=profundidade_requerida,
    )

    area_dragagem = calcular_area_dragagem_secao(
        secao=secao,
        largura=largura,
        profundidade=profundidade_requerida,
        talude=talude,
    )

    return (
        resultado[0],
        resultado[1],
        resultado[2],
        resultado[3],
        resultado[4],
        resultado[5],
        area_dragagem,
    )


def analisar_secoes_verticais_completas(
    secoes: list[SecaoBatimetrica],
    largura: float,
    profundidade_requerida: float,
    talude: float,
) -> list[tuple[str, float, float, float, float, bool, float]]:
    """Analisa a condição vertical e a área de dragagem das seções."""
    resultados = []

    for secao in secoes:
        resultado = analisar_secao_vertical_completa(
            secao=secao,
            largura=largura,
            profundidade_requerida=profundidade_requerida,
            talude=talude,
        )

        resultados.append(resultado)

    return resultados


def preparar_secoes_para_calculo_volume(
    resultados: list[
        tuple[str, float, float, float, float, bool, float]
    ],
) -> list[tuple[float, float]]:
    """Prepara distância e área das seções para o cálculo de volume."""
    secoes_volume = []

    for resultado in resultados:
        distancia = resultado[1]
        area_dragagem = resultado[6]

        secoes_volume.append(
            (
                distancia,
                area_dragagem,
            )
        )

    return secoes_volume


def analisar_canal_vertical(
    secoes: list[SecaoBatimetrica],
    largura: float,
    profundidade_requerida: float,
    talude: float,
) -> tuple:
    """Executa a análise vertical completa do canal."""
    resultados_secoes = analisar_secoes_verticais_completas(
        secoes=secoes,
        largura=largura,
        profundidade_requerida=profundidade_requerida,
        talude=talude,
    )

    secoes_volume = preparar_secoes_para_calculo_volume(
        resultados=resultados_secoes,
    )

    volumes_trechos = calcular_volumes_dragagem_por_trecho(
        secoes=secoes_volume,
    )

    trechos_dragagem = identificar_trechos_dragagem(
        resultados=volumes_trechos,
    )

    volume_total = calcular_volume_total_dragagem(
        secoes=secoes_volume,
    )

    secao_critica = identificar_secao_critica(
        resultados=[
            resultado[:6]
            for resultado in resultados_secoes
        ],
    )

    return (
        resultados_secoes,
        volumes_trechos,
        trechos_dragagem,
        secao_critica,
        volume_total,
    )


def encontrar_offset_profundidade(
    offset_inicial: float,
    profundidade_inicial: float,
    offset_final: float,
    profundidade_final: float,
    profundidade_requerida: float,
) -> float:
    """Calcula o offset onde o perfil atinge a profundidade requerida."""
    return offset_inicial + (
        (profundidade_requerida - profundidade_inicial)
        / (profundidade_final - profundidade_inicial)
        * (offset_final - offset_inicial)
    )


def encontrar_limite_esquerdo_navegavel(
    secao: SecaoBatimetrica,
    profundidade_requerida: float,
) -> float:
    """Encontra o limite esquerdo da faixa navegável que contém o eixo."""
    pontos = secao.pontos

    for indice in range(len(pontos) - 2, -1, -1):
        ponto_inicial = pontos[indice]
        ponto_final = pontos[indice + 1]

        if ponto_final.offset > 0:
            continue

        if (
            ponto_inicial.profundidade < profundidade_requerida
            <= ponto_final.profundidade
        ):
            return encontrar_offset_profundidade(
                offset_inicial=ponto_inicial.offset,
                profundidade_inicial=ponto_inicial.profundidade,
                offset_final=ponto_final.offset,
                profundidade_final=ponto_final.profundidade,
                profundidade_requerida=profundidade_requerida,
            )

    raise ValueError(
        "Nao foi encontrado limite esquerdo para a faixa navegavel."
    )


def encontrar_limite_direito_navegavel(
    secao: SecaoBatimetrica,
    profundidade_requerida: float,
) -> float:
    """Encontra o limite direito da faixa navegável que contém o eixo."""
    pontos = secao.pontos

    for indice in range(len(pontos) - 1):
        ponto_inicial = pontos[indice]
        ponto_final = pontos[indice + 1]

        if ponto_inicial.offset < 0:
            continue

        if (
            ponto_inicial.profundidade >= profundidade_requerida
            > ponto_final.profundidade
        ):
            return encontrar_offset_profundidade(
                offset_inicial=ponto_inicial.offset,
                profundidade_inicial=ponto_inicial.profundidade,
                offset_final=ponto_final.offset,
                profundidade_final=ponto_final.profundidade,
                profundidade_requerida=profundidade_requerida,
            )

    raise ValueError(
        "Nao foi encontrado limite direito para a faixa navegavel."
    )


def calcular_largura_disponivel(
    secao: SecaoBatimetrica,
    profundidade_requerida: float,
) -> float:
    """Calcula a largura disponível da faixa navegável que contém o eixo."""
    pontos = secao.pontos

    for indice in range(len(pontos) - 1):
        ponto_inicial = pontos[indice]
        ponto_final = pontos[indice + 1]

        if ponto_inicial.offset == 0.0:
            profundidade_eixo = ponto_inicial.profundidade
            break

        if ponto_inicial.offset < 0.0 < ponto_final.offset:
            profundidade_eixo = interpolar_profundidade(
                offset=0.0,
                offset_inicial=ponto_inicial.offset,
                profundidade_inicial=ponto_inicial.profundidade,
                offset_final=ponto_final.offset,
                profundidade_final=ponto_final.profundidade,
            )
            break
    else:
        if pontos[-1].offset == 0.0:
            profundidade_eixo = pontos[-1].profundidade
        else:
            raise ValueError(
                "O eixo do canal nao esta contido na secao batimetrica."
            )

    if profundidade_eixo < profundidade_requerida:
        raise ValueError(
            "O eixo do canal nao possui profundidade suficiente."
        )

    limite_esquerdo = encontrar_limite_esquerdo_navegavel(
        secao=secao,
        profundidade_requerida=profundidade_requerida,
    )

    limite_direito = encontrar_limite_direito_navegavel(
        secao=secao,
        profundidade_requerida=profundidade_requerida,
    )

    return limite_direito - limite_esquerdo


def calcular_deficit_largura(
    largura_disponivel: float,
    largura_requerida: float,
) -> float:
    """Calcula o déficit de largura da seção."""
    return max(
        0.0,
        largura_requerida - largura_disponivel,
    )


def analisar_secao_horizontal(
    secao: SecaoBatimetrica,
    profundidade_requerida: float,
    largura_requerida: float,
) -> tuple[str, float, float, float, float, bool]:
    """Analisa a condição horizontal de uma seção batimétrica."""
    try:
        largura_disponivel = calcular_largura_disponivel(
            secao=secao,
            profundidade_requerida=profundidade_requerida,
        )
    except ValueError as erro:
        if str(erro) != "O eixo do canal nao possui profundidade suficiente.":
            raise

        largura_disponivel = 0.0

    deficit = calcular_deficit_largura(
        largura_disponivel=largura_disponivel,
        largura_requerida=largura_requerida,
    )

    atende = deficit == 0

    return (
        secao.identificacao,
        secao.distancia,
        largura_disponivel,
        largura_requerida,
        deficit,
        atende,
    )

    return (
        secao.identificacao,
        secao.distancia,
        largura_disponivel,
        largura_requerida,
        deficit,
        atende,
    )


def analisar_secoes_horizontais(
    secoes: list[SecaoBatimetrica],
    profundidade_requerida: float,
    largura_requerida: float,
) -> list[tuple[str, float, float, float, float, bool]]:
    """Analisa a condição horizontal das seções ao longo do canal."""
    resultados = []

    for secao in secoes:
        resultado = analisar_secao_horizontal(
            secao=secao,
            profundidade_requerida=profundidade_requerida,
            largura_requerida=largura_requerida,
        )

        resultados.append(resultado)

    return resultados


def identificar_secao_critica_horizontal(
    resultados: list[tuple[str, float, float, float, float, bool]],
) -> tuple[str, float, float, float, float, bool]:
    """Identifica a seção com o maior déficit de largura."""
    return max(
        resultados,
        key=lambda resultado: resultado[4],
    )
