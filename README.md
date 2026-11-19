# CanaisNavegacao

> [!WARNING]
> Este projeto foi desenvolvido por estudantes no contexto de uma disciplina de graduação e possui finalidade exclusivamente educacional. Os resultados não foram necessariamente validados para uso profissional e devem ser utilizados com cautela e verificados independentemente.

## Descrição

O **CanaisNavegacao** é uma ferramenta computacional desenvolvida em Python para análise e pré-dimensionamento de canais de navegação em águas rasas.

O projeto estima a profundidade e a largura requeridas para uma embarcação de projeto, verifica a adequação das seções batimétricas e calcula áreas e volumes estimados de dragagem, com diagnóstico por estaca e representações gráficas.

O desenvolvimento é realizado no contexto da disciplina **Projetos Integrados III**, do curso de Engenharia Civil da UFRGS.

## Fluxo de análise

A estrutura atual da ferramenta segue o fluxo:

**Embarcação + canal → Dimensionamento vertical e horizontal → Análise batimétrica → Diagnóstico por estaca → Estimativa de dragagem → Visualização**

A profundidade requerida é determinada a partir da condição:

$$
f(h) = h - T - S_b(h) - MM_{min} = 0
$$

onde:

- $h$ = profundidade do canal;
- $T$ = calado da embarcação;
- $S_b(h)$ = squat calculado para a profundidade analisada;
- $MM_{min}$ = margem de manobrabilidade mínima adotada.

Como o squat depende da profundidade, a ferramenta recalcula o valor de $S_b$ para cada profundidade candidata e utiliza o **método da bisseção** para determinar numericamente a profundidade requerida.

## Métodos de cálculo do squat

O *squat* representa o aumento do calado aparente da embarcação devido aos efeitos hidrodinâmicos associados ao seu movimento em águas rasas e/ou restritas.

A ferramenta possui atualmente três métodos empíricos para estimativa do squat: **ICORELS, Barrass 3 e Yoshimura**.

### Número de Froude de profundidade

O número de Froude baseado na profundidade é calculado por:

$$
Fn_h = \frac{V_S}{\sqrt{gh}}
$$

onde:

- $V_S$ = velocidade da embarcação;
- $g$ = aceleração da gravidade;
- $h$ = profundidade da água.

Esse parâmetro permite caracterizar a relação entre a velocidade da embarcação e a profundidade disponível.

### Fator de bloqueio

Para canais com seção transversal definida, o fator de bloqueio é dado por:

$$
S = \frac{A_S}{A_C}
$$

onde:

- $A_S$ = área da seção transversal imersa da embarcação;
- $A_C$ = área da seção transversal do canal.

Para uma seção trapezoidal:

$$
A_C = Wh + nh^2
$$

e a largura no topo é:

$$
W_{TOP} = W + 2nh
$$

onde $W$ é a largura de fundo do canal e $n$ representa a inclinação horizontal/vertical do talude.

### ICORELS

O método ICORELS é implementado pela expressão:

$$
S_{bI} =
C_S
\frac{\nabla}{L_{pp}^2}
\frac{Fn_h^2}{\sqrt{1-Fn_h^2}}
$$

sendo o volume de deslocamento estimado por:

$$
\nabla = C_B L_{pp}BT
$$

onde:

- $S_{bI}$ = squat estimado pelo método ICORELS;
- $C_S$ = coeficiente do método;
- $\nabla$ = volume de deslocamento;
- $L_{pp}$ = comprimento entre perpendiculares;
- $B$ = boca da embarcação;
- $T$ = calado;
- $C_B$ = coeficiente de bloco.

### Barrass 3

O método Barrass 3 é calculado por:

$$
S_{bB} = \frac{C_B V_k^2 K}{100}
$$

com:

$$
K = 5,74S^{0,76}
$$

onde:

- $V_k$ = velocidade da embarcação em nós;
- $S$ = fator de bloqueio;
- $C_B$ = coeficiente de bloco.

### Yoshimura

O método de Yoshimura é implementado pela expressão:

$$
S_{bY} =
\left[
\left(
0,7+\frac{1,5}{h/T}
\right)
\left(
\frac{C_B}{L_{pp}/B}
\right)
+
\frac{15}{h/T}
\left(
\frac{C_B}{L_{pp}/B}
\right)^3
\right]
\frac{V_e^2}{g}
$$

A velocidade equivalente é definida conforme o tipo de canal:

$$
V_e = V_S
\qquad \text{para canal irrestrito (U)}
$$

e:

$$
V_e = \frac{V_S}{1-S}
\qquad \text{para canais restritos ou artificiais (R/C)}
$$

### Squat adotado

Quando mais de um método é aplicável às condições analisadas, a ferramenta calcula os valores correspondentes e adota, para esta análise preliminar, o maior resultado:

$$
S_{b,\mathrm{adotado}}
=
\max
\left(
S_{bI},
S_{bB},
S_{bY}
\right)_{\mathrm{métodos\ aplicáveis}}
$$

A adoção do maior valor entre os métodos aplicáveis constitui um **critério conservador definido para este projeto**, e não um fator de segurança prescrito pelas referências.

## Funcionalidades implementadas

A ferramenta implementa:

- representação dos dados básicos da embarcação;
- representação de canais irrestritos (U), restritos (R) e artificiais (C);
- relação profundidade/calado;
- relações geométricas da embarcação;
- área da seção transversal do canal;
- fator de bloqueio;
- número de Froude de profundidade;
- profundidade média do canal;
- velocidade crítica;
- largura efetiva para canal irrestrito;
- cálculo de squat pelo método ICORELS;
- cálculo de squat pelo método Barrass 3;
- cálculo de squat pelo método Yoshimura;
- seleção conservadora do maior squat entre os métodos aplicáveis;
- cálculo da Folga Abaixo da Quilha (FAQ);
- cálculo da margem de manobrabilidade mínima;
- verificação da adequação da FAQ;
- cálculo da profundidade requerida pelo método da bisseção.

## Dimensionamento horizontal

O módulo `dimensionamento_horizontal` calcula a largura básica de manobrabilidade (WBM), as parcelas adicionais relacionadas às condições de navegação, a largura de manobra (WM) e as folgas das margens. Considera fatores de velocidade, vento, correntes, ondas, auxílios à navegação, fundo, profundidade, carga perigosa e intensidade de tráfego.

Para canais de mão única, a largura requerida corresponde à soma da largura de manobra e das folgas das duas margens. O módulo também contém funções para canais de mão dupla, largura adicional em curvas e verificação de raios de curva. O exemplo integrado utiliza mão única em trecho reto.

## Batimetria, diagnóstico e dragagem

As seções transversais são representadas por `SecaoBatimetrica`, contendo identificação, distância longitudinal, pontos `PontoBatimetrico` (offset transversal e profundidade, em metros) e coordenadas locais opcionais. Os perfis são interpolados linearmente entre pontos consecutivos.

O programa verifica a profundidade disponível na faixa analisada e a largura navegável que contém o eixo, compara os resultados com as dimensões requeridas e identifica seções críticas. A seção de projeto possui fundo plano e taludes laterais. A área de dragagem é estimada pela diferença positiva entre os perfis de projeto e existente, dentro da cobertura batimétrica fornecida.

O volume entre seções consecutivas é calculado pelo método das áreas médias:

$$V_i = \frac{A_i+A_{i+1}}{2}\,\Delta x_i$$

O volume total é a soma dos volumes por trecho. São gerados gráficos de seção transversal, perfil longitudinal, volumes de dragagem e planta do canal.

## Folga Abaixo da Quilha

De forma simplificada, a Folga Abaixo da Quilha utilizada nesta etapa do projeto é calculada por:

$$
FAQ = h - T - S_b
$$

A margem mínima considerada é:

$$
MM_{min} = \max(0,05T;\ 0,60\,m)
$$

A formulação utilizada nesta etapa constitui uma simplificação acadêmica do problema de navegabilidade, não abrangendo todos os componentes que podem participar de uma análise operacional completa da folga abaixo da quilha.

## Estrutura do projeto

| Caminho | Conteúdo |
| --- | --- |
| `src/canais_navegacao/embarcacao.py` | Dados da embarcação |
| `src/canais_navegacao/canal.py` | Dados do canal |
| `src/canais_navegacao/hidrodinamica.py` | Squat, FAQ e dimensionamento vertical |
| `src/canais_navegacao/dimensionamento_horizontal.py` | Larguras e curvas |
| `src/canais_navegacao/batimetria.py` | Seções, déficits, áreas e volumes |
| `src/canais_navegacao/diagnostico.py` | Diagnóstico integrado |
| `src/canais_navegacao/visualizacao.py` | Representações gráficas |
| `exemplos/` | Exemplos executáveis |
| `tests/` | Testes automatizados |
| `pyproject.toml` e `poetry.lock` | Configuração e dependências |

## Instalação

Requisitos: Git, Python >= 3.11 e < 3.14 e Poetry. A biblioteca Matplotlib é instalada como dependência do projeto.

```bash
git clone https://github.com/ProjetosIntegrados/CanaisNavegacao.git
cd CanaisNavegacao
poetry install
```

## Exemplo completo

Execute na raiz do repositório:

```bash
poetry run python exemplos/exemplo_completo.py
```

O exemplo utiliza um cenário didático representativo do Canal dos Navegantes, com cinco seções espaçadas de 100 m, totalizando 400 m. As profundidades e a geometria são representativas, não constituem levantamento batimétrico oficial e não devem ser utilizadas para decisões operacionais. As embarcações são genéricas e a velocidade adotada é de aproximadamente 6 nós.

Para alternar entre os cenários, altere a variável `navio_exemplo` no início do arquivo:

```python
navio_exemplo = "gaseiro"
# ou: navio_exemplo = "graneleiro"
```

Resultados de referência obtidos com os exemplos:

| Parâmetro | Gaseiro | Graneleiro |
| --- | ---: | ---: |
| Lpp (m) | 90,00 | 167,00 |
| Boca (m) | 16,80 | 29,40 |
| Calado (m) | 5,00 | 9,92 |
| Squat (m) | 0,275 | 0,502 |
| FAQ (m) | 0,725 | -4,422 |
| Profundidade requerida (m) | 5,879 | 10,841 |
| Largura requerida (m) | 40,32 | 76,44 |
| Estacas que atendem | 1 de 5 | 0 de 5 |
| Volume estimado (m³) | 2.986,90 | 130.633,46 |

O programa apresenta resultados no terminal e abre gráficos com Matplotlib. Feche as janelas gráficas para concluir a execução. A pasta `exemplos/` contém ainda demonstrações individuais dos módulos.

## Testes automatizados

```bash
poetry run pytest
```

A versão de entrega contém 165 testes automatizados, abrangendo embarcação, canal, hidrodinâmica, dimensionamento horizontal, batimetria, diagnóstico e visualização. Os testes verificam o comportamento computacional, não constituindo validação operacional do método.

## Limitações e possibilidades de evolução

- Análise preliminar baseada em modelos empíricos e hipóteses simplificadas, sujeitas aos respectivos domínios de aplicação.
- A batimetria deve cobrir a seção de projeto para que a estimativa represente toda a área de intervenção; o exemplo não extrapola o levantamento além dos pontos fornecidos. No cenário do graneleiro, a largura requerida supera os 60 m de cobertura transversal, de modo que o volume é parcial em relação à seção completa de projeto.
- O exemplo não substitui levantamentos hidrográficos, análise de condições ambientais, simulação de manobras ou estudos de engenharia detalhados.
- Possíveis evoluções incluem importação de dados batimétricos e interface de usuário.

## Referência bibliográfica

- SANTOS, Edson Mesquita dos; SPHAIER, Sergio H.; CALIXTO, Mario; CAJATY, Marcelo (coord.). **Planejamento Portuário: Recomendações para Acessos Náuticos**. 2. ed. rev. e atual., 2026.

## Licença

Distribuído sob a licença [MIT](LICENSE).

Projeto acadêmico desenvolvido na disciplina Projetos Integrados III — Engenharia Civil, UFRGS, 2026/2.
