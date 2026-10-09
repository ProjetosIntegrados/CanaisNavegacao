from canais_navegacao.hidrodinamica import (
    relacao_profundidade_calado,
    area_secao_canal,
    fator_bloqueio,
)


profundidade = 12
calado = 10
largura_canal = 100
area_navio = 120

relacao_ht = relacao_profundidade_calado(profundidade, calado)
area_canal = area_secao_canal(largura_canal, profundidade)
bloqueio = fator_bloqueio(area_navio, area_canal)

print(f"Relação h/T: {relacao_ht:.2f}")
print(f"Área da seção do canal: {area_canal:.2f} m²")
print(f"Fator de bloqueio: {bloqueio:.3f}")