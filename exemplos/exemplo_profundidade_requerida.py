from canais_navegacao.embarcacao import Embarcacao
from canais_navegacao.canal import Canal
from canais_navegacao.hidrodinamica import (
    calcular_squat_na_profundidade,
    folga_abaixo_quilha,
    margem_manobrabilidade_minima,
    profundidade_requerida_bissecao,
)
# Dados da embarcação
embarcacao = Embarcacao(
    lpp=200.0,
    boca=30.0,
    calado=10.0,
    cb=0.75,
)

# Dados do canal
canal = Canal(
    profundidade=12.0,
    comprimento=1000.0,
    tipo="U",
)

# Condições de navegação
area_navio = 120.0
velocidade_ms = 5.0
velocidade_nos = velocidade_ms * 1.94384
# Cálculo do squat na profundidade existente
metodo, squat = calcular_squat_na_profundidade(
    profundidade=canal.profundidade,
    embarcacao=embarcacao,
    canal=canal,
    area_navio=area_navio,
    velocidade_ms=velocidade_ms,
    velocidade_nos=velocidade_nos,
)

# Cálculo da FAQ
faq = folga_abaixo_quilha(
    profundidade=canal.profundidade,
    calado=embarcacao.calado,
    squat=squat,
)

# Margem mínima
margem_minima = margem_manobrabilidade_minima(
    embarcacao.calado,
)
# Cálculo da profundidade requerida
profundidade_requerida = profundidade_requerida_bissecao(
    profundidade_inferior=11.0,
    profundidade_superior=12.0,
    embarcacao=embarcacao,
    canal=canal,
    area_navio=area_navio,
    velocidade_ms=velocidade_ms,
    velocidade_nos=velocidade_nos,
)
# Verificação da condição de navegabilidade
canal_adequado = canal.profundidade >= profundidade_requerida
print("\n=== ANÁLISE DE NAVEGABILIDADE ===")

print("\nEmbarcação:")
print(f"Lpp: {embarcacao.lpp:.2f} m")
print(f"Boca: {embarcacao.boca:.2f} m")
print(f"Calado: {embarcacao.calado:.2f} m")
print(f"Coeficiente de bloco: {embarcacao.cb:.2f}")

print("\nCanal:")
print(f"Tipo: {canal.tipo}")
print(f"Profundidade existente: {canal.profundidade:.2f} m")

print("\nCondições de navegação:")
print(f"Velocidade: {velocidade_ms:.2f} m/s ({velocidade_nos:.2f} nós)")

print("\nResultados:")
print(f"Método controlador do squat: {metodo}")
print(f"Squat adotado: {squat:.3f} m")
print(f"FAQ disponível: {faq:.3f} m")
print(f"Margem mínima: {margem_minima:.3f} m")
print(f"Profundidade requerida: {profundidade_requerida:.3f} m")

if canal_adequado:
    print("\nSituação: CANAL ADEQUADO")
else:
    print("\nSituação: CANAL NECESSITA ADEQUAÇÃO")