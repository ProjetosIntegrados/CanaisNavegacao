from canais_navegacao.hidrodinamica import (
    coeficiente_squat_icorels,
    numero_froude_profundidade,
    relacao_boca_calado,
    relacao_comprimento_boca,
    relacao_comprimento_calado,
    relacao_profundidade_calado,
    squat_icorels,
    verificar_validade_icorels,
    volume_deslocamento,
)


# Dados da embarcação
lpp = 200
boca = 30
calado = 10
cb = 0.75

# Condições de navegação
profundidade = 12
velocidade = 5


# Cálculo das relações geométricas
relacao_ht = relacao_profundidade_calado(profundidade, calado)
relacao_bt = relacao_boca_calado(boca, calado)
relacao_lb = relacao_comprimento_boca(lpp, boca)
relacao_lt = relacao_comprimento_calado(lpp, calado)

# Número de Froude de profundidade
froude = numero_froude_profundidade(velocidade, profundidade)


# Coeficiente Cs e volume de deslocamento
cs = coeficiente_squat_icorels(cb)

volume = volume_deslocamento(
    lpp=lpp,
    boca=boca,
    calado=calado,
    cb=cb,
)


# Verificação dos limites básicos de aplicação do ICORELS
valido = verificar_validade_icorels(
    relacao_ht=relacao_ht,
    relacao_bt=relacao_bt,
    relacao_lb=relacao_lb,
    relacao_lt=relacao_lt,
    cb=cb,
    froude_profundidade=froude,
)

# Cálculo do squat pelo método ICORELS
squat = squat_icorels(
    coeficiente_s=cs,
    volume_deslocamento=volume,
    lpp=lpp,
    froude_profundidade=froude,
)


print("Exemplo de cálculo do squat pelo método ICORELS")
print(f"h/T = {relacao_ht:.2f}")
print(f"B/T = {relacao_bt:.2f}")
print(f"L/B = {relacao_lb:.2f}")
print(f"L/T = {relacao_lt:.2f}")
print(f"Fn_h = {froude:.3f}")
print(f"Cs = {cs:.1f}")
print(f"Volume de deslocamento = {volume:.2f} m³")
print(f"Limites básicos atendidos: {valido}")
print(f"Squat ICORELS = {squat:.3f} m")