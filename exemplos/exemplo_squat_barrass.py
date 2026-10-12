from canais_navegacao.hidrodinamica import (
    relacao_profundidade_calado,
    area_secao_canal,
    fator_bloqueio,
    squat_barrass3,
    verificar_validade_barrass3,
)


# Dados de entrada
profundidade = 12
calado = 10
largura_canal = 100
area_navio = 120
cb = 0.75
velocidade_nos = 10

# Cálculo dos parâmetros
relacao_ht = relacao_profundidade_calado(
    profundidade=profundidade,
    calado=calado,
)

area_canal = area_secao_canal(
    largura=largura_canal,
    profundidade=profundidade,
)

bloqueio = fator_bloqueio(
    area_navio=area_navio,
    area_canal=area_canal,
)

valido = verificar_validade_barrass3(
    relacao_ht=relacao_ht,
    bloqueio=bloqueio,
    cb=cb,
)

if valido:
    squat = squat_barrass3(
        velocidade_nos=velocidade_nos,
        cb=cb,
        bloqueio=bloqueio,
    )
print(f"Relação h/T: {relacao_ht:.2f}")
print(f"Área da seção do canal: {area_canal:.2f} m²")
print(f"Fator de bloqueio: {bloqueio:.3f}")
print(f"Método Barrass3 válido: {valido}")

if valido:
    print(f"Squat máximo: {squat:.3f} m")
else:
    print("Parâmetros fora dos limites de validade do método Barrass3.")