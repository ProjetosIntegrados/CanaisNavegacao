# CanaisNavegacao

> [!WARNING]
> Este projeto foi desenvolvido por estudantes no contexto de uma disciplina de graduação e possui finalidade exclusivamente educacional. Os resultados não foram necessariamente validados para uso profissional e devem ser utilizados com cautela e verificados independentemente.

## Descrição

O **CanaisNavegacao** é uma ferramenta computacional desenvolvida em Python para análise e pré-dimensionamento de canais de navegação em águas rasas.

O projeto busca determinar, para uma embarcação de projeto e determinadas condições de navegação, se a profundidade disponível é adequada e estimar a profundidade requerida para a navegação.

O desenvolvimento é realizado no contexto da disciplina **Projetos Integrados III**, do curso de Engenharia Civil da UFRGS.

## Fluxo de análise

A estrutura atual da ferramenta segue o fluxo:

**Embarcação + Canal → Parâmetros geométricos e hidrodinâmicos → Squat → FAQ → Profundidade requerida**

A profundidade requerida é determinada a partir da condição:

\[
f(h) = h - T - S_b(h) - MM_{min} = 0
\]

onde:

- \(h\) = profundidade do canal;
- \(T\) = calado da embarcação;
- \(S_b(h)\) = squat calculado para a profundidade analisada;
- \(MM_{min}\) = margem de manobrabilidade mínima adotada.

Como o squat depende da profundidade, a ferramenta recalcula o valor de \(S_b\) para cada profundidade candidata e utiliza o **método da bisseção** para determinar numericamente a profundidade requerida.

## Métodos de cálculo do squat

O *squat* representa o aumento do calado aparente da embarcação devido aos efeitos hidrodinâmicos associados ao seu movimento em águas rasas e/ou restritas.

A ferramenta possui atualmente três métodos empíricos para estimativa do squat: **ICORELS, Barrass 3 e Yoshimura**.

### Número de Froude de profundidade

O número de Froude baseado na profundidade é calculado por:

\[
Fn_h = \frac{V_S}{\sqrt{gh}}
\]

onde:

- \(V_S\) = velocidade da embarcação;
- \(g\) = aceleração da gravidade;
- \(h\) = profundidade da água.

Esse parâmetro permite caracterizar a relação entre a velocidade da embarcação e a profundidade disponível.

### Fator de bloqueio

Para canais com seção transversal definida, o fator de bloqueio é dado por:

\[
S = \frac{A_S}{A_C}
\]

onde:

- \(A_S\) = área da seção transversal imersa da embarcação;
- \(A_C\) = área da seção transversal do canal.

Para uma seção trapezoidal:

\[
A_C = Wh + nh^2
\]

e a largura no topo é:

\[
W_{TOP} = W + 2nh
\]

onde \(W\) é a largura de fundo do canal e \(n\) representa a inclinação horizontal/vertical do talude.

### ICORELS

O método ICORELS é implementado pela expressão:

\[
S_{bI} =
C_S
\frac{\nabla}{L_{pp}^2}
\frac{Fn_h^2}{\sqrt{1-Fn_h^2}}
\]

sendo o volume de deslocamento estimado por:

\[
\nabla = C_B L_{pp}BT
\]

onde:

- \(S_{bI}\) = squat estimado pelo método ICORELS;
- \(C_S\) = coeficiente do método;
- \(\nabla\) = volume de deslocamento;
- \(L_{pp}\) = comprimento entre perpendiculares;
- \(B\) = boca da embarcação;
- \(T\) = calado;
- \(C_B\) = coeficiente de bloco.

### Barrass 3

O método Barrass 3 é calculado por:

\[
S_{bB} = \frac{C_B V_k^2 K}{100}
\]

com:

\[
K = 5,74S^{0,76}
\]

onde:

- \(V_k\) = velocidade da embarcação em nós;
- \(S\) = fator de bloqueio;
- \(C_B\) = coeficiente de bloco.

### Yoshimura

O método de Yoshimura é implementado pela expressão:

\[
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
\]

A velocidade equivalente é definida conforme o tipo de canal:

\[
V_e = V_S
\qquad \text{para canal irrestrito (U)}
\]

e:

\[
V_e = \frac{V_S}{1-S}
\qquad \text{para canais restritos ou artificiais (R/C)}
\]

### Squat adotado

Quando mais de um método é aplicável às condições analisadas, a ferramenta calcula os valores correspondentes e adota, para esta análise preliminar, o maior resultado:

\[
S_{b,\mathrm{adotado}}
=
\max
\left(
S_{bI},
S_{bB},
S_{bY}
\right)_{\mathrm{métodos\ aplicáveis}}
\]

A adoção do maior valor entre os métodos aplicáveis constitui um **critério conservador definido para este projeto**, e não um fator de segurança prescrito pelas referências.

## Funcionalidades implementadas

Até a etapa atual do projeto foram implementados:

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

## Critério para o squat

Quando mais de um método empírico é aplicável às condições analisadas, são calculados os respectivos valores de squat.

Para a análise preliminar de navegabilidade, a ferramenta adota o **maior valor obtido entre os métodos aplicáveis**, constituindo um critério conservador adotado neste projeto.

Esse critério é uma escolha metodológica do projeto e não deve ser interpretado como um fator de segurança prescrito pelas referências utilizadas.

## Folga Abaixo da Quilha

De forma simplificada, a Folga Abaixo da Quilha utilizada nesta etapa do projeto é calculada por:

\[
FAQ = h - T - S_b
\]

A margem mínima considerada é:

\[
MM_{min} = \max(0,05T;\ 0,60\,m)
\]

A formulação utilizada nesta etapa constitui uma simplificação acadêmica do problema de navegabilidade, não abrangendo todos os componentes que podem participar de uma análise operacional completa da folga abaixo da quilha.

## Próximas etapas

As próximas etapas previstas para o desenvolvimento são:

**Profundidade requerida → Diferença de profundidade → Área de dragagem → Volume de dragagem**

A análise deverá posteriormente ser realizada por trechos do canal entre estacas consecutivas, permitindo identificar os segmentos críticos e estimar o volume de dragagem necessário.

Também está prevista a representação gráfica dos resultados, incluindo seções transversais, perfil longitudinal e evolução dos parâmetros ao longo do canal.

## Instalação

O projeto utiliza Python e Poetry para gerenciamento do ambiente e das dependências.

```bash
poetry install