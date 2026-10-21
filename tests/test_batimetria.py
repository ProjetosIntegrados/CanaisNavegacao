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
    