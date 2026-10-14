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
    coeficiente_squat_icorels,
    volume_deslocamento,
    squat_icorels,
    verificar_validade_icorels,
    relacao_boca_calado,
    relacao_comprimento_boca,
    relacao_comprimento_calado,
    velocidade_equivalente_yoshimura,
    squat_yoshimura,
    calcular_squats_aplicaveis,
    selecionar_squat_conservador,
    margem_manobrabilidade_minima,
    folga_abaixo_quilha,
    verificar_faq,
    funcao_profundidade_requerida,
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


def test_coeficiente_squat_icorels():
    assert coeficiente_squat_icorels(0.65) == 1.7
    assert coeficiente_squat_icorels(0.75) == 2.0
    assert coeficiente_squat_icorels(0.85) == 2.4    


def test_volume_deslocamento():
    volume = volume_deslocamento(
        lpp=200,
        boca=30,
        calado=10,
        cb=0.75,
    )

    assert volume == 45000    


def test_squat_icorels():
    cs = coeficiente_squat_icorels(0.75)
    volume = volume_deslocamento(
        lpp=200,
        boca=30,
        calado=10,
        cb=0.75,
    )
    froude = numero_froude_profundidade(
        velocidade=5,
        profundidade=12,
    )

    squat = squat_icorels(
        coeficiente_s=cs,
        volume_deslocamento=volume,
        lpp=200,
        froude_profundidade=froude,
    )

    assert squat == pytest.approx(0.53841, abs=0.00001)


def test_validade_icorels():
    valido = verificar_validade_icorels(
        relacao_ht=1.2,
        relacao_bt=3.0,
        relacao_lb=7.0,
        relacao_lt=18.0,
        cb=0.75,
        froude_profundidade=0.5,
    )

    assert valido is True      


def test_invalidade_icorels():
    assert verificar_validade_icorels(
        1.0, 3.0, 7.0, 18.0, 0.75, 0.5
    ) is False

    assert verificar_validade_icorels(
        1.2, 2.0, 7.0, 18.0, 0.75, 0.5
    ) is False

    assert verificar_validade_icorels(
        1.2, 3.0, 5.0, 18.0, 0.75, 0.5
    ) is False

    assert verificar_validade_icorels(
        1.2, 3.0, 7.0, 15.0, 0.75, 0.5
    ) is False

    assert verificar_validade_icorels(
        1.2, 3.0, 7.0, 18.0, 0.55, 0.5
    ) is False

    assert verificar_validade_icorels(
        1.2, 3.0, 7.0, 18.0, 0.75, 0.8
    ) is False    


def test_relacao_boca_calado():
    resultado = relacao_boca_calado(
        boca=30,
        calado=10,
    )

    assert resultado == 3.0    


def test_relacao_comprimento_boca():
    resultado = relacao_comprimento_boca(
        lpp=200,
        boca=30,
    )

    assert resultado == pytest.approx(6.66667, abs=0.00001)    


def test_relacao_comprimento_calado():
    resultado = relacao_comprimento_calado(
        lpp=200,
        calado=10,
    )

    assert resultado == 20.0

def test_velocidade_equivalente_yoshimura_canal_u():
    velocidade_equivalente = velocidade_equivalente_yoshimura(
        velocidade=5,
        bloqueio=0.1,
        tipo_canal="U",
    )

    assert velocidade_equivalente == 5  


def test_velocidade_equivalente_yoshimura_canal_restrito():
    velocidade_equivalente = velocidade_equivalente_yoshimura(
        velocidade=5,
        bloqueio=0.1,
        tipo_canal="R",
    )

    assert velocidade_equivalente == pytest.approx(5.55556, abs=0.00001) 


def test_squat_yoshimura():
    relacao_ht = relacao_profundidade_calado(
        profundidade=12,
        calado=10,
    )
    relacao_lb = relacao_comprimento_boca(
        lpp=200,
        boca=30,
    )

    squat = squat_yoshimura(
        relacao_ht=relacao_ht,
        relacao_lb=relacao_lb,
        cb=0.75,
        velocidade_equivalente=5,
    )

    assert squat == pytest.approx(0.6044, abs=0.0001)


def test_velocidade_equivalente_yoshimura_tipo_invalido():
    with pytest.raises(ValueError):
        velocidade_equivalente_yoshimura(
            velocidade=5,
            bloqueio=0.1,
            tipo_canal="X",
        )


def test_selecionar_squat_conservador():
    resultados = {
        "ICORELS": 0.54,
        "Barrass3": 0.62,
        "Yoshimura": 0.60,
    }

    metodo, squat = selecionar_squat_conservador(resultados)

    assert metodo == "Barrass3"
    assert squat == pytest.approx(0.62) 


def test_selecionar_squat_conservador_sem_metodos():
    with pytest.raises(ValueError):
        selecionar_squat_conservador({})       


def test_calcular_squats_aplicaveis_tres_metodos():
    resultados = calcular_squats_aplicaveis(
        tipo_canal="U",
        relacao_ht=1.2,
        relacao_bt=3.0,
        relacao_lb=6.67,
        relacao_lt=20.0,
        cb=0.75,
        bloqueio=0.10,
        froude_profundidade=0.46,
        velocidade_ms=5.0,
        velocidade_nos=10.0,
        volume_deslocamento=45000,
        lpp=200,
    )

    assert "ICORELS" in resultados
    assert "Barrass3" in resultados
    assert "Yoshimura" in resultados   


def test_calcular_squats_aplicaveis_canal_restrito():
    resultados = calcular_squats_aplicaveis(
        tipo_canal="R",
        relacao_ht=1.2,
        relacao_bt=3.0,
        relacao_lb=6.67,
        relacao_lt=20.0,
        cb=0.75,
        bloqueio=0.10,
        froude_profundidade=0.46,
        velocidade_ms=5.0,
        velocidade_nos=10.0,
        volume_deslocamento=45000,
        lpp=200,
    )

    assert "ICORELS" not in resultados
    assert "Barrass3" in resultados
    assert "Yoshimura" in resultados 


def test_calcular_squats_aplicaveis_barrass_invalido():
    resultados = calcular_squats_aplicaveis(
        tipo_canal="U",
        relacao_ht=1.6,
        relacao_bt=3.0,
        relacao_lb=6.67,
        relacao_lt=20.0,
        cb=0.75,
        bloqueio=0.10,
        froude_profundidade=0.46,
        velocidade_ms=5.0,
        velocidade_nos=10.0,
        volume_deslocamento=45000,
        lpp=200,
    )

    assert "ICORELS" in resultados
    assert "Barrass3" not in resultados
    assert "Yoshimura" in resultados 


def test_selecao_conservadora_com_metodos_aplicaveis():
    resultados = calcular_squats_aplicaveis(
        tipo_canal="U",
        relacao_ht=1.2,
        relacao_bt=3.0,
        relacao_lb=6.67,
        relacao_lt=20.0,
        cb=0.75,
        bloqueio=0.10,
        froude_profundidade=0.46,
        velocidade_ms=5.0,
        velocidade_nos=10.0,
        volume_deslocamento=45000,
        lpp=200,
    )

    metodo, squat = selecionar_squat_conservador(resultados)

    assert squat == max(resultados.values())
    assert metodo in resultados     


def test_margem_manobrabilidade_minima():
    assert margem_manobrabilidade_minima(10.0) == pytest.approx(0.60)
    assert margem_manobrabilidade_minima(14.0) == pytest.approx(0.70)


def test_folga_abaixo_quilha():
    faq = folga_abaixo_quilha(
        profundidade=12.0,
        calado=10.0,
        squat=0.60,
    )

    assert faq == pytest.approx(1.40)


def test_verificar_faq():
    assert verificar_faq(1.40, 0.60) is True
    assert verificar_faq(0.45, 0.60) is False    


def test_funcao_profundidade_requerida():
    resultado = funcao_profundidade_requerida(
        profundidade=11.25,
        calado=10.0,
        squat=0.67,
        margem_minima=0.60,
    )

    assert resultado == pytest.approx(-0.02)                  