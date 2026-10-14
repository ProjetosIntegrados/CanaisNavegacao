import math

from canais_navegacao.embarcacao import Embarcacao
from canais_navegacao.canal import Canal


GRAVIDADE = 9.81


def numero_froude_profundidade(velocidade: float, profundidade: float) -> float:
    """Calcula o número de Froude de profundidade."""
    return velocidade / math.sqrt(GRAVIDADE * profundidade)


def relacao_boca_calado(boca: float, calado: float) -> float:
    """Calcula a relação entre a boca e o calado da embarcação."""
    return boca / calado


def relacao_comprimento_boca(lpp: float, boca: float) -> float:
    """Calcula a relação entre o comprimento e a boca da embarcação."""
    return lpp / boca


def relacao_comprimento_calado(lpp: float, calado: float) -> float:
    """Calcula a relação entre o comprimento e o calado da embarcação."""
    return lpp / calado


def relacao_profundidade_calado(profundidade: float, calado: float) -> float:
    """Calcula a relação entre a profundidade da água e o calado da embarcação."""
    return profundidade / calado


def area_secao_canal(
    largura: float,
    profundidade: float,
    talude: float = 0,
) -> float:
    """Calcula a área da seção transversal do canal."""
    return largura * profundidade + talude * profundidade**2


def largura_topo_canal(
    largura: float,
    profundidade: float,
    talude: float,
) -> float:
    """Calcula a largura no topo da seção transversal do canal."""
    return largura + 2 * talude * profundidade


def profundidade_media(
    area_canal: float,
    largura_topo: float,
) -> float:
    """Calcula a profundidade média da água no canal."""
    return area_canal / largura_topo


def coeficiente_velocidade_critica(bloqueio: float) -> float:
    """Calcula o coeficiente de velocidade crítica em canal restrito."""
    return (2 * math.sin(math.asin(1 - bloqueio) / 3))**1.5


def velocidade_critica(
    coeficiente_critico: float,
    profundidade_media: float,
) -> float:
    """Calcula a velocidade crítica em canal restrito."""
    return coeficiente_critico * math.sqrt(GRAVIDADE * profundidade_media)


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


def coeficiente_squat_icorels(cb: float) -> float:
    """Calcula o coeficiente Cs utilizado pelo método ICORELS."""
    if cb < 0.7:
        return 1.7
    if cb < 0.8:
        return 2.0
    return 2.4


def volume_deslocamento(
    lpp: float,
    boca: float,
    calado: float,
    cb: float,
) -> float:
    """Calcula o volume de deslocamento da embarcação."""
    return cb * lpp * boca * calado


def squat_icorels(
    coeficiente_s: float,
    volume_deslocamento: float,
    lpp: float,
    froude_profundidade: float,
) -> float:
    """Calcula o squat máximo pelo método ICORELS."""
    return (
        coeficiente_s
        * volume_deslocamento
        / lpp**2
        * froude_profundidade**2
        / math.sqrt(1 - froude_profundidade**2)
    )


def verificar_validade_icorels(
    relacao_ht: float,
    relacao_bt: float,
    relacao_lb: float,
    relacao_lt: float,
    cb: float,
    froude_profundidade: float,
) -> bool:
    """Verifica os limites básicos de aplicação do método ICORELS."""
    return (
        1.1 <= relacao_ht <= 2.0
        and 2.19 <= relacao_bt <= 3.5
        and 5.5 <= relacao_lb <= 8.5
        and 16.1 <= relacao_lt <= 20.2
        and 0.6 <= cb <= 0.8
        and froude_profundidade <= 0.7
    )


def velocidade_equivalente_yoshimura(
    velocidade: float,
    bloqueio: float,
    tipo_canal: str,
) -> float:
    """Calcula a velocidade equivalente utilizada pelo método de Yoshimura."""
    if tipo_canal == "U":
        return velocidade

    if tipo_canal in ("R", "C"):
        return velocidade / (1 - bloqueio)

    raise ValueError("Tipo de canal deve ser U, R ou C.")


def squat_yoshimura(
    relacao_ht: float,
    relacao_lb: float,
    cb: float,
    velocidade_equivalente: float,
) -> float:
    """Calcula o squat máximo na proa pelo método de Yoshimura."""
    return (
        (
            (0.7 + 1.5 / relacao_ht)
            * (cb / relacao_lb)
            + 15
            / relacao_ht
            * (cb / relacao_lb) ** 3
        )
        * velocidade_equivalente**2
        / GRAVIDADE
    )


def selecionar_squat_conservador(resultados: dict[str, float]) -> tuple[str, float]:
    """Seleciona o maior squat entre os métodos aplicáveis."""
    if not resultados:
        raise ValueError("Nenhum método de squat aplicável.")

    metodo = max(resultados, key=resultados.get)
    return metodo, resultados[metodo]


def calcular_squats_aplicaveis(
    tipo_canal: str,
    relacao_ht: float,
    relacao_bt: float,
    relacao_lb: float,
    relacao_lt: float,
    cb: float,
    bloqueio: float,
    froude_profundidade: float,
    velocidade_ms: float,
    velocidade_nos: float,
    volume_deslocamento: float,
    lpp: float,
) -> dict[str, float]:
    """Calcula o squat pelos métodos aplicáveis às condições informadas."""
    resultados = {}

    icorels_valido = verificar_validade_icorels(
        relacao_ht=relacao_ht,
        relacao_bt=relacao_bt,
        relacao_lb=relacao_lb,
        relacao_lt=relacao_lt,
        cb=cb,
        froude_profundidade=froude_profundidade,
    )

    if tipo_canal == "U" and icorels_valido:
        resultados["ICORELS"] = squat_icorels(
            coeficiente_s=coeficiente_squat_icorels(cb),
            volume_deslocamento=volume_deslocamento,
            lpp=lpp,
            froude_profundidade=froude_profundidade,
        )


    barrass_valido = verificar_validade_barrass3(
        relacao_ht=relacao_ht,
        bloqueio=bloqueio,
        cb=cb,
    )

    if tipo_canal in ("U", "R", "C") and barrass_valido:
        resultados["Barrass3"] = squat_barrass3(
            velocidade_nos=velocidade_nos,
            cb=cb,
            bloqueio=bloqueio,
        )


    if tipo_canal in ("U", "R", "C"):
        velocidade_equivalente = velocidade_equivalente_yoshimura(
            velocidade=velocidade_ms,
            bloqueio=bloqueio,
            tipo_canal=tipo_canal,
        )

        resultados["Yoshimura"] = squat_yoshimura(
            relacao_ht=relacao_ht,
            relacao_lb=relacao_lb,
            cb=cb,
            velocidade_equivalente=velocidade_equivalente,
        )

    return resultados         


def margem_manobrabilidade_minima(calado: float) -> float:
    """Calcula a Margem de Manobrabilidade mínima recomendada pela NORMAM-224/DPC."""
    return max(0.05 * calado, 0.60)


def folga_abaixo_quilha(
    profundidade: float,
    calado: float,
    squat: float,
) -> float:
    """Calcula a Folga Abaixo da Quilha considerando o squat."""
    return profundidade - calado - squat


def verificar_faq(faq: float, margem_minima: float) -> bool:
    """Verifica se a FAQ atende à Margem de Manobrabilidade mínima."""
    return faq >= margem_minima


def funcao_profundidade_requerida(
    profundidade: float,
    calado: float,
    squat: float,
    margem_minima: float,
) -> float:
    """Calcula a diferença entre a FAQ e a Margem de Manobrabilidade mínima."""
    return profundidade - calado - squat - margem_minima


def largura_efetiva_canal_irrestrito(
    boca: float,
    cb: float,
) -> float:
    """Calcula a largura efetiva de um canal irrestrito."""
    return (7.04 / cb**0.85) * boca


def verificar_largura_efetiva_canal_irrestrito(
    relacao_ht: float,
) -> bool:
    """Verifica a faixa de aplicação da expressão da largura efetiva."""
    return 1.10 <= relacao_ht <= 1.40


def calcular_squat_na_profundidade(
    profundidade: float,
    embarcacao: Embarcacao,
    canal: Canal,
    area_navio: float,
    velocidade_ms: float,
    velocidade_nos: float,
) -> tuple[str, float]:
    """Calcula o squat conservador para uma profundidade candidata."""
    relacao_ht = relacao_profundidade_calado(
        profundidade,
        embarcacao.calado,
    )

    relacao_bt = relacao_boca_calado(
        embarcacao.boca,
        embarcacao.calado,
    )

    relacao_lb = relacao_comprimento_boca(
        embarcacao.lpp,
        embarcacao.boca,
    )

    relacao_lt = relacao_comprimento_calado(
        embarcacao.lpp,
        embarcacao.calado,
    )
    froude_profundidade = numero_froude_profundidade(
        velocidade_ms,
        profundidade,
    )
    if canal.tipo == "U":
        if not verificar_largura_efetiva_canal_irrestrito(relacao_ht):
            raise ValueError(
                "Relação h/T fora da faixa da expressão da largura efetiva."
            )

        largura_efetiva = largura_efetiva_canal_irrestrito(
            embarcacao.boca,
            embarcacao.cb,
        )

        area_canal = area_secao_canal(
            largura_efetiva,
            profundidade,
        )
    else:
        area_canal = area_secao_canal(
            canal.largura,
            profundidade,
            canal.talude,
        )    
    bloqueio = fator_bloqueio(
        area_navio,
        area_canal,
    )
    deslocamento = volume_deslocamento(
        embarcacao.lpp,
        embarcacao.boca,
        embarcacao.calado,
        embarcacao.cb,
    )
    resultados = calcular_squats_aplicaveis(
        tipo_canal=canal.tipo,
        relacao_ht=relacao_ht,
        relacao_bt=relacao_bt,
        relacao_lb=relacao_lb,
        relacao_lt=relacao_lt,
        cb=embarcacao.cb,
        bloqueio=bloqueio,
        froude_profundidade=froude_profundidade,
        velocidade_ms=velocidade_ms,
        velocidade_nos=velocidade_nos,
        volume_deslocamento=deslocamento,
        lpp=embarcacao.lpp,
    )
    metodo, squat = selecionar_squat_conservador(resultados)

    return metodo, squat        


def avaliar_profundidade(
    profundidade: float,
    embarcacao: Embarcacao,
    canal: Canal,
    area_navio: float,
    velocidade_ms: float,
    velocidade_nos: float,
) -> float:
    """Avalia a diferença entre a FAQ e a margem mínima em uma profundidade candidata."""
    _, squat = calcular_squat_na_profundidade(
        profundidade=profundidade,
        embarcacao=embarcacao,
        canal=canal,
        area_navio=area_navio,
        velocidade_ms=velocidade_ms,
        velocidade_nos=velocidade_nos,
    )
    margem_minima = margem_manobrabilidade_minima(
        embarcacao.calado,
    )
    return funcao_profundidade_requerida(
        profundidade=profundidade,
        calado=embarcacao.calado,
        squat=squat,
        margem_minima=margem_minima,
    )


def profundidade_requerida_bissecao(
    profundidade_inferior: float,
    profundidade_superior: float,
    embarcacao: Embarcacao,
    canal: Canal,
    area_navio: float,
    velocidade_ms: float,
    velocidade_nos: float,
    tolerancia: float = 0.001,
) -> float:
    """Calcula a profundidade requerida pelo método da bisseção."""
    valor_inferior = avaliar_profundidade(
        profundidade=profundidade_inferior,
        embarcacao=embarcacao,
        canal=canal,
        area_navio=area_navio,
        velocidade_ms=velocidade_ms,
        velocidade_nos=velocidade_nos,
    )

    valor_superior = avaliar_profundidade(
        profundidade=profundidade_superior,
        embarcacao=embarcacao,
        canal=canal,
        area_navio=area_navio,
        velocidade_ms=velocidade_ms,
        velocidade_nos=velocidade_nos,
    )
    if valor_inferior * valor_superior > 0:
        raise ValueError(
            "O intervalo informado não contém uma raiz."
        )
    while profundidade_superior - profundidade_inferior > tolerancia:
        profundidade_media = (
            profundidade_inferior + profundidade_superior
        ) / 2
        valor_medio = avaliar_profundidade(
            profundidade=profundidade_media,
            embarcacao=embarcacao,
            canal=canal,
            area_navio=area_navio,
            velocidade_ms=velocidade_ms,
            velocidade_nos=velocidade_nos,
        )
        if valor_inferior * valor_medio <= 0:
            profundidade_superior = profundidade_media
            valor_superior = valor_medio
        else:
            profundidade_inferior = profundidade_media
            valor_inferior = valor_medio
    return (
        profundidade_inferior + profundidade_superior
    ) / 2