from canais_navegacao.hidrodinamica import numero_froude_profundidade


velocidade = 5
profundidade = 10

froude = numero_froude_profundidade(
    velocidade=velocidade,
    profundidade=profundidade,
)

print(f"Velocidade: {velocidade} m/s")
print(f"Profundidade: {profundidade} m")
print(f"Número de Froude de profundidade: {froude:.3f}")