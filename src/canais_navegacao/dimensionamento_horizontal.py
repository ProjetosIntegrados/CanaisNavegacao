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
