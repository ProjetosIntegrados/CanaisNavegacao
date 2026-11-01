from canais_navegacao.canal import Canal
from canais_navegacao.embarcacao import Embarcacao
from canais_navegacao.hidrodinamica import (
    calcular_squat_na_profundidade,
    folga_abaixo_quilha,
    margem_manobrabilidade_minima,
    profundidade_requerida_bissecao,
)
from canais_navegacao.dimensionamento_horizontal import (
    calcular_fator_auxilios_navegacao,
    calcular_fator_carga_perigosa,
    calcular_fator_corrente_longitudinal,
    calcular_fator_corrente_transversal,
    calcular_fator_intensidade_trafego,
    calcular_fator_ondas,
    calcular_fator_profundidade,
    calcular_fator_superficie_fundo,
    calcular_fator_velocidade,
    calcular_fator_vento_transversal,
    calcular_folga_margem,
    calcular_largura_canal_mao_unica,
    calcular_largura_manobra,
    calcular_largura_manobrabilidade_basica,
)
from canais_navegacao.batimetria import (
    PontoBatimetrico,
    SecaoBatimetrica,
    analisar_canal_vertical,
)
from canais_navegacao.diagnostico import diagnosticar_canal

from canais_navegacao.visualizacao import (
    plotar_secao_transversal,
    plotar_perfil_longitudinal,
    plotar_volumes_dragagem,
)


# ============================================================
# DADOS DE ENTRADA
# ============================================================

embarcacao = Embarcacao(
    lpp=200.0,
    boca=30.0,
    calado=10.0,
    cb=0.75,
)

canal = Canal(
    profundidade=12.0,
    comprimento=1000.0,
    tipo="U",
)

area_navio = 120.0

velocidade_ms = 5.0
velocidade_nos = velocidade_ms * 1.94384


# ============================================================
# DIMENSIONAMENTO VERTICAL
# ============================================================

metodo_squat, squat = calcular_squat_na_profundidade(
    profundidade=canal.profundidade,
    embarcacao=embarcacao,
    canal=canal,
    area_navio=area_navio,
    velocidade_ms=velocidade_ms,
    velocidade_nos=velocidade_nos,
)

faq = folga_abaixo_quilha(
    profundidade=canal.profundidade,
    calado=embarcacao.calado,
    squat=squat,
)

margem_minima = margem_manobrabilidade_minima(
    embarcacao.calado,
)

profundidade_requerida = profundidade_requerida_bissecao(
    profundidade_inferior=11.0,
    profundidade_superior=12.0,
    embarcacao=embarcacao,
    canal=canal,
    area_navio=area_navio,
    velocidade_ms=velocidade_ms,
    velocidade_nos=velocidade_nos,
)


# ============================================================
# DIMENSIONAMENTO HORIZONTAL
# ============================================================

wbm = calcular_largura_manobrabilidade_basica(
    boca=embarcacao.boca,
    manobrabilidade="boa",
)

w1 = calcular_fator_velocidade(
    boca=embarcacao.boca,
    velocidade=velocidade_nos,
)

w2 = calcular_fator_vento_transversal(
    boca=embarcacao.boca,
    velocidade_vento=15.0,
    velocidade_navio="moderada",
)

w3 = calcular_fator_corrente_transversal(
    boca=embarcacao.boca,
    velocidade_corrente=0.3,
    velocidade_navio="moderada",
    canal_abrigado=True,
)

w4 = calcular_fator_corrente_longitudinal(
    boca=embarcacao.boca,
    velocidade_corrente=1.0,
    velocidade_navio="moderada",
)

w5 = calcular_fator_ondas(
    boca=embarcacao.boca,
    altura_significativa=0.5,
    canal_abrigado=True,
)

w6 = calcular_fator_auxilios_navegacao(
    boca=embarcacao.boca,
    classificacao="bom",
)

w7 = calcular_fator_superficie_fundo(
    boca=embarcacao.boca,
    profundidade=canal.profundidade,
    calado=embarcacao.calado,
    tipo_fundo="liso_mole",
)

w8 = calcular_fator_profundidade(
    boca=embarcacao.boca,
    profundidade=canal.profundidade,
    calado=embarcacao.calado,
    canal_abrigado=True,
)

w9 = calcular_fator_carga_perigosa()

w10 = calcular_fator_intensidade_trafego(
    boca=embarcacao.boca,
    intensidade="media",
)

fatores = [
    w1,
    w2,
    w3,
    w4,
    w5,
    w6,
    w7,
    w8,
    w9,
    w10,
]

largura_manobra = calcular_largura_manobra(
    wbm=wbm,
    fatores=fatores,
)

folga_esquerda = calcular_folga_margem(
    boca=embarcacao.boca,
    tipo_margem="inclinada_suave",
    velocidade_navio="moderada",
)

folga_direita = calcular_folga_margem(
    boca=embarcacao.boca,
    tipo_margem="inclinada_suave",
    velocidade_navio="moderada",
)

largura_requerida = calcular_largura_canal_mao_unica(
    largura_manobra=largura_manobra,
    folga_margem_esquerda=folga_esquerda,
    folga_margem_direita=folga_direita,
)

# ============================================================
# SEÇÕES BATIMÉTRICAS
# ============================================================

secoes = [
    SecaoBatimetrica(
        identificacao="Estaca 0",
        distancia=0.0,
        pontos=[
            PontoBatimetrico(-50.0, 10.0),
            PontoBatimetrico(-40.0, 11.5),
            PontoBatimetrico(-30.0, 12.0),
            PontoBatimetrico(0.0, 12.5),
            PontoBatimetrico(30.0, 12.0),
            PontoBatimetrico(40.0, 11.5),
            PontoBatimetrico(50.0, 10.0),
        ],
        x=0.0,
        y=0.0,
    ),
    SecaoBatimetrica(
        identificacao="Estaca 1",
        distancia=250.0,
        pontos=[
            PontoBatimetrico(-50.0, 8.0),
            PontoBatimetrico(-40.0, 9.5),
            PontoBatimetrico(-30.0, 10.8),
            PontoBatimetrico(0.0, 11.5),
            PontoBatimetrico(30.0, 10.8),
            PontoBatimetrico(40.0, 9.5),
            PontoBatimetrico(50.0, 8.0),
        ],
        x=250.0,
        y=0.0,
    ),
    SecaoBatimetrica(
        identificacao="Estaca 2",
        distancia=500.0,
        pontos=[
            PontoBatimetrico(-50.0, 8.0),
            PontoBatimetrico(-40.0, 10.0),
            PontoBatimetrico(-30.0, 11.3),
            PontoBatimetrico(0.0, 11.8),
            PontoBatimetrico(30.0, 11.3),
            PontoBatimetrico(40.0, 10.0),
            PontoBatimetrico(50.0, 8.0),
        ],
        x=495.0,
        y=40.0,
    ),
    SecaoBatimetrica(
        identificacao="Estaca 3",
        distancia=750.0,
        pontos=[
            PontoBatimetrico(-50.0, 8.0),
            PontoBatimetrico(-40.0, 9.0),
            PontoBatimetrico(-30.0, 10.5),
            PontoBatimetrico(0.0, 11.0),
            PontoBatimetrico(30.0, 10.5),
            PontoBatimetrico(40.0, 9.0),
            PontoBatimetrico(50.0, 8.0),
        ],
        x=730.0,
        y=120.0,
    ),
    SecaoBatimetrica(
        identificacao="Estaca 4",
        distancia=1000.0,
        pontos=[
            PontoBatimetrico(-50.0, 8.0),
            PontoBatimetrico(-40.0, 10.0),
            PontoBatimetrico(-30.0, 11.5),
            PontoBatimetrico(0.0, 12.0),
            PontoBatimetrico(30.0, 11.5),
            PontoBatimetrico(40.0, 10.0),
            PontoBatimetrico(50.0, 8.0),
        ],
        x=950.0,
        y=235.0,
    ),
]


# ============================================================
# DIAGNÓSTICO INTEGRADO
# ============================================================

diagnostico = diagnosticar_canal(
    secoes=secoes,
    largura_requerida=largura_requerida,
    profundidade_requerida=profundidade_requerida,
)


# ============================================================
# ANÁLISE DE DRAGAGEM
# ============================================================

resultado_vertical = analisar_canal_vertical(
    secoes=secoes,
    largura=largura_requerida,
    profundidade_requerida=profundidade_requerida,
    talude=3.0,
)

resultados_secoes = resultado_vertical[0]
volumes_trechos = resultado_vertical[1]
trechos_dragagem = resultado_vertical[2]
secao_critica = resultado_vertical[3]
volume_total = resultado_vertical[4]

# ============================================================
# RESULTADOS PRELIMINARES
# ============================================================

print("\n=== ANÁLISE COMPLETA DO CANAL ===")

print("\nEmbarcação:")
print(f"Lpp: {embarcacao.lpp:.2f} m")
print(f"Boca: {embarcacao.boca:.2f} m")
print(f"Calado: {embarcacao.calado:.2f} m")
print(f"Cb: {embarcacao.cb:.2f}")

print("\nDimensionamento vertical:")
print(f"Método de squat: {metodo_squat}")
print(f"Squat: {squat:.3f} m")
print(f"FAQ na profundidade existente: {faq:.3f} m")
print(f"Margem mínima: {margem_minima:.3f} m")
print(f"Profundidade requerida: {profundidade_requerida:.3f} m")

print("\nDimensionamento horizontal:")
print(f"WBM: {wbm:.2f} m")
print(f"WM: {largura_manobra:.2f} m")
print(f"Folga margem esquerda: {folga_esquerda:.2f} m")
print(f"Folga margem direita: {folga_direita:.2f} m")
print(f"Largura requerida: {largura_requerida:.2f} m")

print("\nDiagnóstico das seções:")

for resultado in diagnostico:
    situacao = "ATENDE" if resultado[10] else "NÃO ATENDE"

    print(
        f"{resultado[0]} | "
        f"Prof. disp.: {resultado[2]:.2f} m | "
        f"Larg. disp.: {resultado[6]:.2f} m | "
        f"{situacao}"
    )

print("\nDragagem:")
print(f"Seção crítica: {secao_critica[0]}")
print(f"Trechos com necessidade de dragagem: {len(trechos_dragagem)}")
print(f"Volume total estimado: {volume_total:.2f} m³")


# ============================================================
# VISUALIZAÇÕES
# ============================================================

plotar_secao_transversal(
    secao=secoes[3],
    largura=largura_requerida,
    profundidade=profundidade_requerida,
    talude=3.0,
)

plotar_perfil_longitudinal(
    secoes=secoes,
    largura=largura_requerida,
    profundidade_requerida=profundidade_requerida,
)

plotar_volumes_dragagem(
    resultados_secoes=resultados_secoes,
)
