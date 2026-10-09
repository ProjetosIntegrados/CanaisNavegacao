import pytest

from canais_navegacao.hidrodinamica import (
    numero_froude_profundidade,
    relacao_profundidade_calado,
    area_secao_canal,
    fator_bloqueio,
)


def test_numero_froude_profundidade():
    resultado = numero_froude_profundidade(
        velocidade=5,
        profundidade=10,
    )

    assert resultado == pytest.approx(0.5048187773)


def test_relacao_profundidade_calado():
    resultado = relacao_profundidade_calado(
        profundidade=12,
        calado=10,
    )

    assert resultado == pytest.approx(1.2)


def test_area_secao_canal():
    resultado = area_secao_canal(
        largura=100,
        profundidade=12,
    )

    assert resultado == pytest.approx(1200)
    

def test_fator_bloqueio():
    resultado = fator_bloqueio(
        area_navio=120,
        area_canal=1200,
    )

    assert resultado == pytest.approx(0.1)