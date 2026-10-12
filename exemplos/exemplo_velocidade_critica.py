from canais_navegacao.hidrodinamica import (
    area_secao_canal,
    largura_topo_canal,
    profundidade_media,
    fator_bloqueio,
    coeficiente_velocidade_critica,
    velocidade_critica,
)


# Dados do canal
largura = 80
profundidade = 11
talude = 3

# Área da seção transversal submersa da embarcação
area_navio = 124.3


# Cálculos da geometria do canal
area_canal = area_secao_canal(
    largura=largura,
    profundidade=profundidade,
    talude=talude,
)

largura_topo = largura_topo_canal(
    largura=largura,
    profundidade=profundidade,
    talude=talude,
)

h_media = profundidade_media(
    area_canal=area_canal,
    largura_topo=largura_topo,
)

# Fator de bloqueio
bloqueio = fator_bloqueio(
    area_navio=area_navio,
    area_canal=area_canal,
)

# Velocidade crítica
kc = coeficiente_velocidade_critica(
    bloqueio=bloqueio,
)

v_critica = velocidade_critica(
    coeficiente_critico=kc,
    profundidade_media=h_media,
)


print(f"Área da seção do canal: {area_canal:.2f} m²")
print(f"Largura no topo: {largura_topo:.2f} m")
print(f"Profundidade média: {h_media:.2f} m")
print(f"Fator de bloqueio: {bloqueio:.3f}")
print(f"Coeficiente de velocidade crítica: {kc:.3f}")
print(f"Velocidade crítica: {v_critica:.2f} m/s")