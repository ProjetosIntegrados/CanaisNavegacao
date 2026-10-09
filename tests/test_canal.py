from canais_navegacao.canal import Canal


def test_dados_basicos_canal():
    canal = Canal(
        largura=100,
        profundidade=12,
        comprimento=5000,
    )

    assert canal.largura == 100
    assert canal.profundidade == 12
    assert canal.comprimento == 5000