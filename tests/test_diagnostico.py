import pytest

from canais_navegacao.batimetria import (
    PontoBatimetrico,
    SecaoBatimetrica,
)
from canais_navegacao.diagnostico import diagnosticar_secao


def test_diagnosticar_secao():
    secao = SecaoBatimetrica(
        identificacao="Estaca 0",
        distancia=0.0,
        pontos=[
            PontoBatimetrico(-40.0, 8.0),
            PontoBatimetrico(-20.0, 11.0),
            PontoBatimetrico(0.0, 12.0),
            PontoBatimetrico(20.0, 11.0),
            PontoBatimetrico(40.0, 8.0),
        ],
    )

    resultado = diagnosticar_secao(
        secao=secao,
        largura_requerida=40.0,
        profundidade_requerida=10.0,
    )

    assert resultado[0] == "Estaca 0"
    assert resultado[1] == 0.0
    assert resultado[5] is True
    assert resultado[9] is True
    assert resultado[10] is True


def test_diagnosticar_secao_nao_atende():
    secao = SecaoBatimetrica(
        identificacao="Estaca 0",
        distancia=0.0,
        pontos=[
            PontoBatimetrico(-40.0, 8.0),
            PontoBatimetrico(-20.0, 11.0),
            PontoBatimetrico(0.0, 12.0),
            PontoBatimetrico(20.0, 11.0),
            PontoBatimetrico(40.0, 8.0),
        ],
    )

    resultado = diagnosticar_secao(
        secao=secao,
        largura_requerida=60.0,
        profundidade_requerida=10.0,
    )

    assert resultado[5] is False
    assert resultado[9] is False
    assert resultado[10] is False
    