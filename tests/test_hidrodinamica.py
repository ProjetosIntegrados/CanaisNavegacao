import pytest

from canais_navegacao.hidrodinamica import numero_froude_profundidade


def test_numero_froude_profundidade():
    resultado = numero_froude_profundidade(
        velocidade=5,
        profundidade=10,
    )

    assert resultado == pytest.approx(0.5048187773)