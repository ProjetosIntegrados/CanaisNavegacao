import matplotlib.pyplot as plt

from canais_navegacao.batimetria import (
    PontoBatimetrico,
    SecaoBatimetrica,
)
from canais_navegacao.visualizacao import plotar_secao_transversal


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
    