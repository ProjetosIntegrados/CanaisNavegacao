import pytest

from canais_navegacao.batimetria import (
    PontoBatimetrico,
    SecaoBatimetrica,
    profundidade_secao_projeto,
    pontos_mudanca_secao_projeto,
    interpolar_profundidade,
    inserir_pontos_mudanca,
    encontrar_intersecao,
    area_dragagem_intervalo,
    calcular_area_dragagem_secao,
    calcular_volume_dragagem_entre_secoes,
    calcular_volume_total_dragagem,
    calcular_volumes_dragagem_por_trecho,
    identificar_trechos_dragagem,
    calcular_deficit_profundidade,
    ponto_dentro_largura_navegavel,
    calcular_profundidade_disponivel,
    analisar_secao_vertical,
    analisar_secoes_verticais,
    identificar_secao_critica,
    analisar_secao_vertical_completa,
    analisar_secoes_verticais_completas,
    analisar_canal_vertical,
    encontrar_offset_profundidade,
    encontrar_limite_esquerdo_navegavel,
    encontrar_limite_direito_navegavel,
    calcular_largura_disponivel,
    calcular_deficit_largura,
    analisar_secao_horizontal,
    analisar_secoes_horizontais,
    identificar_secao_critica_horizontal,

)

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


def test_secao_batimetrica_com_coordenadas():
    secao = SecaoBatimetrica(
        identificacao="Estaca 0",
        distancia=0.0,
        pontos=[
            PontoBatimetrico(-20.0, 10.0),
            PontoBatimetrico(0.0, 12.0),
            PontoBatimetrico(20.0, 10.0),
        ],
        x=1000.0,
        y=2000.0,
    )

    assert secao.x == pytest.approx(1000.0)
    assert secao.y == pytest.approx(2000.0)


def test_profundidade_secao_projeto_no_fundo():
    assert profundidade_secao_projeto(0, 20, 10, 2) == 10


def test_profundidade_secao_projeto_no_talude():
    assert profundidade_secao_projeto(20, 20, 10, 2) == 5


def test_profundidade_secao_projeto_fora_da_secao():
    assert profundidade_secao_projeto(40, 20, 10, 2) == 0


def test_profundidade_secao_projeto_offset_negativo():
    assert profundidade_secao_projeto(-20, 20, 10, 2) == 5 


def test_pontos_mudanca_secao_projeto():
    pontos = pontos_mudanca_secao_projeto(
        largura=20.0,
        profundidade=10.0,
        talude=2.0,
    )

    assert pontos == [-30.0, -10.0, 10.0, 30.0]     


def test_interpolar_profundidade():
    profundidade = interpolar_profundidade(
        offset=5,
        offset_inicial=0,
        profundidade_inicial=9,
        offset_final=10,
        profundidade_final=11,
    )

    assert profundidade == 10


def test_inserir_pontos_mudanca():
    pontos = [
        PontoBatimetrico(offset=0, profundidade=8),
        PontoBatimetrico(offset=20, profundidade=8),
    ]

    novos_pontos = inserir_pontos_mudanca(
        pontos=pontos,
        pontos_mudanca=[-30, -10, 10, 30],
    )

    assert len(novos_pontos) == 3
    assert novos_pontos[0].offset == 0
    assert novos_pontos[1].offset == 10
    assert novos_pontos[1].profundidade == 8
    assert novos_pontos[2].offset == 20    


def test_encontrar_intersecao():
    offset = encontrar_intersecao(
        offset_inicial=0,
        diferenca_inicial=1,
        offset_final=10,
        diferenca_final=-1,
    )

    assert offset == 5


def test_area_dragagem_intervalo_sem_dragagem():
    area = area_dragagem_intervalo(
        offset_inicial=0,
        diferenca_inicial=-1,
        offset_final=10,
        diferenca_final=-2,
    )

    assert area == 0


def test_area_dragagem_intervalo_completo():
    area = area_dragagem_intervalo(
        offset_inicial=0,
        diferenca_inicial=2,
        offset_final=10,
        diferenca_final=1,
    )

    assert area == 15


def test_area_dragagem_intervalo_com_intersecao():
    area = area_dragagem_intervalo(
        offset_inicial=0,
        diferenca_inicial=1,
        offset_final=10,
        diferenca_final=-1,
    )

    assert area == 2.5


def test_calcular_area_dragagem_secao():
    pontos = [
        PontoBatimetrico(offset=-30, profundidade=2),
        PontoBatimetrico(offset=-20, profundidade=5),
        PontoBatimetrico(offset=-10, profundidade=8),
        PontoBatimetrico(offset=0, profundidade=9),
        PontoBatimetrico(offset=10, profundidade=8),
        PontoBatimetrico(offset=20, profundidade=5),
        PontoBatimetrico(offset=30, profundidade=2),
    ]

    secao = SecaoBatimetrica(
        identificacao="Seção teste",
        distancia=0,
        pontos=pontos,
    )

    area = calcular_area_dragagem_secao(
        secao=secao,
        largura=20,
        profundidade=10,
        talude=2,
    )

    assert area == 50


def test_calcular_area_dragagem_secao_com_intersecao():
    pontos = [
        PontoBatimetrico(offset=0, profundidade=9),
        PontoBatimetrico(offset=10, profundidade=11),
    ]

    secao = SecaoBatimetrica(
        identificacao="Seção com interseção",
        distancia=0,
        pontos=pontos,
    )

    area = calcular_area_dragagem_secao(
        secao=secao,
        largura=20,
        profundidade=10,
        talude=2,
    )

    assert area == 2.5


def test_calcular_area_dragagem_secao_com_ponto_mudanca():
    pontos = [
        PontoBatimetrico(offset=0, profundidade=8),
        PontoBatimetrico(offset=20, profundidade=8),
    ]

    secao = SecaoBatimetrica(
        identificacao="Seção com ponto de mudança",
        distancia=0,
        pontos=pontos,
    )

    area = calcular_area_dragagem_secao(
        secao=secao,
        largura=20,
        profundidade=10,
        talude=2,
    )

    assert area == 24 


def test_volume_dragagem_entre_secoes_areas_iguais():
    volume = calcular_volume_dragagem_entre_secoes(
        area_inicial=50,
        area_final=50,
        distancia=100,
    )

    assert volume == 5000


def test_volume_dragagem_entre_secoes_areas_diferentes():
    volume = calcular_volume_dragagem_entre_secoes(
        area_inicial=50,
        area_final=70,
        distancia=100,
    )

    assert volume == 6000


def test_volume_dragagem_entre_secoes_sem_dragagem():
    volume = calcular_volume_dragagem_entre_secoes(
        area_inicial=0,
        area_final=0,
        distancia=100,
    )

    assert volume == 0


def test_volume_total_dragagem_multiplas_secoes():
    secoes = [
        (0, 50),
        (100, 70),
        (220, 40),
        (300, 0),
    ]

    volume_total = calcular_volume_total_dragagem(secoes)

    assert volume_total == 14200    


def test_volume_total_dragagem_com_trecho_sem_dragagem():
    secoes = [
        (0, 50),
        (100, 0),
        (200, 0),
    ]

    volume_total = calcular_volume_total_dragagem(secoes)

    assert volume_total == 2500
        

def test_volumes_dragagem_por_trecho():
    secoes = [
        (0, 50),
        (100, 70),
        (220, 40),
        (300, 0),
    ]

    resultados = calcular_volumes_dragagem_por_trecho(secoes)

    assert resultados == [
        (0, 100, 50, 70, 100, 6000),
        (100, 220, 70, 40, 120, 6600),
        (220, 300, 40, 0, 80, 1600),
    ]    


def test_volumes_dragagem_por_trecho_sem_dragagem():
    secoes = [
        (0, 50),
        (100, 0),
        (200, 0),
    ]

    resultados = calcular_volumes_dragagem_por_trecho(secoes)

    assert resultados == [
        (0, 100, 50, 0, 100, 2500),
        (100, 200, 0, 0, 100, 0),
    ]


def test_identificar_trechos_dragagem():
    resultados = [
        (0, 100, 50, 0, 100, 2500),
        (100, 200, 0, 0, 100, 0),
    ]

    trechos = identificar_trechos_dragagem(resultados)

    assert trechos == [
        (0, 100, True),
        (100, 200, False),
    ]


def test_calcular_deficit_profundidade_insuficiente():
    deficit = calcular_deficit_profundidade(
        profundidade_disponivel=8.5,
        profundidade_requerida=9.1,
    )

    assert deficit == pytest.approx(0.6)


def test_calcular_deficit_profundidade_adequada():
    deficit = calcular_deficit_profundidade(
        profundidade_disponivel=9.4,
        profundidade_requerida=9.1,
    )

    assert deficit == 0.0


def test_ponto_dentro_largura_navegavel():
    largura = 20.0

    assert ponto_dentro_largura_navegavel(0.0, largura) is True
    assert ponto_dentro_largura_navegavel(8.0, largura) is True
    assert ponto_dentro_largura_navegavel(10.0, largura) is True
    assert ponto_dentro_largura_navegavel(-10.0, largura) is True
    assert ponto_dentro_largura_navegavel(15.0, largura) is False
    assert ponto_dentro_largura_navegavel(-15.0, largura) is False


def test_calcular_profundidade_disponivel():
    secao = SecaoBatimetrica(
        identificacao="Estaca 0+100",
        distancia=100.0,
        pontos=[
            PontoBatimetrico(-15.0, 6.0),
            PontoBatimetrico(-10.0, 8.9),
            PontoBatimetrico(0.0, 8.5),
            PontoBatimetrico(10.0, 8.7),
            PontoBatimetrico(15.0, 6.2),
        ],
    )

    profundidade = calcular_profundidade_disponivel(
        secao=secao,
        largura=20.0,
    )

    assert profundidade == 8.5


def test_calcular_profundidade_disponivel_com_interpolacao():
    secao = SecaoBatimetrica(
        identificacao="Estaca 0+100",
        distancia=100.0,
        pontos=[
            PontoBatimetrico(-15.0, 7.0),
            PontoBatimetrico(-5.0, 9.0),
            PontoBatimetrico(5.0, 9.0),
            PontoBatimetrico(15.0, 8.0),
        ],
    )

    profundidade = calcular_profundidade_disponivel(
        secao=secao,
        largura=20.0,
    )

    assert profundidade == pytest.approx(8.0)


def test_analisar_secao_vertical_com_deficit():
    secao = SecaoBatimetrica(
        identificacao="Estaca 0+100",
        distancia=100.0,
        pontos=[
            PontoBatimetrico(-10.0, 8.9),
            PontoBatimetrico(0.0, 8.5),
            PontoBatimetrico(10.0, 8.7),
        ],
    )

    resultado = analisar_secao_vertical(
        secao=secao,
        largura=20.0,
        profundidade_requerida=9.1,
    )

    assert resultado[0] == "Estaca 0+100"
    assert resultado[1] == 100.0
    assert resultado[2] == 8.5
    assert resultado[3] == 9.1
    assert resultado[4] == pytest.approx(0.6)
    assert resultado[5] is True


def test_analisar_secao_vertical_adequada():
    secao = SecaoBatimetrica(
        identificacao="Estaca 0+200",
        distancia=200.0,
        pontos=[
            PontoBatimetrico(-10.0, 9.4),
            PontoBatimetrico(0.0, 9.6),
            PontoBatimetrico(10.0, 9.5),
        ],
    )

    resultado = analisar_secao_vertical(
        secao=secao,
        largura=20.0,
        profundidade_requerida=9.1,
    )

    assert resultado[2] == 9.4
    assert resultado[4] == 0.0
    assert resultado[5] is False


def test_analisar_secoes_verticais():
    secoes = [
        SecaoBatimetrica(
            identificacao="Estaca 0+000",
            distancia=0.0,
            pontos=[
                PontoBatimetrico(-10.0, 9.4),
                PontoBatimetrico(0.0, 9.6),
                PontoBatimetrico(10.0, 9.5),
            ],
        ),
        SecaoBatimetrica(
            identificacao="Estaca 0+100",
            distancia=100.0,
            pontos=[
                PontoBatimetrico(-10.0, 8.9),
                PontoBatimetrico(0.0, 8.7),
                PontoBatimetrico(10.0, 8.8),
            ],
        ),
        SecaoBatimetrica(
            identificacao="Estaca 0+220",
            distancia=220.0,
            pontos=[
                PontoBatimetrico(-10.0, 8.5),
                PontoBatimetrico(0.0, 8.3),
                PontoBatimetrico(10.0, 8.4),
            ],
        ),
    ]

    resultados = analisar_secoes_verticais(
        secoes=secoes,
        largura=20.0,
        profundidade_requerida=9.1,
    )

    assert len(resultados) == 3

    assert resultados[0][0] == "Estaca 0+000"
    assert resultados[0][2] == 9.4
    assert resultados[0][4] == 0.0
    assert resultados[0][5] is False

    assert resultados[1][0] == "Estaca 0+100"
    assert resultados[1][2] == 8.7
    assert resultados[1][4] == pytest.approx(0.4)
    assert resultados[1][5] is True

    assert resultados[2][0] == "Estaca 0+220"
    assert resultados[2][2] == 8.3
    assert resultados[2][4] == pytest.approx(0.8)
    assert resultados[2][5] is True


def test_identificar_secao_critica():
    resultados = [
        ("Estaca 0+000", 0.0, 9.4, 9.1, 0.0, False),
        ("Estaca 0+100", 100.0, 8.7, 9.1, 0.4, True),
        ("Estaca 0+220", 220.0, 8.3, 9.1, 0.8, True),
    ]

    secao_critica = identificar_secao_critica(resultados)

    assert secao_critica[0] == "Estaca 0+220"
    assert secao_critica[1] == 220.0
    assert secao_critica[2] == 8.3
    assert secao_critica[3] == 9.1
    assert secao_critica[4] == pytest.approx(0.8)
    assert secao_critica[5] is True


def test_analisar_secao_vertical_completa():
    secao = SecaoBatimetrica(
        identificacao="Estaca 0+100",
        distancia=100.0,
        pontos=[
            PontoBatimetrico(-20.0, 8.0),
            PontoBatimetrico(-10.0, 8.5),
            PontoBatimetrico(0.0, 8.5),
            PontoBatimetrico(10.0, 8.5),
            PontoBatimetrico(20.0, 8.0),
        ],
    )

    resultado = analisar_secao_vertical_completa(
        secao=secao,
        largura=20.0,
        profundidade_requerida=9.0,
        talude=2.0,
    )

    assert resultado[0] == "Estaca 0+100"
    assert resultado[1] == 100.0
    assert resultado[2] == 8.5
    assert resultado[3] == 9.0
    assert resultado[4] == pytest.approx(0.5)
    assert resultado[5] is True
    assert resultado[6] > 0.0


def test_analisar_secoes_verticais_completas():
    secoes = [
        SecaoBatimetrica(
            identificacao="Estaca 0+000",
            distancia=0.0,
            pontos=[
                PontoBatimetrico(-20.0, 9.5),
                PontoBatimetrico(-10.0, 9.4),
                PontoBatimetrico(0.0, 9.6),
                PontoBatimetrico(10.0, 9.5),
                PontoBatimetrico(20.0, 9.0),
            ],
        ),
        SecaoBatimetrica(
            identificacao="Estaca 0+100",
            distancia=100.0,
            pontos=[
                PontoBatimetrico(-20.0, 8.0),
                PontoBatimetrico(-10.0, 8.5),
                PontoBatimetrico(0.0, 8.5),
                PontoBatimetrico(10.0, 8.5),
                PontoBatimetrico(20.0, 8.0),
            ],
        ),
    ]

    resultados = analisar_secoes_verticais_completas(
        secoes=secoes,
        largura=20.0,
        profundidade_requerida=9.0,
        talude=2.0,
    )

    assert len(resultados) == 2

    assert resultados[0][0] == "Estaca 0+000"
    assert resultados[0][1] == 0.0
    assert resultados[0][4] == 0.0
    assert resultados[0][5] is False

    assert resultados[1][0] == "Estaca 0+100"
    assert resultados[1][1] == 100.0
    assert resultados[1][2] == 8.5
    assert resultados[1][4] == pytest.approx(0.5)
    assert resultados[1][5] is True
    assert resultados[1][6] > 0.0


def test_analisar_canal_vertical():
    secoes = [
        SecaoBatimetrica(
            "Estaca 0+000",
            0.0,
            [
                PontoBatimetrico(-20.0, 9.5),
                PontoBatimetrico(-10.0, 9.4),
                PontoBatimetrico(0.0, 9.6),
                PontoBatimetrico(10.0, 9.5),
                PontoBatimetrico(20.0, 9.0),
            ],
        ),
        SecaoBatimetrica(
            "Estaca 0+100",
            100.0,
            [
                PontoBatimetrico(-20.0, 8.0),
                PontoBatimetrico(-10.0, 8.5),
                PontoBatimetrico(0.0, 8.5),
                PontoBatimetrico(10.0, 8.5),
                PontoBatimetrico(20.0, 8.0),
            ],
        ),
    ]

    resultado = analisar_canal_vertical(
        secoes=secoes,
        largura=20.0,
        profundidade_requerida=9.0,
        talude=2.0,
    )

    resultados_secoes = resultado[0]
    volumes_trechos = resultado[1]
    trechos_dragagem = resultado[2]
    secao_critica = resultado[3]
    volume_total = resultado[4]

    assert len(resultados_secoes) == 2
    assert len(volumes_trechos) == 1
    assert len(trechos_dragagem) == 1
    assert secao_critica[0] == "Estaca 0+100"
    assert secao_critica[4] == pytest.approx(0.5)
    assert volume_total > 0.0


def test_encontrar_offset_profundidade():
    resultado = encontrar_offset_profundidade(
        offset_inicial=-40.0,
        profundidade_inicial=8.0,
        offset_final=-20.0,
        profundidade_final=11.0,
        profundidade_requerida=10.0,
    )

    assert resultado == pytest.approx(-26.6666667)


def test_encontrar_limite_esquerdo_navegavel():
    secao = SecaoBatimetrica(
        identificacao="Estaca 0",
        distancia=0.0,
        pontos=[
            PontoBatimetrico(-60.0, 4.0),
            PontoBatimetrico(-40.0, 8.0),
            PontoBatimetrico(-20.0, 11.0),
            PontoBatimetrico(0.0, 12.0),
            PontoBatimetrico(20.0, 11.0),
            PontoBatimetrico(40.0, 8.0),
            PontoBatimetrico(60.0, 4.0),
        ],
    )

    resultado = encontrar_limite_esquerdo_navegavel(
        secao=secao,
        profundidade_requerida=10.0,
    )

    assert resultado == pytest.approx(-26.6666667)


def test_encontrar_limite_direito_navegavel():
    secao = SecaoBatimetrica(
        identificacao="Estaca 0",
        distancia=0.0,
        pontos=[
            PontoBatimetrico(-60.0, 4.0),
            PontoBatimetrico(-40.0, 8.0),
            PontoBatimetrico(-20.0, 11.0),
            PontoBatimetrico(0.0, 12.0),
            PontoBatimetrico(20.0, 11.0),
            PontoBatimetrico(40.0, 8.0),
            PontoBatimetrico(60.0, 4.0),
        ],
    )

    resultado = encontrar_limite_direito_navegavel(
        secao=secao,
        profundidade_requerida=10.0,
    )

    assert resultado == pytest.approx(26.6666667)


def test_calcular_largura_disponivel():
    secao = SecaoBatimetrica(
        identificacao="Estaca 0",
        distancia=0.0,
        pontos=[
            PontoBatimetrico(-60.0, 4.0),
            PontoBatimetrico(-40.0, 8.0),
            PontoBatimetrico(-20.0, 11.0),
            PontoBatimetrico(0.0, 12.0),
            PontoBatimetrico(20.0, 11.0),
            PontoBatimetrico(40.0, 8.0),
            PontoBatimetrico(60.0, 4.0),
        ],
    )

    resultado = calcular_largura_disponivel(
        secao=secao,
        profundidade_requerida=10.0,
    )

    assert resultado == pytest.approx(53.3333333)


def test_calcular_deficit_largura():
    resultado = calcular_deficit_largura(
        largura_disponivel=90.0,
        largura_requerida=110.0,
    )

    assert resultado == pytest.approx(20.0)


def test_calcular_deficit_largura_sem_deficit():
    resultado = calcular_deficit_largura(
        largura_disponivel=120.0,
        largura_requerida=110.0,
    )

    assert resultado == pytest.approx(0.0)


def test_analisar_secao_horizontal():
    secao = SecaoBatimetrica(
        identificacao="Estaca 0",
        distancia=0.0,
        pontos=[
            PontoBatimetrico(-60.0, 4.0),
            PontoBatimetrico(-40.0, 8.0),
            PontoBatimetrico(-20.0, 11.0),
            PontoBatimetrico(0.0, 12.0),
            PontoBatimetrico(20.0, 11.0),
            PontoBatimetrico(40.0, 8.0),
            PontoBatimetrico(60.0, 4.0),
        ],
    )

    resultado = analisar_secao_horizontal(
        secao=secao,
        profundidade_requerida=10.0,
        largura_requerida=60.0,
    )

    assert resultado[0] == "Estaca 0"
    assert resultado[1] == pytest.approx(0.0)
    assert resultado[2] == pytest.approx(53.3333333)
    assert resultado[3] == pytest.approx(60.0)
    assert resultado[4] == pytest.approx(6.6666667)
    assert resultado[5] is False

def test_analisar_secao_horizontal_eixo_sem_profundidade_suficiente():
    secao = SecaoBatimetrica(
        identificacao="Estaca 0",
        distancia=0.0,
        pontos=[
            PontoBatimetrico(-40.0, 8.0),
            PontoBatimetrico(-20.0, 11.0),
            PontoBatimetrico(0.0, 8.0),
            PontoBatimetrico(20.0, 11.0),
            PontoBatimetrico(40.0, 8.0),
        ],
    )

    resultado = analisar_secao_horizontal(
        secao=secao,
        profundidade_requerida=10.0,
        largura_requerida=60.0,
    )

    assert resultado[0] == "Estaca 0"
    assert resultado[1] == pytest.approx(0.0)
    assert resultado[2] == pytest.approx(0.0)
    assert resultado[3] == pytest.approx(60.0)
    assert resultado[4] == pytest.approx(60.0)
    assert resultado[5] is False

def test_analisar_secoes_horizontais():
    secao_1 = SecaoBatimetrica(
        identificacao="Estaca 0",
        distancia=0.0,
        pontos=[
            PontoBatimetrico(-40.0, 8.0),
            PontoBatimetrico(-20.0, 11.0),
            PontoBatimetrico(0.0, 12.0),
            PontoBatimetrico(20.0, 11.0),
            PontoBatimetrico(40.0, 8.0),
        ],
    )

    secao_2 = SecaoBatimetrica(
        identificacao="Estaca 1",
        distancia=500.0,
        pontos=[
            PontoBatimetrico(-50.0, 8.0),
            PontoBatimetrico(-30.0, 11.0),
            PontoBatimetrico(0.0, 12.0),
            PontoBatimetrico(30.0, 11.0),
            PontoBatimetrico(50.0, 8.0),
        ],
    )

    resultados = analisar_secoes_horizontais(
        secoes=[secao_1, secao_2],
        profundidade_requerida=10.0,
        largura_requerida=60.0,
    )

    assert len(resultados) == 2

    assert resultados[0][0] == "Estaca 0"
    assert resultados[0][1] == pytest.approx(0.0)
    assert resultados[0][2] == pytest.approx(53.3333333)
    assert resultados[0][4] == pytest.approx(6.6666667)
    assert resultados[0][5] is False

    assert resultados[1][0] == "Estaca 1"
    assert resultados[1][1] == pytest.approx(500.0)
    assert resultados[1][2] == pytest.approx(73.3333333)
    assert resultados[1][4] == pytest.approx(0.0)
    assert resultados[1][5] is True


def test_identificar_secao_critica_horizontal():
    resultados = [
        ("Estaca 0", 0.0, 53.0, 60.0, 7.0, False),
        ("Estaca 1", 500.0, 45.0, 60.0, 15.0, False),
        ("Estaca 2", 1000.0, 70.0, 60.0, 0.0, True),
    ]

    resultado = identificar_secao_critica_horizontal(
        resultados=resultados,
    )

    assert resultado[0] == "Estaca 1"
    assert resultado[4] == pytest.approx(15.0)


def test_largura_disponivel_considera_faixa_contendo_eixo():
    secao = SecaoBatimetrica(
        identificacao="Estaca 0",
        distancia=0.0,
        pontos=[
            PontoBatimetrico(-80.0, 8.0),
            PontoBatimetrico(-60.0, 11.0),
            PontoBatimetrico(-40.0, 8.0),
            PontoBatimetrico(-20.0, 11.0),
            PontoBatimetrico(0.0, 12.0),
            PontoBatimetrico(20.0, 11.0),
            PontoBatimetrico(40.0, 8.0),
        ],
    )

    resultado = calcular_largura_disponivel(
        secao=secao,
        profundidade_requerida=10.0,
    )

    assert resultado == pytest.approx(53.3333333)


def test_largura_disponivel_eixo_sem_profundidade_suficiente():
    secao = SecaoBatimetrica(
        identificacao="Estaca 0",
        distancia=0.0,
        pontos=[
            PontoBatimetrico(-40.0, 8.0),
            PontoBatimetrico(-20.0, 11.0),
            PontoBatimetrico(0.0, 8.0),
            PontoBatimetrico(20.0, 11.0),
            PontoBatimetrico(40.0, 8.0),
        ],
    )

    with pytest.raises(ValueError):
        calcular_largura_disponivel(
            secao=secao,
            profundidade_requerida=10.0,
        )



def test_largura_disponivel_sem_ponto_exatamente_no_eixo():
    secao = SecaoBatimetrica(
        identificacao="Estaca 0",
        distancia=0.0,
        pontos=[
            PontoBatimetrico(-40.0, 8.0),
            PontoBatimetrico(-20.0, 11.0),
            PontoBatimetrico(10.0, 12.0),
            PontoBatimetrico(40.0, 8.0),
        ],
    )

    resultado = calcular_largura_disponivel(
        secao=secao,
        profundidade_requerida=10.0,
    )

    assert resultado == pytest.approx(51.6666667)
    
