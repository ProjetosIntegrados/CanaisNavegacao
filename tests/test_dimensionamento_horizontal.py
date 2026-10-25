import pytest

from canais_navegacao.dimensionamento_horizontal import (
    calcular_largura_manobrabilidade_basica,
    calcular_fator_velocidade,
    calcular_fator_vento_transversal,
    calcular_fator_corrente_transversal,
    calcular_fator_corrente_longitudinal,
    calcular_fator_ondas,
    calcular_fator_auxilios_navegacao,
    calcular_fator_superficie_fundo,
    calcular_fator_profundidade,
    calcular_fator_carga_perigosa,
    calcular_fator_intensidade_trafego,
    calcular_largura_manobra,
    calcular_folga_margem,
    calcular_largura_canal_mao_unica,
    calcular_largura_passagem,
    calcular_largura_canal_mao_dupla,
    calcular_largura_adicional_deriva,
    calcular_largura_adicional_tempo_resposta,
    calcular_largura_adicional_curva,
    calcular_largura_canal_curva,
    calcular_raio_recomendado_curva,
    calcular_raio_minimo_curva,
    verificar_raio_curva,
)


def test_largura_manobrabilidade_boa():
    resultado = calcular_largura_manobrabilidade_basica(
        boca=30.0,
        manobrabilidade="boa",
    )

    assert resultado == pytest.approx(39.0)


def test_largura_manobrabilidade_moderada():
    resultado = calcular_largura_manobrabilidade_basica(
        boca=30.0,
        manobrabilidade="moderada",
    )

    assert resultado == pytest.approx(45.0)


def test_largura_manobrabilidade_baixa():
    resultado = calcular_largura_manobrabilidade_basica(
        boca=30.0,
        manobrabilidade="baixa",
    )

    assert resultado == pytest.approx(54.0)


def test_fator_velocidade_alta():
    resultado = calcular_fator_velocidade(
        boca=20,
        velocidade=15,
    )

    assert resultado == 2.0


def test_fator_velocidade_moderada():
    resultado = calcular_fator_velocidade(
        boca=20,
        velocidade=10,
    )

    assert resultado == 0.0


def test_fator_vento_transversal_brando():
    resultado = calcular_fator_vento_transversal(
        boca=20,
        velocidade_vento=10,
        velocidade_navio="moderada",
    )

    assert resultado == 4.0


def test_fator_vento_transversal_moderado():
    resultado = calcular_fator_vento_transversal(
        boca=20,
        velocidade_vento=20,
        velocidade_navio="moderada",
    )

    assert resultado == 8.0


def test_fator_vento_transversal_forte():
    resultado = calcular_fator_vento_transversal(
        boca=20,
        velocidade_vento=40,
        velocidade_navio="baixa",
    )

    assert resultado == 22.0


def test_fator_vento_transversal_muita_area_lateral():
    resultado = calcular_fator_vento_transversal(
        boca=20,
        velocidade_vento=20,
        velocidade_navio="moderada",
        muita_area_lateral=True,
    )

    assert resultado == pytest.approx(12.0)


def test_fator_corrente_transversal_fraca_canal_abrigado():
    resultado = calcular_fator_corrente_transversal(
        boca=20,
        velocidade_corrente=0.3,
        velocidade_navio="moderada",
        canal_abrigado=True,
    )

    assert resultado == pytest.approx(4.0)


def test_fator_corrente_transversal_moderada_canal_desabrigado():
    resultado = calcular_fator_corrente_transversal(
        boca=20,
        velocidade_corrente=1.0,
        velocidade_navio="baixa",
        canal_abrigado=False,
    )

    assert resultado == pytest.approx(20.0)


def test_fator_corrente_transversal_forte_canal_abrigado():
    with pytest.raises(ValueError):
        calcular_fator_corrente_transversal(
            boca=20,
            velocidade_corrente=1.7,
            velocidade_navio="moderada",
            canal_abrigado=True,
        )


def test_fator_corrente_longitudinal_fraca():
    resultado = calcular_fator_corrente_longitudinal(
        boca=20,
        velocidade_corrente=1.0,
        velocidade_navio="moderada",
    )

    assert resultado == pytest.approx(0.0)


def test_fator_corrente_longitudinal_moderada():
    resultado = calcular_fator_corrente_longitudinal(
        boca=20,
        velocidade_corrente=2.0,
        velocidade_navio="moderada",
    )

    assert resultado == pytest.approx(2.0)


def test_fator_corrente_longitudinal_forte():
    resultado = calcular_fator_corrente_longitudinal(
        boca=20,
        velocidade_corrente=3.5,
        velocidade_navio="baixa",
    )

    assert resultado == pytest.approx(8.0)


def test_fator_ondas_canal_abrigado():
    resultado = calcular_fator_ondas(
        boca=20,
        altura_significativa=2.0,
        canal_abrigado=True,
    )

    assert resultado == pytest.approx(0.0)


def test_fator_ondas_moderadas_canal_desabrigado():
    resultado = calcular_fator_ondas(
        boca=20,
        altura_significativa=2.0,
        canal_abrigado=False,
    )

    assert resultado == pytest.approx(10.0)


def test_fator_ondas_altas_canal_desabrigado():
    resultado = calcular_fator_ondas(
        boca=20,
        altura_significativa=3.5,
        canal_abrigado=False,
    )

    assert resultado == pytest.approx(20.0)


def test_fator_auxilios_excelentes():
    resultado = calcular_fator_auxilios_navegacao(
        boca=20,
        classificacao="excelente",
    )

    assert resultado == pytest.approx(0.0)


def test_fator_auxilios_bons():
    resultado = calcular_fator_auxilios_navegacao(
        boca=20,
        classificacao="bom",
    )

    assert resultado == pytest.approx(4.0)


def test_fator_auxilios_moderados():
    resultado = calcular_fator_auxilios_navegacao(
        boca=20,
        classificacao="moderado",
    )

    assert resultado == pytest.approx(8.0)


def test_fator_superficie_fundo_profundidade_maior():
    resultado = calcular_fator_superficie_fundo(
        boca=20,
        profundidade=15,
        calado=10,
        tipo_fundo="irregular_duro",
    )

    assert resultado == pytest.approx(0.0)


def test_fator_superficie_fundo_liso_mole():
    resultado = calcular_fator_superficie_fundo(
        boca=20,
        profundidade=12,
        calado=10,
        tipo_fundo="liso_mole",
    )

    assert resultado == pytest.approx(2.0)


def test_fator_superficie_fundo_irregular_duro():
    resultado = calcular_fator_superficie_fundo(
        boca=20,
        profundidade=12,
        calado=10,
        tipo_fundo="irregular_duro",
    )

    assert resultado == pytest.approx(4.0)


def test_fator_profundidade_canal_desabrigado():
    resultado = calcular_fator_profundidade(
        boca=20,
        profundidade=13,
        calado=10,
        canal_abrigado=False,
    )

    assert resultado == pytest.approx(2.0)


def test_fator_profundidade_rasa_canal_desabrigado():
    resultado = calcular_fator_profundidade(
        boca=20,
        profundidade=12,
        calado=10,
        canal_abrigado=False,
    )

    assert resultado == pytest.approx(4.0)


def test_fator_profundidade_canal_abrigado():
    resultado = calcular_fator_profundidade(
        boca=20,
        profundidade=13,
        calado=10,
        canal_abrigado=True,
    )

    assert resultado == pytest.approx(4.0)


def test_fator_profundidade_rasa_canal_abrigado():
    resultado = calcular_fator_profundidade(
        boca=20,
        profundidade=11,
        calado=10,
        canal_abrigado=True,
    )

    assert resultado == pytest.approx(8.0)


def test_fator_carga_perigosa():
    resultado = calcular_fator_carga_perigosa()

    assert resultado == pytest.approx(0.0)


def test_fator_intensidade_trafego_baixa():
    resultado = calcular_fator_intensidade_trafego(
        boca=20,
        intensidade="baixa",
    )

    assert resultado == pytest.approx(0.0)


def test_fator_intensidade_trafego_media():
    resultado = calcular_fator_intensidade_trafego(
        boca=20,
        intensidade="media",
    )

    assert resultado == pytest.approx(0.0)


def test_fator_intensidade_trafego_alta():
    resultado = calcular_fator_intensidade_trafego(
        boca=20,
        intensidade="alta",
    )

    assert resultado == pytest.approx(10.0)


def test_calcular_largura_manobra():
    resultado = calcular_largura_manobra(
        wbm=30.0,
        fatores=[
            2.0,
            4.0,
            5.0,
            2.0,
            10.0,
            4.0,
            2.0,
            4.0,
            0.0,
            10.0,
        ],
    )

    assert resultado == pytest.approx(73.0)


def test_folga_margem_inclinada_suave():
    resultado = calcular_folga_margem(
        boca=20,
        tipo_margem="inclinada_suave",
        velocidade_navio="moderada",
    )

    assert resultado == pytest.approx(2.0)


def test_folga_margem_inclinada_ingreme():
    resultado = calcular_folga_margem(
        boca=20,
        tipo_margem="inclinada_ingreme",
        velocidade_navio="moderada",
    )

    assert resultado == pytest.approx(10.0)


def test_folga_margem_vertical():
    resultado = calcular_folga_margem(
        boca=20,
        tipo_margem="vertical",
        velocidade_navio="moderada",
    )

    assert resultado == pytest.approx(20.0)


def test_folga_margem_velocidade_baixa():
    resultado = calcular_folga_margem(
        boca=20,
        tipo_margem="inclinada_suave",
        velocidade_navio="baixa",
    )

    assert resultado == pytest.approx(0.0)


def test_calcular_largura_canal_mao_unica():
    resultado = calcular_largura_canal_mao_unica(
        largura_manobra=60.0,
        folga_margem_esquerda=10.0,
        folga_margem_direita=14.0,
    )

    assert resultado == pytest.approx(84.0)


def test_largura_passagem_canal_abrigado():
    resultado = calcular_largura_passagem(
        boca=20,
        velocidade_navio="moderada",
        canal_abrigado=True,
    )

    assert resultado == pytest.approx(28.0)


def test_largura_passagem_canal_desabrigado():
    resultado = calcular_largura_passagem(
        boca=20,
        velocidade_navio="moderada",
        canal_abrigado=False,
    )

    assert resultado == pytest.approx(32.0)


def test_largura_passagem_velocidade_alta():
    resultado = calcular_largura_passagem(
        boca=20,
        velocidade_navio="alta",
        canal_abrigado=False,
    )

    assert resultado == pytest.approx(40.0)


def test_largura_passagem_velocidade_baixa():
    resultado = calcular_largura_passagem(
        boca=20,
        velocidade_navio="baixa",
        canal_abrigado=True,
    )

    assert resultado == pytest.approx(20.0)


def test_calcular_largura_canal_mao_dupla():
    resultado = calcular_largura_canal_mao_dupla(
        largura_manobra=60.0,
        folga_margem_esquerda=10.0,
        folga_margem_direita=14.0,
        largura_passagem=28.0,
    )

    assert resultado == pytest.approx(172.0)


def test_largura_adicional_deriva_navio_convencional():
    resultado = calcular_largura_adicional_deriva(
        comprimento=200.0,
        raio_curva=1000.0,
    )

    assert resultado == pytest.approx(5.0)


def test_largura_adicional_deriva_navio_grande_deslocamento():
    resultado = calcular_largura_adicional_deriva(
        comprimento=200.0,
        raio_curva=1000.0,
        navio_grande_deslocamento=True,
    )

    assert resultado == pytest.approx(8.8888889)


def test_largura_adicional_tempo_resposta():
    resultado = calcular_largura_adicional_tempo_resposta(
        boca=20.0,
    )

    assert resultado == pytest.approx(8.0)


def test_largura_adicional_curva():
    resultado = calcular_largura_adicional_curva(
        largura_adicional_deriva=5.0,
        largura_adicional_tempo_resposta=8.0,
    )

    assert resultado == pytest.approx(13.0)


def test_largura_canal_curva():
    resultado = calcular_largura_canal_curva(
        largura_canal_reto=100.0,
        largura_adicional_curva=13.0,
    )

    assert resultado == pytest.approx(113.0)


def test_raio_recomendado_curva_por_tipo_navio():
    casos = {
        "carga": 5.0,
        "carga_pequeno": 6.0,
        "conteineiro_pos_panamax": 7.0,
        "conteineiro_panamax": 6.0,
        "graneleiro_muito_grande": 6.0,
        "graneleiro_panamax": 6.0,
        "graneleiro_pequeno": 5.0,
        "vlcc": 5.0,
        "petroleiro_pequeno": 5.0,
        "gnl": 4.0,
        "carga_refrigerada": 5.0,
        "passageiro": 4.0,
        "balsa": 5.0,
    }

    for tipo_navio, fator in casos.items():
        resultado = calcular_raio_recomendado_curva(
            comprimento=200.0,
            tipo_navio=tipo_navio,
        )

        assert resultado == pytest.approx(fator * 200.0)


def test_raio_minimo_curva_angulo_ate_25():
    resultado = calcular_raio_minimo_curva(
        comprimento=200.0,
        angulo_deflexao=20.0,
        tipo_navio="carga",
    )

    assert resultado == pytest.approx(600.0)


def test_raio_minimo_curva_angulo_maior_25():
    resultado = calcular_raio_minimo_curva(
        comprimento=200.0,
        angulo_deflexao=30.0,
        tipo_navio="carga",
    )

    assert resultado == pytest.approx(1000.0)


def test_raio_curva_atende_angulo_ate_25():
    resultado = verificar_raio_curva(
        raio_curva=601.0,
        comprimento=200.0,
        angulo_deflexao=20.0,
        tipo_navio="carga",
    )

    assert resultado is True


def test_raio_curva_nao_atende_igual_ao_minimo():
    resultado = verificar_raio_curva(
        raio_curva=600.0,
        comprimento=200.0,
        angulo_deflexao=20.0,
        tipo_navio="carga",
    )

    assert resultado is False


def test_raio_curva_atende_angulo_maior_25():
    resultado = verificar_raio_curva(
        raio_curva=1001.0,
        comprimento=200.0,
        angulo_deflexao=30.0,
        tipo_navio="carga",
    )

    assert resultado is True


def test_raio_curva_nao_atende_tabela():
    resultado = verificar_raio_curva(
        raio_curva=1000.0,
        comprimento=200.0,
        angulo_deflexao=30.0,
        tipo_navio="carga",
    )

    assert resultado is False
    