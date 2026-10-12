import pytest

from canais_navegacao.canal import Canal


def test_dados_basicos_canal():
    canal = Canal(
        largura=100,
        talude=3,
        profundidade=12,
        comprimento=5000,
        tipo="C",
    )

    assert canal.largura == 100
    assert canal.profundidade == 12
    assert canal.comprimento == 5000
    assert canal.tipo == "C"



def test_canal_irrestrito_sem_largura():
    canal = Canal(
        profundidade=12,
        comprimento=5000,
        tipo="U",
    )

    assert canal.tipo == "U"
    assert canal.largura is None


def test_tipo_canal_invalido():
     with pytest.raises(ValueError):
        Canal(
            largura=100,
            profundidade=12,
            comprimento=5000,
            tipo="X",
        )    


def test_canal_restrito():
    canal = Canal(
        profundidade=12,
        comprimento=5000,
        tipo="R",
        largura=100,
        talude=3,
        altura_calha=5,
    )

    assert canal.largura == 100
    assert canal.talude == 3
    assert canal.altura_calha == 5


def test_canal_artificial():
    canal = Canal(
        profundidade=12,
        comprimento=5000,
        tipo="C",
        largura=100,
        talude=3,
    )

    assert canal.largura == 100
    assert canal.talude == 3
    assert canal.altura_calha is None


def test_canal_restrito_sem_parametros():
    with pytest.raises(ValueError):
        Canal(
            profundidade=12,
            comprimento=5000,
            tipo="R",
        )    


def test_canal_artificial_sem_parametros():
    with pytest.raises(ValueError):
        Canal(
            profundidade=12,
            comprimento=5000,
            tipo="C",
        )        