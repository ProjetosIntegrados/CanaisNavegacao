import pytest

from canais_navegacao.dimensionamento_horizontal import (
    calcular_largura_manobrabilidade_basica,
)


def test_largura_manobrabilidade_boa():
    resultado = calcular_largura_manobrabilidade_basica(
        boca=30.0,
        manobrabilidade="boa",
    )

    assert resultado == pytest.approx(39.0)


def test_largura_manobrabilidade_moderada():
    resultado = calcular_largura_manobrabilidade_basica(
        boca=30.0,
        manobrabilidade="moderada",
    )

    assert resultado == pytest.approx(45.0)


def test_largura_manobrabilidade_baixa():
    resultado = calcular_largura_manobrabilidade_basica(
        boca=30.0,
        manobrabilidade="baixa",
    )

    assert resultado == pytest.approx(54.0)
    