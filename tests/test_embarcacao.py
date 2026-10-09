from canais_navegacao.embarcacao import Embarcacao


def test_dados_basicos_embarcacao():
    navio = Embarcacao(200, 32, 10, 0.75)

    assert navio.lpp == 200
    assert navio.boca == 32
    assert navio.calado == 10
    assert navio.cb == 0.75