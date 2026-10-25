def calcular_largura_manobrabilidade_basica(
    boca: float,
    manobrabilidade: str,
) -> float:
    """Calcula a largura básica de manobrabilidade WBM."""
    fatores = {
        "boa": 1.3,
        "moderada": 1.5,
        "baixa": 1.8,
    }

    fator = fatores[manobrabilidade]

    return fator * boca


def calcular_fator_velocidade(
    boca: float,
    velocidade: float,
) -> float:
    """Calcula W1 associado à velocidade do navio."""
    if velocidade > 12:
        return 0.1 * boca

    return 0.0


def calcular_fator_vento_transversal(
    boca: float,
    velocidade_vento: float,
    velocidade_navio: str,
    muita_area_lateral: bool = False,
) -> float:
    """Calcula W2 associado ao vento transversal."""
    if velocidade_vento <= 15:
        fatores = {
            "alta": 0.1,
            "moderada": 0.2,
            "baixa": 0.3,
        }
    elif velocidade_vento < 33:
        fatores = {
            "alta": 0.3,
            "moderada": 0.4,
            "baixa": 0.6,
        }
    elif velocidade_vento < 48:
        fatores = {
            "alta": 0.5,
            "moderada": 0.7,
            "baixa": 1.1,
        }
    else:
        raise ValueError(
            "Velocidade do vento fora da faixa da metodologia."
        )

    fator = fatores[velocidade_navio]

    if muita_area_lateral:
        fator += 0.2

    return fator * boca


def calcular_fator_corrente_transversal(
    boca: float,
    velocidade_corrente: float,
    velocidade_navio: str,
    canal_abrigado: bool,
) -> float:
    """Calcula W3 associado à corrente transversal."""
    if velocidade_corrente < 0.2:
        return 0.0

    if velocidade_corrente < 0.5:
        fatores = {
            "alta": (0.2, 0.1),
            "moderada": (0.25, 0.2),
            "baixa": (0.3, 0.3),
        }
    elif velocidade_corrente < 1.5:
        fatores = {
            "alta": (0.5, 0.4),
            "moderada": (0.7, 0.6),
            "baixa": (1.0, 0.8),
        }
    elif velocidade_corrente < 2:
        if canal_abrigado:
            raise ValueError(
                "Corrente transversal forte em canal abrigado "
                "requer simulacao de manobra."
            )

        fatores = {
            "alta": (1.0, 0.0),
            "moderada": (1.2, 0.0),
            "baixa": (1.6, 0.0),
        }
    else:
        raise ValueError(
            "Velocidade da corrente transversal fora da faixa da metodologia."
        )

    indice = 1 if canal_abrigado else 0
    fator = fatores[velocidade_navio][indice]

    return fator * boca


def calcular_fator_corrente_longitudinal(
    boca: float,
    velocidade_corrente: float,
    velocidade_navio: str,
) -> float:
    """Calcula W4 associado à corrente longitudinal."""
    if velocidade_corrente <= 1.5:
        return 0.0

    if velocidade_corrente < 3:
        fatores = {
            "alta": 0.0,
            "moderada": 0.1,
            "baixa": 0.2,
        }
    else:
        fatores = {
            "alta": 0.1,
            "moderada": 0.2,
            "baixa": 0.4,
        }

    return fatores[velocidade_navio] * boca


def calcular_fator_ondas(
    boca: float,
    altura_significativa: float,
    canal_abrigado: bool,
) -> float:
    """Calcula W5 associado à altura significativa das ondas."""
    if canal_abrigado:
        return 0.0

    if altura_significativa <= 1:
        fator = 0.0
    elif altura_significativa < 3:
        fator = 0.5
    else:
        fator = 1.0

    return fator * boca


def calcular_fator_auxilios_navegacao(
    boca: float,
    classificacao: str,
) -> float:
    """Calcula W6 associado aos auxílios à navegação."""
    fatores = {
        "excelente": 0.0,
        "bom": 0.2,
        "moderado": 0.4,
    }

    return fatores[classificacao] * boca


def calcular_fator_superficie_fundo(
    boca: float,
    profundidade: float,
    calado: float,
    tipo_fundo: str,
) -> float:
    """Calcula W7 associado aos efeitos da superfície de fundo."""
    if profundidade >= 1.5 * calado:
        return 0.0

    fatores = {
        "liso_mole": 0.1,
        "irregular_duro": 0.2,
    }

    return fatores[tipo_fundo] * boca


def calcular_fator_profundidade(
    boca: float,
    profundidade: float,
    calado: float,
    canal_abrigado: bool,
) -> float:
    """Calcula W8 associado aos efeitos da profundidade."""
    relacao = profundidade / calado

    if relacao >= 1.5:
        return 0.0

    if canal_abrigado:
        if relacao > 1.15:
            return 0.2 * boca

        return 0.4 * boca

    if relacao > 1.25:
        return 0.1 * boca

    return 0.2 * boca


def calcular_fator_carga_perigosa() -> float:
    """Calcula W9 associado à periculosidade da carga."""
    return 0.0


def calcular_fator_intensidade_trafego(
    boca: float,
    intensidade: str,
) -> float:
    """Calcula W10 associado à intensidade do tráfego."""
    fatores = {
        "baixa": 0.0,
        "media": 0.0,
        "alta": 0.5,
    }

    return fatores[intensidade] * boca


def calcular_largura_manobra(
    wbm: float,
    fatores: list[float],
) -> float:
    """Calcula a largura de manobra WM."""
    return wbm + sum(fatores)


def calcular_folga_margem(
    boca: float,
    tipo_margem: str,
    velocidade_navio: str,
) -> float:
    """Calcula a folga de segurança associada a uma margem do canal."""
    fatores = {
        "inclinada_suave": {
            "alta": 0.2,
            "moderada": 0.1,
            "baixa": 0.0,
        },
        "inclinada_ingreme": {
            "alta": 0.7,
            "moderada": 0.5,
            "baixa": 0.3,
        },
        "vertical": {
            "alta": 1.3,
            "moderada": 1.0,
            "baixa": 0.5,
        },
    }

    fator = fatores[tipo_margem][velocidade_navio]

    return fator * boca


def calcular_largura_canal_mao_unica(
    largura_manobra: float,
    folga_margem_esquerda: float,
    folga_margem_direita: float,
) -> float:
    """Calcula a largura requerida para canal de mão única."""
    return (
        largura_manobra
        + folga_margem_esquerda
        + folga_margem_direita
    )


def calcular_largura_passagem(
    boca: float,
    velocidade_navio: str,
    canal_abrigado: bool,
) -> float:
    """Calcula WP para canal com duas faixas de navegação."""
    if canal_abrigado:
        fatores = {
            "alta": 1.8,
            "moderada": 1.4,
            "baixa": 1.0,
        }
    else:
        fatores = {
            "alta": 2.0,
            "moderada": 1.6,
            "baixa": 1.2,
        }

    return fatores[velocidade_navio] * boca


def calcular_largura_canal_mao_dupla(
    largura_manobra: float,
    folga_margem_esquerda: float,
    folga_margem_direita: float,
    largura_passagem: float,
) -> float:
    """Calcula a largura requerida para canal de mão dupla."""
    return (
        2 * largura_manobra
        + folga_margem_esquerda
        + folga_margem_direita
        + largura_passagem
    )
