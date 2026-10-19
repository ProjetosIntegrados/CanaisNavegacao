from canais_navegacao.batimetria import PontoBatimetrico, SecaoBatimetrica


def test_criar_ponto_batimetrico():
    ponto = PontoBatimetrico(
        offset=-20.0,
        profundidade=10.8,
    )

    assert ponto.offset == -20.0
    assert ponto.profundidade == 10.8


def test_criar_secao_batimetrica():
    pontos = [
        PontoBatimetrico(offset=-20.0, profundidade=10.8),
        PontoBatimetrico(offset=0.0, profundidade=11.3),
        PontoBatimetrico(offset=20.0, profundidade=10.7),
    ]

    secao = SecaoBatimetrica(
        identificacao="001",
        distancia=0.0,
        pontos=pontos,
    )

    assert secao.identificacao == "001"
    assert secao.distancia == 0.0
    assert secao.pontos == pontos    