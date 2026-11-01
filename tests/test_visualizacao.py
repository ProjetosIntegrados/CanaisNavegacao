import pytest

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

from canais_navegacao.batimetria import (
    PontoBatimetrico,
    SecaoBatimetrica,
)
from canais_navegacao.visualizacao import (
    calcular_direcao_secao,
    plotar_perfil_longitudinal,
    plotar_planta_canal,
    plotar_secao_transversal,
    plotar_volumes_dragagem,
)


def test_calcular_direcao_secao():
    secoes = [
        SecaoBatimetrica(
            identificacao="Estaca 0",
            distancia=0.0,
            pontos=[],
            x=0.0,
            y=0.0,
        ),
        SecaoBatimetrica(
            identificacao="Estaca 1",
            distancia=100.0,
            pontos=[],
            x=100.0,
            y=0.0,
        ),
        SecaoBatimetrica(
            identificacao="Estaca 2",
            distancia=200.0,
            pontos=[],
            x=200.0,
            y=100.0,
        ),
    ]

    direcao_x, direcao_y = calcular_direcao_secao(
        secoes=secoes,
        indice=1,
    )

    assert direcao_x == pytest.approx(0.894427)
    assert direcao_y == pytest.approx(0.447214)



def test_plotar_secao_transversal(monkeypatch):
    secao = SecaoBatimetrica(
        identificacao="Estaca 0",
        distancia=0.0,
        pontos=[
            PontoBatimetrico(-50.0, 5.0),
            PontoBatimetrico(-30.0, 8.0),
            PontoBatimetrico(-20.0, 9.0),
            PontoBatimetrico(0.0, 12.0),
            PontoBatimetrico(20.0, 9.0),
            PontoBatimetrico(30.0, 8.0),
            PontoBatimetrico(50.0, 5.0),
        ],
    )

    monkeypatch.setattr(plt, "show", lambda: None)

    plotar_secao_transversal(
        secao=secao,
        largura=40.0,
        profundidade=10.0,
        talude=3.0,
    )

    eixo = plt.gca()

    assert "Estaca 0" in eixo.get_title()
    assert "10.95 m²" in eixo.get_title()
    assert eixo.get_xlabel() == "Offset (m)"
    assert eixo.get_ylabel() == "Profundidade (m)"

    plt.close()


def test_plotar_perfil_longitudinal(monkeypatch):
    secoes = [
        SecaoBatimetrica(
            identificacao="Estaca 0",
            distancia=0.0,
            pontos=[
                PontoBatimetrico(-20.0, 10.5),
                PontoBatimetrico(0.0, 12.0),
                PontoBatimetrico(20.0, 10.5),
            ],
        ),
        SecaoBatimetrica(
            identificacao="Estaca 1",
            distancia=100.0,
            pontos=[
                PontoBatimetrico(-20.0, 9.5),
                PontoBatimetrico(0.0, 11.0),
                PontoBatimetrico(20.0, 9.5),
            ],
        ),
    ]

    monkeypatch.setattr(plt, "show", lambda: None)

    plotar_perfil_longitudinal(
        secoes=secoes,
        largura=40.0,
        profundidade_requerida=10.0,
    )

    eixo = plt.gca()

    assert eixo.get_title() == "Perfil longitudinal do canal"
    assert eixo.get_xlabel() == "Distância ao longo do canal (m)"
    assert eixo.get_ylabel() == "Profundidade (m)"

    plt.close()


def test_plotar_volumes_dragagem(monkeypatch):
    resultados = [
        ("Estaca 0", 0.0, 10.5, 10.0, 0.0, False, 2.0),
        ("Estaca 1", 100.0, 9.5, 10.0, 0.5, True, 4.0),
        ("Estaca 2", 200.0, 10.5, 10.0, 0.0, False, 2.0),
    ]

    monkeypatch.setattr(plt, "show", lambda: None)

    plotar_volumes_dragagem(
        resultados_secoes=resultados,
    )

    eixo = plt.gca()

    assert "Volumes de dragagem do canal" in eixo.get_title()
    assert "600.00 m³" in eixo.get_title()
    assert eixo.get_xlabel() == "Trecho do canal"
    assert eixo.get_ylabel() == "Volume de dragagem (m³)"

    plt.close()


def test_plotar_planta_canal(monkeypatch):
    secoes = [
        SecaoBatimetrica(
            identificacao="Estaca 0",
            distancia=0.0,
            pontos=[],
            x=0.0,
            y=0.0,
        ),
        SecaoBatimetrica(
            identificacao="Estaca 1",
            distancia=100.0,
            pontos=[],
            x=100.0,
            y=0.0,
        ),
        SecaoBatimetrica(
            identificacao="Estaca 2",
            distancia=200.0,
            pontos=[],
            x=200.0,
            y=50.0,
        ),
    ]

    diagnostico = [
        (
            "Estaca 0",
            0.0,
            10.5,
            10.0,
            0.0,
            True,
            50.0,
            40.0,
            0.0,
            True,
            True,
        ),
        (
            "Estaca 1",
            100.0,
            9.5,
            10.0,
            0.5,
            False,
            30.0,
            40.0,
            10.0,
            False,
            False,
        ),
        (
            "Estaca 2",
            200.0,
            9.8,
            10.0,
            0.2,
            False,
            35.0,
            40.0,
            5.0,
            False,
            False,
        ),
    ]

    monkeypatch.setattr(plt, "show", lambda: None)

    plotar_planta_canal(
        secoes=secoes,
        largura_requerida=40.0,
        diagnostico=diagnostico,
    )

    eixo = plt.gca()

    assert eixo.get_title() == "Planta do canal"
    assert eixo.get_xlabel() == "X (m)"
    assert eixo.get_ylabel() == "Y (m)"

    plt.close()