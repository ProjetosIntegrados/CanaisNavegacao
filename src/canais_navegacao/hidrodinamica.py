import math


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