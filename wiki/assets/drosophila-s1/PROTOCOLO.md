# Protocolo — detectores de interação em dados de regulação gênica de *Drosophila* (v1)

**Congelamento prospectivo das análises restantes, gravado em 17/11/2026** (`configs/congelamento.json`, com hashes). Não se trata de um pré-registro anterior a qualquer contato com os dados (ver §1.3). Estudo exploratório de correspondência biológica: não é demonstração causal, validação biológica definitiva nem benchmark com gabarito completo.

## 1. Pergunta, fundamentação e histórico

### 1.1 Pergunta

> Aplicados aos mesmos dados de regulação gênica, diferentes detectores apontam relações semelhantes ou distintas, e em que medida essas relações correspondem a evidências biológicas conhecidas?

Ela se desdobra em três perguntas:
1. Os pares de fatores priorizados pelos detectores concordam entre si?
2. São estáveis sob reamostragem?
3. Têm suporte biológico documentado além do obtido por controles de importância individual e de correlação?

### 1.2 O que vem de cada fonte

| Componente | Origem | Situação |
|---|---|---|
| Dados, tarefa e configuração do iRF (n.iter = 5, B = 30, RIT com profundidade 5, 500 árvores, nchild 2, agrupamento de réplicas) | Basu et al. 2018, §4 e SI S3.1; `enhancer.R` (Zenodo) | **reproduzido** |
| Escore de estabilidade do iRF (fração de bootstraps em que o conjunto é recuperado) | Basu et al. 2018 | **reproduzido** (extrator nativo) |
| Lista de pares da Tabela S1 de Basu et al. e seus critérios ((i) um fator regula a expressão do outro; (ii) ligação conjunta associada a maior expressão) | Basu et al. 2018, SI S4 | **ponto de partida bibliográfico**; não é usado como gabarito |
| EIM quantitativa e qualitativa; floresta de profundidade restrita para a EIM com n > 1000 e floresta separada para a previsão | Hornung & Boulesteix 2022; `?interactionfor` (0.6.0) | **reproduzido** (implementação dos autores, padrões) |
| Avaliar rankings de pares pela precisão entre os mais bem ranqueados contra um padrão funcional, em comparação com a precisão de um ranking aleatório, e comparar a sobreposição dos pares do topo entre medidas | Deshpande, VanderSluis & Myers 2013 (medidas de similaridade de perfis de interação genética contra um padrão de coanotação GO, por precisão-revocação; sobreposição dos 1.000 pares mais similares entre medidas) | **adaptado**: aqui as listas são de pares de fatores, o corte é k pequeno e a referência é a tabela bibliográfica, não o GO |
| Partição agrupada, reamostragem de grupos, permutação por grupos, mapeamento para pares de genes, controles de grau, de importância individual e de correlação, categorias A–E e regras de ranking | — | **proposto por nós** (nenhum dos artigos fixa estas decisões) |

### 1.3 Histórico de exposição aos dados

- **Comparação anterior (16/11/2026, `comparacao_preditores_v1`):** só previsão, com AP de RF, IF e iRF nas partições oficial e agrupada. Interações não foram extraídas.
- **Conhecimento prévio:** a Tabela S1 e a Fig. 2 do artigo do iRF já eram conhecidas, com estabilidades para pares como Gt–Kr, Gt–Zld e Zld–Gt–Twi. Os artigos foram lidos nesta etapa.
- **Piloto técnico de 17/11/2026:** IF, iRF e RF numa reamostragem (r01). Foram lidos apenas custos e contagens (`info.json`); os rankings não foram abertos.
- **Ordem do trabalho:** a tabela de evidências foi construída e congelada (`evidencias/congelamento_evidencias.json`, 15:29 UTC) antes de qualquer ranking deste estudo.

## 2. Dados e tarefa

- **Fonte:** Zenodo 10.5281/zenodo.1401347, `iRF_analyses.zip` (md5 `651290c6…`). Arquivos usados: `enhancer.Rdata` e `irfSuppData1.csv`. A auditoria está em `resultados/auditoria/auditoria_dados.json`.
- **Linha:** uma região genômica de *D. melanogaster*, com 117 a 4.566 pb e coordenadas r6; a maioria são Vienna Tiles.
- **Desfecho:** 1 = a região dirige expressão com padrão no blastoderma (estágio 5) em ensaio de reporter transgênico. São 694 positivos em 7.809 regiões.
- **Preditores:** 80, todos usados no ajuste. Cada valor é o máximo do enriquecimento normalizado de ChIP na região:
  - histonas: colunas 1–38 e 43–45;
  - controles input: colunas 39–42;
  - **35 colunas de fatores de transcrição** (46–80), correspondentes a **23 fatores** (réplicas agrupadas por `Predictor_collapsed`).
- **Avaliação bibliográfica:** feita só em pares de fatores (253 pares). As interações com histonas e input são relatadas à parte, de forma descritiva.
- **Seleção de variáveis:** nenhuma, por associação com o desfecho.

## 3. Partição e vazamento

- **Grupos:** componentes conexos de sobreposição genômica, mesmo id ou atributos idênticos. São 4.086 grupos; na partição oficial, 1.165 deles (4.216 linhas) ficam dos dois lados.
- **Partição principal:** `StratifiedGroupKFold(5, shuffle, 2026)`. Os folds 0–2 formam o treino (4.658 linhas, 416 positivos), o fold 3 a validação (1.545, 127) e o fold 4 o teste (1.606, 151). Nenhum grupo é dividido.
- **Uso da validação:** só para a importância por permutação do RF (controle de importância individual). Não há ajuste de hiperparâmetros.
- **Pré-processamento:** nenhum é aprendido (nenhuma transformação, nenhum ausente).
- **Análise secundária:** a partição oficial dos autores, chamada de reprodução, que inclui o vazamento por sobreposição.

## 4. Referência biológica (congelada antes dos rankings)

Detalhes em `scripts/03_evidencias_busca.py`, `04a`, `04b` e `evidencias/`.

**Universo:** 253 pares de 23 fatores, com IDs NCBI e FlyBase em `configs/fatores.json`.

**Estratégia uniforme para todos os pares:**
1. **BioGRID 5.0.263:** interações físicas e genéticas entre os dois genes.
2. **PubMed:** (nomes e sinônimos de A) AND (nomes e sinônimos de B) AND Drosophila, em título e resumo; todos os resumos retornados foram baixados.
3. **Frases com os dois fatores:** identificadas por padrões fixos.
4. **Revisão manual:** até 3 frases por par, escolhidas por uma regra fixa de prioridade (no máximo uma por artigo), lidas e classificadas.

**Categorias:** A, X (regulação cruzada, subcategoria registrada à parte), B, C, Cneg, D, E e N/P, como definidas em `04b_evidencias_tabela.py`.

**Suporte principal:** categoria A, isto é, regulação conjunta de um alvo comum ou dependência funcional no embrião inicial, com experimento. X, B, C e D são reportadas separadamente. Afirmações de revisões e do próprio artigo do iRF não contam como A.

**Cobertura e limites:**
- todos os 253 pares foram pesquisados com o mesmo procedimento;
- a classificação usa títulos e resumos, não o texto completo, e só frases que mencionam os dois fatores;
- 37 pares têm artigos em que os dois fatores aparecem, mas nunca na mesma frase; esses pares ficam E;
- com o limite de 3 frases, pares muito estudados podem ter categorias mais fortes não lidas;
- **E significa "nenhuma evidência localizada por esta busca"**, não ausência de relação;
- os pares da Tabela S1 do iRF entram na tabela só se recuperados pela busca uniforme. A citação do suplemento fica numa coluna informativa e não conta como suporte.

**Taxa-base:** 45 dos 253 pares têm A (17,8%).

## 5. Métodos

Configurações em `configs/metodos.json`; não há busca de hiperparâmetros.

- **IF** (diversityForest 0.6.0, `interactionfor`, padrões):
  - `importance = "both"`, `probability = TRUE`;
  - com n > 1000, a EIM vem de uma floresta de 20.000 árvores com profundidade 7 (2000 < n ≤ 5000) e a previsão de uma floresta de 2.000 árvores completas, ambas do pacote;
  - todos os 3.160 pares são avaliados (p = 80 ≤ 100);
  - EIM quantitativa e qualitativa formam **rankings separados**.
- **iRF** (2.0.0, configuração de `enhancer.R`):
  - n.iter = 5, 500 árvores por iteração, B = 30;
  - RIT com profundidade 5, 500 árvores e nchild 2;
  - `varnames.grp` agrupa réplicas;
  - a previsão vem da floresta da iteração 5;
  - conjuntos e estabilidades da iteração 5.
- **RF** (ranger 0.18.0): floresta de probabilidade com 500 árvores e padrões. É a referência preditiva e a base do controle de importância individual.
- **Orçamento:** os esforços não são iguais e não se igualou o número de árvores.
  - IF: 22.000 árvores e EIM sobre 3.160 pares.
  - iRF: 5 × 500 árvores + 30 × 500 árvores de bootstrap + RIT.
  - RF: 500 árvores.
  - Custos medidos no piloto (n = 3.693, 1 thread): IF 21 min, iRF 7 min, RF 3 min (dos quais 3 min são a importância por permutação).
- **RPF e RSRF:** não incluídos. O desfecho é binário, o RSRF 0.1.6 não implementa classificação, e a extração do RPF não foi definida para este caso.

## 6. Regras de ranking (pares de fatores)

- **Ordenação de todas as listas:** escore decrescente. Empates são desfeitos por sorteio com semente fixa (2026 + índice da lista), **nunca pela ordem alfabética**.
- **Empates na fronteira:** reporta-se o tamanho do grupo empatado e a faixa (mínimo–máximo) das métricas em 1.000 resoluções aleatórias do empate.
- **IF-quant e IF-qual:** pares de colunas de fatores **diferentes**. O escore do par de fatores é o **máximo** da EIM entre os pares de colunas desses dois fatores (réplicas). Todos os 253 pares têm escore.
- **iRF (principal):** só **conjuntos de exatamente 2 grupos retornados pelo extrator**, ambos fatores. prdBQ e prdFQ contam como prd (máximo). Pares não retornados ficam fora da lista, que **não é completada**.
  - Projeção de conjuntos de ordem maior em pares: **análise secundária**, com o máximo da estabilidade dos conjuntos que contêm o par.
  - Conjuntos de ordem superior e conjuntos com histonas: análise descritiva separada.
- **Controle de importância individual:**
  - a importância de cada fator é o máximo, entre suas colunas, da queda de AP na validação por permutação (média de 10 repetições);
  - os fatores recebem postos (1 = mais importante; empates sorteados);
  - escore do par = −(posto_i + posto_j).
- **Controle de correlação:** máximo do \|Spearman\| no treino entre colunas dos dois fatores.
- **Controle aleatório:** 10.000 listas de k pares sorteados entre os 253.
- **Controle de grau preservado:** para cada lista observada, 10.000 listas aleatórias com a **mesma frequência de participação de cada fator** que os k primeiros pares observados (trocas duplas de arestas no grafo completo de 23 fatores, sem repetir pares). Verifica se o suporte vem só de fatores muito estudados.

## 7. Execução

- **Treino completo:** sementes 2026, 2027 e 2028, para avaliar a variação pelo algoritmo.
- **Reamostragens:** R = 20 subamostras de 80% dos grupos do treino, sem reposição, para avaliar a variação pelos dados. São idênticas para os três métodos e usam a semente 2026.
- **Estabilidade interna do iRF:** o escore de estabilidade nativo (30 bootstraps).
- **Permutações:** 10 permutações do desfecho no treino, todas com IF, iRF e RF (as etapas supervisionadas aplicáveis), semente 2026.
  - **Unidade:** o vetor de rótulos de cada grupo é trocado com o de outro grupo de mesmo tamanho. Isso preserva a dependência entre regiões sobrepostas.
  - **Limitação:** tamanhos com um único grupo (por exemplo, 18) não são permutados.
- **Partição oficial:** os três métodos, semente 2026 (secundária).
- **Teto:** 40 CPU-h alocadas. Estimativa para o desenho completo: cerca de 20 CPU-h. Uma tarefa por elemento de array (1 CPU), com retomada por tarefa, logs e registro de falhas.

## 8. Análises predefinidas

- **k:** 10 é o corte principal; 5 e 20 são sensibilidades, quando houver candidatos suficientes.
- **Suporte:** fração dos k primeiros pares com A (principal), e separadamente com X, B, C, D e E.
  - Os k primeiros pares são escolhidos antes da consulta à evidência, sem pular pares sem suporte. Todos os pares são pesquisados, então o denominador é sempre k.
  - Comparações:
    - contra a taxa-base (probabilidade hipergeométrica descritiva);
    - contra o controle aleatório;
    - contra o controle de grau preservado (fração das listas com suporte ≥ ao observado);
    - contra os controles de importância individual e de correlação (diferença de frações).
- **Estabilidade:**
  - frequência de seleção de cada par entre os k primeiros nas 20 reamostragens;
  - Jaccard@k médio entre reamostragens e entre sementes.
- **Concordância:** Jaccard@k entre métodos, no treino completo (semente 2026) e por reamostragem, quando os métodos usam o mesmo subconjunto. Compara-se a estabilidade dentro de cada método com a concordância entre métodos.
- **Permutação:** suporte e número de candidatos sob a resposta permutada.
- **Previsão (complementar):** AP, ROC-AUC e Brier no teste agrupado, para as três sementes. Diferenças pareadas contra a RF, com bootstrap por grupo (2.000 reamostragens).
- **Multiplicidade:**
  - comparações principais: 3 listas de detectores × k = 10 × 4 referências;
  - todas as demais são sensibilidades descritivas;
  - nenhuma probabilidade é usada como teste confirmatório;
  - as reamostragens são sobrepostas e não são experimentos independentes.
- **Estudos de caso (regra congelada):**
  1. par **compartilhado e estável**: entre os 10 primeiros de pelo menos 2 das 3 listas de detectores no treino completo (semente 2026), com a maior frequência média de seleção nas reamostragens;
  2. par **exclusivo e estável**: entre os 10 primeiros de exatamente 1 lista, com frequência de seleção ≥ 0,5 nessa lista, o maior;
  3. par **sem suporte localizado** (E) entre os 10 primeiros de alguma lista, com a maior frequência de seleção.

  Se não existir, o caso não é forçado. Empate: maior soma de escores normalizados.
