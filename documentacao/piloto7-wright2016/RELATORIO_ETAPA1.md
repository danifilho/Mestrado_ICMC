# Piloto 7 — Etapa 1: mesmo desenho do Wright (2016), detectores atuais

Rodada corrigida (D9), concluída em 2026-11-18 às 23:10 EST.
- **Escopo:** 20 cenários × 100 repetições = 2.000 conjuntos de dados, todos completos em R e em Python.
- **Fila:** scavenger (não consome a cota).
- **Jobs:** R 21342976; Python 21351086.

## O que foi feito

### Dados
- **Treino:** exatamente os conjuntos da Etapa 0, gerados com o código original dos autores, n = 1000, 2 SNPs de interação, 5 marginais e 93 de ruído.
- **Cenários:** os 5 modelos plotados × as 4 combinações das Figuras 3 e 4, com mtry = 50.
- **Teste:** independente, com n = 1000, da mesma população (mesmas MAFs de ruído do treino) e semente própria.

### Detectores
Cada um produz um ranking nativo dos 21 pares formados pelos 7 SNPs não ruidosos:

| Detector | Configuração | Escore do par |
|---|---|---|
| EBM | interpret 0.7.8, padrões | importância do termo do par |
| H de Friedman | hstats, sobre um RF ranger | H² |
| SHAP | treeshap, sobre o mesmo RF | média de \|interação\| |
| RPF | randomPlantedForest, `max_interaction = 2` | variância do componente purificado |
| iRF / siRF | iRF 3.0.0 | estabilidade |
| NID | MLP [256, 128, 64] | escore dos pesos |
| IF | diversityForest, 500 árvores | EIM quantitativa e qualitativa |

O RSRF foi excluído e registrado, por falta de código público.

### Régua global
Usada em cada modelo de previsão (RF, IF, iRF, RPF, NID, EBM):
- I(A,B) = queda(A,B) − queda(A) − queda(B), calculada no teste com 30 permutações compartilhadas;
- métrica principal: log-loss; secundária: acurácia;
- ranking principal por |I| (convenção pré-fixada). As direções −I e I entram como sensibilidade.

### Referências do Wright
JVIMP (rfsrc 1.6.1, a versão que reproduz o artigo), JMST e PPI, calculadas nos mesmos dados de treino na Etapa 0.

Gini e permutação ficam fora das comparações de pares. São medidas de SNPs isolados: o posto é o máximo dos dois SNPs entre 100 variáveis, e não o posto do par entre 21. Estão nas tabelas, mas não são comparáveis.

### Métrica
- Média de P(posto do par verdadeiro ≤ k) para k = 1…10, entre os 21 pares.
- Acaso = 0,262.
- No modelo "Sem interação", o par não interage (os dois SNPs têm só efeitos marginais). Detecção acima do acaso ali significa que o detector ranqueia pela força marginal.

## Desempenho preditivo no teste (contexto)

| Modelo | log-loss | acurácia |
|---|---|---|
| RF | 0,657 | 0,610 |
| iRF | 0,658 | 0,608 |
| IF | 0,663 | 0,609 |
| NID | 0,680 | 0,579 |
| RPF | 0,685 | 0,616 |
| EBM | 0,819 | 0,588 |

O EBM tem a pior log-loss: probabilidades confiantes demais. Mesmo assim, tem acurácia comparável à dos outros modelos.

## Resultados de detecção (Fig. 1 e Fig. 2)

Média de P(posto ≤ k), k = 1…10. A coluna "4 com int." é a média dos quatro modelos com interação.

| Detector | Só int. | Modificador | Sinérgico | Redundante | 4 com int. | Sem interação (espúria) |
|---|---|---|---|---|---|---|
| **EBM (nativo)** | **0,66** | **0,66** | 0,67 | **0,60** | **0,65** | **0,27** |
| H de Friedman (nativo) | 0,45 | 0,43 | 0,64 | 0,53 | 0,51 | 0,36 |
| RPF (nativo) | 0,40 | 0,60 | 0,66 | 0,32 | 0,50 | 0,32 |
| Régua · RF, \|I\| | 0,37 | 0,52 | 0,63 | 0,35 | 0,47 | 0,38 |
| Régua · EBM, \|I\| | 0,49 | 0,44 | 0,52 | 0,41 | 0,47 | 0,34 |
| SHAP (nativo) | 0,32 | 0,53 | 0,66 | 0,28 | 0,45 | 0,41 |
| JVIMP (Wright) | 0,31 | 0,46 | 0,58 | 0,28 | 0,40 | 0,34 |
| JMST (Wright) | 0,16 | 0,45 | 0,67 | 0,20 | 0,37 | 0,47 |
| siRF (nativo) | 0,15 | 0,42 | 0,63 | 0,20 | 0,35 | 0,44 |
| PPI (Wright) | 0,11 | 0,44 | 0,66 | 0,16 | 0,34 | 0,45 |
| iRF (nativo) | 0,16 | 0,41 | 0,59 | 0,18 | 0,34 | 0,43 |
| NID (nativo) | 0,08 | 0,32 | 0,61 | 0,14 | 0,29 | 0,41 |
| IF, EIM quantitativa (nativo) | 0,20 | 0,23 | 0,35 | 0,21 | 0,25 | 0,29 |
| IF, EIM qualitativa (nativo) | 0,22 | 0,19 | 0,17 | 0,37 | 0,24 | 0,27 |

As tabelas completas estão em `resultados/tabelas/etapa1_*` (todas as direções da régua, log-loss e acurácia, curvas por cenário).

## Leitura

1. **O padrão do Wright se repete com os detectores atuais.** O caso sinérgico é fácil para todos (0,59–0,67, exceto IF). "Só interação" e "Redundante" são difíceis para os detectores baseados em florestas e na rede (iRF, siRF, NID, JMST, PPI: 0,08–0,20, abaixo ou perto do acaso).

   Esses mesmos detectores ranqueiam o par em cerca de 0,41–0,47 no modelo "Sem interação". Ou seja, eles acompanham a força marginal dos dois SNPs, e não a interação. É a mesma conclusão do Wright, agora estendida ao iRF, siRF e NID.

2. **O EBM é a exceção clara.** Tem a maior detecção nos quatro modelos com interação (0,60–0,67) e fica no nível do acaso em "Sem interação" (0,27). É o único detector com sinal alto e quase nenhuma detecção espúria (Fig. 2, canto superior esquerdo).

   Uma explicação plausível, não testada aqui: o EBM ajusta primeiro os efeitos principais e só depois procura pares nos resíduos. Com isso, o efeito marginal não "vaza" para o escore do par.

3. **H e RPF ficam em posição intermediária.** Detectam razoavelmente (0,50–0,51), com pouca detecção espúria (0,32–0,36). O SHAP de interação usa o mesmo RF que o H, mas é mais contaminado pela força marginal (0,41 em "Sem interação").

4. **A régua global, com |I| em log-loss, iguala os modelos baseados em florestas.**
   - RF, iRF, IF e EBM ficam todos em cerca de 0,46–0,47 nos modelos com interação e 0,33–0,41 em "Sem interação".
   - Ela melhora muito o iRF, o siRF e o IF em relação aos escores nativos deles (0,34 e 0,25 → 0,46–0,47). Supera a JVIMP, a JMST e a PPI do Wright.
   - Mas não alcança o EBM nativo.
   - A régua no NID e no RPF é mais fraca (0,33–0,35).
   - Ou seja, a régua é estável entre modelos, como o orientador queria, mas o que ela mede depende do modelo de previsão por baixo.

5. **Sensibilidade da direção da régua.**
   - **−I:** ranqueia melhor (RF 0,55 com interação e 0,30 sem; EBM 0,52 e 0,27). Isso é coerente com o teste sintético: interação em log-loss dá I < 0.
   - **|I|:** é a convenção principal pré-fixada e fica como resultado principal.
   - **I:** é quase sempre pior que o acaso (0,08–0,13 nos modelos com interação).

6. **IF ficou no nível do acaso em tudo** (EIM quantitativa e qualitativa, 0,24–0,29). Isso não deve ser lido como fraqueza do método sem verificação:
   - o protocolo fixou 500 árvores para todos;
   - o padrão do `interactionfor` para calcular a EIM é 20.000 árvores (2.000 sem importância);
   - com 500 árvores, a EIM tende a ser muito ruidosa.

   A régua aplicada à mesma floresta IF chega a 0,46, então a floresta em si aprende o sinal. Uma sensibilidade com o padrão do pacote (20.000 árvores) esclareceria isso. Não foi rodada.

7. **Concordância entre detectores é baixa a moderada** (Fig. 4, τ de Kendall médio sobre os 21 pares):
   - iRF × siRF: 0,69;
   - H × SHAP: 0,62 (mesmo RF);
   - EBM concorda pouco com os outros: 0,10–0,35;
   - IF não concorda com ninguém: ≤ 0,17.

   Entre as réguas de modelos diferentes, τ = 0,12–0,50 (RF × iRF = 0,50). A mesma régua aplicada a modelos diferentes não produz o mesmo ranking.

## Limitações

- **Escopo:** só mtry = 50 e os 20 cenários do subconjunto. A Etapa 0 completa (mtry 10 e 50, 72 desenhos) está rodando; a Etapa 1 não foi estendida a ela.
- **Hiperparâmetros:** padrões de cada pacote com 500 árvores, sem ajuste. Isso afeta especialmente a EIM do IF (ver o item 6 da Leitura).
- **Escore do EBM:** é 0 para pares não selecionados. Há empates no fim do ranking, resolvidos pela média dos postos.
- **Incerteza:** com 100 repetições por cenário, o erro-padrão de cada ponto da curva é ≤ 0,05. As médias por modelo usam 400 repetições.
- **Incidentes:** a primeira rodada (v0) foi invalidada porque o teste vinha de outra população (D9). Está guardada como `*_v0_teste_outra_populacao`.

## Arquivos

- **Figuras:** `figuras/e1_fig1_mapa_deteccao`, `e1_fig2_sinal_vs_espurio`, `e1_fig3_curvas` e `e1_fig4_concordancia` (PNG e SVG). Os dados de cada figura estão em `figuras/dados/`.
- **Tabelas:** `resultados/tabelas/etapa1_*`.
- **Scripts:**
  - `src/etapa1.R` e `src/etapa1_py.py` (detectores e régua);
  - `scripts/05_analisar_etapa1.py` (análise);
  - `scripts/06_figuras_etapa1.py` (figuras).
