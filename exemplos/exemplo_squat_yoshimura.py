from canais_navegacao.hidrodinamica import (
    relacao_profundidade_calado,
    relacao_comprimento_boca,
    velocidade_equivalente_yoshimura,
    squat_yoshimura,
)


# Dados da embarcação
lpp = 200
boca = 30
calado = 10
cb = 0.75

# Dados do canal e da navegação
profundidade = 12
tipo_canal = "U"
velocidade = 5  # m/s
bloqueio = 0.1

# Relações geométricas
relacao_ht = relacao_profundidade_calado(
    profundidade=profundidade,
    calado=calado,
)

relacao_lb = relacao_comprimento_boca(
    lpp=lpp,
    boca=boca,
)

# Velocidade equivalente
velocidade_equivalente = velocidade_equivalente_yoshimura(
    velocidade=velocidade,
    bloqueio=bloqueio,
    tipo_canal=tipo_canal,
)

# Squat pelo método de Yoshimura
squat = squat_yoshimura(
    relacao_ht=relacao_ht,
    relacao_lb=relacao_lb,
    cb=cb,
    velocidade_equivalente=velocidade_equivalente,
)

print("Exemplo de cálculo do squat pelo método de Yoshimura")
print(f"Tipo de canal = {tipo_canal}")
print(f"h/T = {relacao_ht:.2f}")
print(f"L/B = {relacao_lb:.2f}")
print(f"Velocidade do navio = {velocidade:.2f} m/s")
print(f"Velocidade equivalente = {velocidade_equivalente:.2f} m/s")
print(f"Squat Yoshimura = {squat:.3f} m")