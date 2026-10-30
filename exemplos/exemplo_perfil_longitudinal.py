from canais_navegacao.batimetria import (
    PontoBatimetrico,
    SecaoBatimetrica,
)
from canais_navegacao.visualizacao import plotar_perfil_longitudinal


secoes = [
    SecaoBatimetrica(
        identificacao="Estaca 0",
        distancia=0.0,
        pontos=[
            PontoBatimetrico(-30.0, 9.0),
            PontoBatimetrico(-20.0, 10.5),
            PontoBatimetrico(0.0, 12.0),
            PontoBatimetrico(20.0, 10.5),
            PontoBatimetrico(30.0, 9.0),
        ],
    ),
    SecaoBatimetrica(
        identificacao="Estaca 1",
        distancia=100.0,
        pontos=[
            PontoBatimetrico(-30.0, 8.0),
            PontoBatimetrico(-20.0, 9.5),
            PontoBatimetrico(0.0, 11.0),
            PontoBatimetrico(20.0, 9.5),
            PontoBatimetrico(30.0, 8.0),
        ],
    ),
    SecaoBatimetrica(
        identificacao="Estaca 2",
        distancia=200.0,
        pontos=[
            PontoBatimetrico(-30.0, 9.0),
            PontoBatimetrico(-20.0, 10.2),
            PontoBatimetrico(0.0, 11.5),
            PontoBatimetrico(20.0, 10.2),
            PontoBatimetrico(30.0, 9.0),
        ],
    ),
    SecaoBatimetrica(
        identificacao="Estaca 3",
        distancia=300.0,
        pontos=[
            PontoBatimetrico(-30.0, 7.5),
            PontoBatimetrico(-20.0, 9.0),
            PontoBatimetrico(0.0, 10.5),
            PontoBatimetrico(20.0, 9.0),
            PontoBatimetrico(30.0, 7.5),
        ],
    ),
    SecaoBatimetrica(
        identificacao="Estaca 4",
        distancia=400.0,
        pontos=[
            PontoBatimetrico(-30.0, 9.0),
            PontoBatimetrico(-20.0, 10.5),
            PontoBatimetrico(0.0, 12.0),
            PontoBatimetrico(20.0, 10.5),
            PontoBatimetrico(30.0, 9.0),
        ],
    ),
]


plotar_perfil_longitudinal(
    secoes=secoes,
    largura=40.0,
    profundidade_requerida=10.0,
)