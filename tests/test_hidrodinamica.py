import pytest

from canais_navegacao.hidrodinamica import (
    numero_froude_profundidade,
    relacao_profundidade_calado,
    area_secao_canal,
    largura_topo_canal,
    profundidade_media,
    coeficiente_velocidade_critica,
    velocidade_critica,
    fator_bloqueio,
    squat_barrass3,
    verificar_validade_barrass3,
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
        largura=80,
        profundidade=11,
        talude=3,
    )

    assert resultado == pytest.approx(1243)


def test_largura_topo_canal():
    resultado = largura_topo_canal(
        largura=80,
        profundidade=11,
        talude=3,
    )

    assert resultado == pytest.approx(146)


def test_profundidade_media():
    resultado = profundidade_media(
        area_canal=1243,
        largura_topo=146,
    )

    assert resultado == pytest.approx(8.5136986301)


def test_coeficiente_velocidade_critica():
    resultado = coeficiente_velocidade_critica(
        bloqueio=0.10,
    )

    assert resultado == pytest.approx(0.6228144402)


def test_velocidade_critica():
    resultado = velocidade_critica(
        coeficiente_critico=0.6228144402,
        profundidade_media=8.5136986301,
    )

    assert resultado == pytest.approx(5.6918351513)

        
def test_fator_bloqueio():
    resultado = fator_bloqueio(
        area_navio=120,
        area_canal=1200,
    )

    assert resultado == pytest.approx(0.1)


def test_squat_barrass3():
    resultado = squat_barrass3(
        velocidade_nos=10,
        cb=0.75,
        bloqueio=0.10,
    )

    assert resultado == pytest.approx(0.7481232568)


def test_validade_barrass3_parametros_validos():
    resultado = verificar_validade_barrass3(
        relacao_ht=1.2,
        bloqueio=0.10,
        cb=0.75,
    )

    assert resultado is True


def test_validade_barrass3_parametros_invalidos():
    resultado = verificar_validade_barrass3(
        relacao_ht=1.6,
        bloqueio=0.10,
        cb=0.75,
    )

    assert resultado is False    