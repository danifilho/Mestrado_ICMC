# Decisões — Piloto 7 (reprodução de Wright et al. 2016 e extensão)

## D0 (18/11/2026): protocolo recebido em rascunho, incompleto

- O protocolo foi colado pelo pesquisador em 18/11/2026 com a instrução "executar no HPCC". O texto recebido está em `PROTOCOLO.md`.
- **Status declarado no próprio texto:** rascunho para revisão (Daniel e Prof. Cerri), com a regra de que nada deve rodar antes do congelamento.
- **Texto truncado:** termina na seção 5.3. A Etapa 2 (P2: escala logit × probabilidade, log-loss × acurácia) não tem métodos no texto recebido.
- **Estudo anterior suspenso:** a pedido do pesquisador, o `medida_global_drosophila_splicing_v1` foi suspenso. Ficou só o piloto de ajuste do fold 1 no HPCC (jobs 21310231–21310232), sem análise.

## D1 (18/11/2026): diferenças entre o texto e o código de Wright et al., transcritas da seção 2.3 do protocolo; seguir o código

| Item | Texto do artigo | Código |
|---|---|---|
| Modelos | 5 | 6 (modifier_snp1, modifier_snp2) |
| Combinações de MAF | 4 | 3: (0,2; 0,2), (0,2; 0,4), (0,4; 0,2) |
| Cenários | 160 × 5 medidas | 72 desenhos × 2 mtry = 144 cenários, × 5 medidas |
| Proporção de casos | "aproximadamente igual" | β0 sem o termo de interação: de 0,34 a 0,57 |

Estes itens foram transcritos do protocolo e ainda **não foram conferidos** contra `problems.R`, porque o Arquivo adicional 3 não está disponível nesta máquina nem no HPCC.

## Verificação da simulação (seção 3.5), feita em 18/11/2026

Código: `scripts/00_verificar_simulacao.py`. Saída: `auditoria/verificacao_simulacao.json`.
- **β0 da Tabela 3:** −1,44.
- **Penetrâncias:** (0,0) 0,3526, (1,1) 0,4427, (2,1) 0,5366, (2,2) 0,7122, contra 0,35, 0,44, 0,54 e 0,72 no artigo.
  - Diferença máxima: 0,0078, na célula (2,2), dentro do critério de 0,01.
- **Proporção esperada de casos nos 72 desenhos:** de 0,335 a 0,570.
  - Coincide com a faixa de 0,34 a 0,57 do protocolo.
  - A definição exata de `modifier_snp1` ainda é **provisória**: modificador no SNP1, por simetria.
- **Pendente:** as Tabelas S1–S20 (Arquivo adicional 2) e a proporção simulada (±0,02).

## Respostas do pesquisador (18/11/2026)

- **Arquivos adicionais:** autorizado baixar.
- **Pacotes:** autorizado instalar do CRAN no HPCC.
- **Teto do Piloto 7:** 150 CPU-h.
- **Congelamento:** congelar o texto recebido e rodar a Etapa 0. A Etapa 2 fica para quando o texto completo chegar.

## D2 (18/11/2026): materiais baixados (`fontes/`)

| Arquivo | Bytes | sha256 | Conteúdo |
|---|---:|---|---|
| MOESM1_ESM.gz | 40.907 | `693284c8…58e9` | pacote ranger **0.1.6.33** (16/02/2015) com `importance = "pairwise"` (PPI) |
| MOESM2_ESM.pdf | 80.069 | `d1a81944…3c0c` | tabelas de penetrância S1–S20 |
| MOESM3_ESM.zip | 44.919 | `8ac2eb5e…0110` | código de reprodução (`replication/01…06`) |
| MOESM4_ESM.pdf | 1.894.245 | `6f50bc02…39ec` | Figuras S1–S110 |

## D3 (18/11/2026): conferências contra o código dos autores (`01_main_simulation`)

- **β0:** `bx = 2·β·(2·MAF² + 2·MAF·(1−MAF)) = 2·β·(2·MAF)`. Coincide com a fórmula do protocolo.
- **Modelos:** `modifier_snp1` = (c1 0, c2 β, c12 β), que é o "Modifier SNP" das figuras. `modifier_snp2` = (β, 0, β) **não é plotado** (excluído em `02_plot_main.R`). Correção da hipótese provisória do script 00, sem efeito na proporção de casos (os dois SNPs têm a mesma MAF).
- **Ruído:** MAF ~ `runif` e genótipos por `sample(c(0,1,2), prob = HW)`.
- **Captura:** individuais usam o maior posto dos dois SNPs entre os 100 (`rank(-imp)`, empates pela média). Pares usam o posto do par verdadeiro entre os 21 pares dos 7 SNPs não ruidosos (JMST: menor = interação).
- **Curvas** (`02_plot_main.R`): proporção com posto ≤ k; individuais com k ≥ 2, pares com k = 1..10.
- **Instâncias de dados:** no BatchExperiments, a instância depende do desenho e da repetição; todas as medidas e os dois mtry usam os mesmos dados de cada repetição.

## D4 (18/11/2026): gabarito numérico extraído do PDF vetorial, e não por leitura visual

- **Fonte:** `scripts/01_gabarito_pdf.py` lê as polilinhas do ggplot embutidas no Arquivo adicional 4 (Figuras S1–S48).
  - Parâmetros: lidos da legenda de cada figura.
  - Painéis: ordem do `facet_wrap`.
  - Medidas: pela cor da paleta Set1 do script dos autores.
- **Saída:** 5.760 pontos (48 figuras × 5 modelos × curvas). Figuras S1–S12 e S25–S36 têm mtry = 50; S13–S24 e S37–S48, mtry = 10.
- **Conversão para valores:**
  - y: conferido pelas linhas de grade, com erro ≤ 0,0001.
  - k: atribuído pela ordem dos pontos. Nos gráficos de pares, a posição x lida desvia até 0,13, porque o eixo usa expansão discreta. Isso não afeta os valores.
- **Imprecisão do gabarito:** só a da extração vetorial, desprezível diante do erro de Monte Carlo (EP ≤ 0,05).
- **Figuras 3 e 4 do artigo:** os parâmetros dos painéis foram inferidos do texto dos Resultados (PMC4815164), sem a legenda:
  - (a) base, com β_I = β_M = 0,4 e MAF_I = MAF_M = 0,2;
  - MAF_I = 0,4;
  - β_M = 0,8;
  - β_I = 0,8.
  - Esses quatro desenhos correspondem às Figuras S1, S2, S4 e S7 (individuais) e S25, S26, S28 e S31 (pares). O subconjunto da Etapa 0 é definido por eles.

## D5 (18/11/2026): execução da Etapa 0

- **Executor:** `src/etapa0.R` executa `problems.R`, `simulate_snps.R` e `algorithms.R` **sem modificação**, num array SLURM (`scripts/rodar_array.sb`), sem BatchExperiments.
- **Sementes:**
  - dados: 12345 + 1000·desenho + repetição;
  - cada medida: semente dos dados + 100·índice + mtry.
  - A reprodução numérica dos dados de 2016 (semente do registro do BatchExperiments e `RNGkind(sample.kind = "Rounding")`) é **secundária** e não foi tentada nesta rodada.
- **ranger:** Gini, permutação e PPI usam o **ranger 0.1.6.33 do Arquivo adicional 1**, como no artigo. randomForestSRC usa a versão atual do CRAN.
- **Critério 2** (ordens), operacionalizado antes dos resultados em `scripts/03_comparar_etapa0.py`. Só contam os casos em que a diferença publicada entre as médias das curvas passa de 0,10:
  - Gini × Permutação, por cenário e modelo;
  - Sem interação × Só interação, por cenário e medida de pares.

## Pendências (situação em 18/11, antes da Etapa 0)

1. **Arquivos adicionais 1–4 (Springer):**
   - o download automático foi negado pelo controle de permissões desta sessão;
   - é preciso autorização explícita ou que o pesquisador os coloque em `fontes/`.
2. **Pacotes de R no HPCC:** faltam randomForestSRC, BatchExperiments, BatchJobs, hstats, iml e treeshap no ambiente `preditores`.
   - Disponíveis: ranger 0.18.0, diversityForest 0.6.0, randomPlantedForest 0.2.1.9000, iRF 3.0.0 e 2.0.0 (biblioteca separada).
   - A instalação baixa pacotes do CRAN e precisa de autorização.
3. **Orçamento de CPU-h:** não definido para o Piloto 7.
4. **Congelamento:** o protocolo pede revisão por Daniel e pelo Prof. Cerri antes de `congelar.py`. Falta saber se a instrução "executar" substitui essa revisão.
5. **Etapa 2:** sem especificação no texto recebido.
6. **RSRF e NID:** o protocolo pede decisão antes do congelamento.
   - **RSRF:** o protocolo diz não haver código público, mas o pacote `simpleRSRF` 0.1.6 está no repositório rsrf-code-paper, já usado no projeto. Ele só faz **regressão**; classificação não está implementada.
   - **NID:** exige PyTorch, que não está no ambiente.

## D6 (18/11/2026): compatibilidade de versões (piloto de tempo, job 21314389)

No primeiro piloto, **todas** as medidas falharam por compatibilidade, e nenhum posto foi produzido:
- **ranger 0.1.6.33** (Arquivo adicional 1):
  - **problema:** `importance.ranger` é exportado, mas não registrado como método S3 (NAMESPACE de 2015). Desde o R 3.6, métodos não registrados de pacotes anexados não são achados, e `ranger::importance(rf)` falha.
  - **correção:** `registerS3method("importance", "ranger", ranger::importance.ranger)` no executor. Nenhum cálculo muda.
- **randomForestSRC 3.10.0:**
  - **problema:** não tem mais `find.interaction`. A busca no arquivo do CRAN mostrou que a **última versão com a função é a 3.4.1**; a 3.4.2 já não a tem.
  - **correção:** instalada a 3.4.1 em biblioteca separada (`p7_Rlib_rfsrc341`), usada para JVIMP e JMST.
  - **ressalva:** não é a versão de 2016, e mudanças internas desde então podem alterar as florestas (seção 2.2 do protocolo).
- **Funções de `algorithms.R`:** continuam inalteradas.
- **Piloto refeito:** depois das duas correções, com o executor e o script do array atualizados. O congelamento será refeito antes do subconjunto, registrando essas duas alterações.
- **Segundo piloto** (job 21314741): Gini, permutação, PPI e JVIMP sem NA. A **JMST deu posto NA em 11 de 20 casos**, sem erro.
  - **Causa** (diagnóstico em `logs/debug_jmst.R`, job 21315512): no randomForestSRC 3.4.1, `find.interaction` devolve a matriz **ordenada por importância** (`sorted = TRUE`). O `jmst_wrapper` monta o nome do par na ordem da matriz; quando interactionSNP2 vem antes de interactionSNP1, o nome "interactionSNP1:interactionSNP2" não existe.
  - **Correção:** o executor redefine `find.interaction(...)` com `sorted = FALSE`, de modo que a matriz siga a ordem de `xvar.names`. Como a JMST é a média das duas direções e a JVIMP usa |Difference| por par, nenhum valor muda.
- **Jobs cancelados (18/11):** os jobs restantes do estudo suspenso `medida_global` (21310232_7 e _9) foram cancelados, a pedido do pesquisador de focar no Piloto 7.
- **Terceiro piloto** (job 21315690): nenhum NA nas 5 medidas.
  - **Tempo por repetição:** mtry 50 ≈ 64 s (Gini 6, permutação 8, JMST 23, JVIMP 21, PPI 6); mtry 10 ≈ 59 s.
  - **Projeção:** subconjunto (20 cenários × 100 repetições) ≈ 36 CPU-h. Etapa 0 completa (72 desenhos × 2 mtry) ≈ 246 CPU-h, acima do teto de 150; mesmo sem o `modifier_snp2`, que não é plotado, ≈ 205 CPU-h. O escopo da etapa completa será decidido depois do subconjunto.
  - **Reaproveitamento:** as repetições 1 e 2 do desenho base, já calculadas pelo piloto com as mesmas sementes, entram no subconjunto.

## D7 (18/11/2026): resultado do subconjunto da Etapa 0 — a P0 NÃO passa pelo critério pré-fixado

**Execução:** job 21316012, 200/200 tarefas e 2.000 repetições (20 cenários × 100), 38,7 CPU-h. Fonte: `resultados/tabelas/etapa0_subconjunto_veredito.json`.
- **Critério 1:** 89,5 % dos 960 pontos com |nosso − publicado| ≤ 0,10, abaixo do mínimo de 90 %.
- **Critério 2:** 1 de 26 ordens invertida (JVIMP; Sem interação × Só interação no cenário MAF_I = 0,4).
- **Proporção de casos:** 20/20 desenhos dentro de ±0,02 da esperada. Na primeira comparação, os 4 desenhos do `modifier_snp1` apareciam sem valor esperado, por um erro de nome no script 00, corrigido.

**Por medida** (fração de pontos dentro de ±0,10; diferença média nosso − publicado):

| Medida | Dentro de ±0,10 | Diferença média |
|---|---:|---:|
| Gini | 0,978 | −0,003 |
| Permutação | 0,994 | −0,002 |
| JMST | 0,980 | 0,000 |
| PPI | 0,975 | −0,001 |
| JVIMP | **0,565** | **−0,098** |

- **Onde está a falha:** só na **JVIMP**. Ela detecta menos que o publicado nos modelos com interação, quando MAF_I = 0,4 ou β_I = 0,8 (até −0,36 no Sinérgico).
- **As outras quatro medidas** reproduzem dentro do erro de Monte Carlo.

**Diagnóstico** (posterior ao resultado; **não altera o veredito pré-registrado**):
- **Hipótese:** a diferença vem da implementação da VIMP no randomForestSRC 3.4.1, que não é a versão de 2015.
- **Versão de teste:** o randomForestSRC **1.6.1** (04/03/2015), vigente quando o ranger com PPI foi compilado (16/02/2015).
  - Instalado em biblioteca separada, com `-std=gnu17` (o C de 2015 não compila no padrão C23 do GCC 15); o código-fonte não foi alterado.
  - No 1.6.1, `find.interaction` já força `sorted = FALSE` quando `xvar.names` é dado, o que confirma que a correção da D6 reproduz o comportamento original.
- **Rodada:** só a JVIMP do subconjunto, com as mesmas sementes de dados (`resultados/brutos/etapa0_rfsrc161`).

**Resultado do diagnóstico** (job 21317813; 200/200 tarefas; 25,5 CPU-h; JVIMP ≈ 45 s por repetição no 1.6.1). Fonte: `resultados/tabelas/etapa0_subconjunto_jvimp_etapa0_rfsrc161_veredito.json`.
- **Critério 1:** a JVIMP calculada no randomForestSRC 1.6.1 tem **93 %** dos pontos dentro de ±0,10, contra 56,5 % no 3.4.1. No total, **97,1 %** dos pontos ficam dentro de ±0,10.
- **Critério 2:** nenhuma ordem invertida. Os dois critérios são atendidos.
- **Leitura:** a falha da P0 com o 3.4.1 vem da **versão do randomForestSRC** na JVIMP, não do desenho, da simulação nem do código. Com o software da época, o pipeline reproduz as cinco medidas no subconjunto.
- **Veredito formal:**
  - pré-registrado (randomForestSRC atual): **não passa**;
  - diagnóstico posterior (versão de 2015): **passa**.
  - Cabe ao pesquisador decidir qual configuração vale como referência para seguir.

**Custo acumulado do Piloto 7:** ≈ 65 de 150 CPU-h (instalações e pilotos ≈ 1, subconjunto 38,7, diagnóstico 25,5). Restam ≈ 85.
- **Etapa 0 completa** (144 cenários × 100 repetições): ≈ 200–340 CPU-h, conforme a versão usada na JVIMP. **Não cabe** no saldo sem redução.

## D8 (18/11/2026): Etapa 1 — decisões antes de qualquer resultado

**Pedido e respostas do pesquisador.** O pesquisador pediu "roda esta etapa 1" e reenviou a seção 5. Respostas às perguntas:
- instalar PyTorch e interpret (PyPI) num ambiente Python separado;
- **excluir o RSRF** (o simpleRSRF só faz regressão, e o custo com p = 100 é proibitivo);
- 20 cenários × 100 repetições, com o teto ampliado conforme o piloto.
- O pesquisador também informou a **fila scavenger** do HPCC da MSU: não consome a cota e não tem os limites de concorrência. A Etapa 1 roda nela (`PreemptMode = REQUEUE`; retomada por repetição).

**Desenho e dados**
- **Cenários:** os mesmos 20 do subconjunto da Etapa 0 (mtry = 50).
- **Treino:** os mesmos dados da Etapa 0 (mesmas sementes, `problems.R` original).
- **Teste independente:** semente dos dados + 500000. Os conjuntos ficam em `resultados/dados_etapa1/`.
- **Permutações da régua:** 30, com semente dos dados + 900000. O R e o Python usam geradores diferentes, então as permutações são as mesmas dentro de cada linguagem, mas não entre R e Python.

**Detectores e versões**

| Detector | Implementação | Ranking nativo | Régua global sobre |
|---|---|---|---|
| RF | ranger 0.18.0, 500 árvores, mtry 50, probabilidade | — | o próprio |
| Estatística H | hstats 1.2.2 sobre o RF; 7 variáveis; n_max 500; H² normalizado | H² do par | RF |
| Shapley | treeshap 0.4.0 sobre o RF; interações em **50 observações** do teste (~4 s/obs. com p = 100) | média de \|interação\| | RF |
| IF quant. / qual. | diversityForest 0.6.0, `interactionfor`, 500 árvores, `importance = "both"` | EIM (máximo entre as direções) | IF |
| iRF | **iRF 3.0.0** (o do CRAN/arquivo foi substituído pelo do GitHub), `signed = FALSE`, n.iter 5, mtry 50, 500 árvores, **n.bootstrap = 30**, int.return = 5 | estabilidade | floresta da iteração 5 |
| siRF | iRF 3.0.0, `signed = TRUE` (mesmo pacote) | máxima estabilidade entre as combinações de sinal | iRF |
| RPF | randomPlantedForest **0.2.1.9000** (6d6375d, a versão do artigo; o protocolo citava 0.5.0.9000), max_interaction 2, padrões (50 árvores, splits 30) | variância do componente purificado no teste | RPF (probabilidade de `predict`) |
| NID | código original (commit ae974e1) + PyTorch 2.15 CPU; MLP [256, 128, 64], L1 1e-4, parada antecipada | `interpret_pairwise_interactions` | MLP |
| EBM | interpret 0.7.8, padrões | importância do termo do par (0 se não selecionado) | EBM |
| Referências (Etapa 0) | Gini, permutação, PPI, JMST e JVIMP | postos já calculados na Etapa 0, com os mesmos dados de treino | — |

**Desvios dos "padrões do pacote", registrados:**
- **iRF:** `n.bootstrap = 30` em vez do padrão 1. Com 1, a estabilidade é binária e não ordena. 30 é o valor usado no artigo do iRF.
- **iRF:** `int.return = 5`; sem ele, o pacote não devolve interações.
- **RPF:** `max_interaction = 2`. O padrão 1 é aditivo e não tem pares.
- **RPF:** 50 árvores (padrão), e não 500. Com 500, o custo seria ~10× maior.
- **NID:** perda BCE para o desfecho binário (o original usa MSE) e padronização de X.
- **Shapley:** calculado em 50 observações, por custo.

**Direção da régua global** (o protocolo não a fixa):
- **Definição:** I(A,B) = queda(A,B) − queda(A) − queda(B).
- **Comportamento**, conforme o teste sintético do estudo `medida_global`:
  - interação verdadeira → I < 0 (perda compartilhada);
  - redundância → I > 0;
  - aditivo → I ≈ 0.
- **Ranking principal:** **|I| decrescente**, a mesma convenção da JVIMP de Wright (que usa |Difference|, com Difference = soma individual − conjunta = −I).
- **Sensibilidades:** −I decrescente (interação primeiro) e I decrescente.
- **Rankings nativos:** escore decrescente. Empates recebem o posto médio, como no `rank()` de Wright.

**Métricas** (seção 5.3):
- curvas de detecção top-k (k = 1..10) do par verdadeiro entre os 21 pares;
- média da curva;
- taxa no modelo "Sem interação", reportada à parte;
- concordância: interseção dos 3 primeiros pares e tau de Kendall entre os rankings de cada repetição.

**Piloto da Etapa 1** (jobs 21323307 e 21323308; 1 repetição dos 5 modelos do cenário base):
- **Custo por repetição:** R ≈ 25 min e Python ≈ 1,3 min. Os mais caros: componentes do RPF ≈ 4 min, Shapley ≈ 4 min, régua do IF ≈ 3,5 min, iRF e siRF ≈ 3 min cada.
- **Total:** ≈ 870 CPU-h nas 2.000 repetições, na fila scavenger, sem consumir a cota.
- **Primeira tentativa:** falhou por dois motivos técnicos, ambos corrigidos.
  - Faltava o R.utils para o `fread` ler `.gz`; foi instalado do CRAN.
  - O `get_weights` do NID só lê as camadas da classe `MLP`. O `detect_interactions` do próprio repositório usa `create_mlp`, uma inconsistência do código original. Passou-se a usar `MLP`, como no `demo.ipynb`.
- **iRF e siRF:** par não retornado recebe estabilidade 0 (empate no fim), como o IF e o EBM com pares não selecionados. O top-k não muda; isso só evita NA no tau de Kendall.
- **Observação técnica, sem interpretação de resultado:** o log-loss médio de EBM (1,7) e RPF (1,0) é alto, por probabilidades extremas; no RPF, a perda L2 corta as previsões em 0 e 1. A régua em log-loss desses modelos é sensível a isso, e por isso a acurácia é reportada ao lado.
- **Fila (correção):**
  - **Problema:** `--partition=scavenger` sozinho foi reescrito pelo plugin de submissão do ICER para `general-long`. O piloto da Etapa 1 rodou na fila comum e **consumiu cota** (≈ 2,2 CPU-h).
  - **Correção:** a scavenger exige a associação `--account=scavenger --qos=scavenger` (conferida com `sbatch --test-only`). Os arrays 21325094 e 21325095, ainda pendentes e sem execução, foram cancelados e ressubmetidos com essas opções.
- **Interrupções na scavenger (18/11, ~15 h EST):**
  - **Requeue normal:** 35 tarefas foram interrompidas e recolocadas na fila, retomando pela repetição.
  - **Timeout:** 2 tarefas (21325128_47 e _94) voltaram à fila com limite de **12 min** em vez de 12 h. Terminaram em TIMEOUT, que não é recolocado na fila; as partes em Python delas dependiam da conclusão (`aftercorr`).
  - **Ressubmissão:** as duas foram ressubmetidas no mesmo `rodar_etapa1.sb`, com a retomada pelas repetições já gravadas. Ao fim, as tarefas incompletas são conferidas e ressubmetidas.

- 2026-11-18 16:30 EST: mais duas tarefas R (119 e 166) voltaram da preempção com limite reduzido (12 min e 7 min) e morreram em TIMEOUT. Ressubmetidas: R=21335771, PY=21335772 (`--array=119,166`, PY com `aftercorr`). A retomada por repetição evita refazer as repetições já gravadas. Varredura final de tarefas incompletas será feita no fim dos arrays.

- 2026-11-18 18:10 EST: o array PY 21325129 (`aftercorr:21325128`) ficou travado em "Dependency" mesmo com as tarefas R correspondentes concluídas (só 14 de 400 liberadas), provavelmente pelas preempções e recolocações na fila da scavenger. Cancelados 21325129, 21330606 e 21335772; ressubmetidas sem dependência as 373 tarefas cujas 5 repetições em R já existiam e faltava o Python (PY=21339606). As 9 tarefas R ainda rodando (359, 360, 384–390) terão o Python enviado depois que terminarem. As tarefas R 47, 94, 119 e 166 (TIMEOUT) foram concluídas pelas ressubmissões.

## D9 — Etapa 1 v0 invalidada: teste de outra população (2026-11-18, 19:30 EST)

- **Sintoma.** Na v0 completa (2.000 de 2.000 repetições em R e em Python), o RF (ranger) teve acurácia média de 0,479 no teste, abaixo do acaso, com log-loss de 0,699, acima de ln 2. Ele ficou pior justamente nos cenários em que os outros modelos acertam mais (d16: IF 0,590, RF 0,469).
- **Diagnóstico** (d16, rep 1):
  - a coluna de probabilidade está correta;
  - treinando numa metade do treino e testando na outra, a acurácia é 0,62;
  - uma regressão logística com os 7 SNPs, do treino para o teste, acerta 0,683;
  - o RF só com os 7 SNPs acerta 0,66;
  - o RF com os 100 SNPs, do treino para o teste, acerta 0,446.
- **Causa.** `problems.R` (autores, linha 50) sorteia `maf_noise <- runif(93)` a cada chamada de `simulate_data`. A v0 gerou o teste com outra semente e, portanto, com outras MAFs de ruído: o noiseSNP1 tem média 0,86 no treino e 1,14 no teste. Treino e teste vinham de populações diferentes, um deslocamento de distribuição nos SNPs de ruído.
- **Partes da v0 afetadas:**
  - a régua global de todos os modelos;
  - o escore nativo do SHAP (50 observações do teste) e o do RPF (componentes no teste);
  - o desempenho preditivo.
- **Partes da v0 não afetadas:** os escores nativos calculados só no treino (IF, iRF, siRF, H, NID, EBM).
- **Correção** em `src/etapa1.R`:
  - o treino é gerado com o mesmo `simulate_data`, mas com `runif` interceptado para guardar as MAFs. Os sorteios são idênticos, e o treino continua igual ao da Etapa 0 (conferido em d01 e d16);
  - o teste usa essas mesmas MAFs, com a semente dos dados + 500000;
  - verificação em d16, rep 1: a acurácia do RF no teste sobe de 0,446 para 0,662;
  - na nova rodada, em d01: o treino é igual ao da v0, e a diferença média dos SNPs de ruído entre treino e teste é 0,021.
- **Arquivamento.** A v0 foi guardada, sem apagar nada, em:
  - `resultados/brutos/etapa1_v0_teste_outra_populacao`;
  - `resultados/dados_etapa1_v0_teste_outra_populacao` (HPCC);
  - `resultados/tabelas/v0_teste_outra_populacao`.
- **Nova rodada.** Etapa 1 inteira em R: job 21342976 (`--array=1-400`, scavenger). A parte em Python será enviada sem `aftercorr`, depois que o R terminar, por causa do travamento descrito acima.

## D10 — Etapa 0 completa (pedido do usuário, 2026-11-18)

- **Pedido:** "Depois da etapa 1 roda a etapa 0 com mtry 10 e 50". Os 72 desenhos do código × mtry {10, 50} = 144 cenários, com 100 repetições cada (seção 4.4, passo 2).
- **Por que o subconjunto foi só com mtry 50:**
  - era o passo 1 da seção 4.4 (o portão da reprodução);
  - a Etapa 0 completa (cerca de 246 CPU-h) passava do teto de 150 CPU-h, que valia antes de usarmos a scavenger.
- **Fila:** scavenger, que não consome a cota (`scripts/rodar_array_scavenger.sb`: QOS e conta scavenger, requeue, 12 h, logs anexados).
- **Duas rodadas:**
  - `completo_comp_rfsrc341`: as 5 medidas, com randomForestSRC 3.4.1 (a versão atual com `find.interaction`). Saída em `resultados/brutos/etapa0_comp_rfsrc341`; 720 tarefas de 10 repetições.
  - `completo_comp_rfsrc161`: só a JVIMP, com randomForestSRC 1.6.1 (a versão da época, que reproduziu no subconjunto; D6). Saída em `resultados/brutos/etapa0_comp_rfsrc161`; 720 tarefas.
  - Os dois veredictos serão registrados, como no subconjunto.
- **Pastas novas.** A retomada é por arquivo `rep*.csv`, e os arquivos do subconjunto só têm mtry 50. Por isso as rodadas completas gravam em pastas novas e recalculam também os 20 desenhos do subconjunto. As sementes são as mesmas, então os resultados devem ser idênticos ao subconjunto, o que serve de verificação.
- **Quando:** depois que a Etapa 1 corrigida (D9) terminar.

### D10 — resultado (2026-11-19, 00:52 EST)

- **Execução:** jobs 21351088 (3.4.1) e 21351089 (1.6.1), na scavenger. As 1.440 tarefas terminaram COMPLETED, sem reenvio: 7.200 repetições em cada rodada (72 desenhos × 100). A partir daqui, `scripts/03_comparar_etapa0.py` aceita `--de <pasta>`.
- **Gabarito:** 5.760 pontos (48 figuras suplementares: mtry 10 e 50, 5 modelos, 5 medidas, k), todos com par no gabarito. Proporção de casos dentro de ±0,02 da esperada em 60/60 desenhos.
- **Veredicto com rfsrc 3.4.1 (todas as medidas):** **não passa.** 88,2 % dos pontos dentro de 0,10 (critério: 90 %), com 2 inversões de ordem de 103. As duas inversões são da JVIMP (β 0,4 / 0,4, MAF 0,4 / 0,2, "Sem interação" × "Só interação", nos dois mtry). Por medida: Gini 0,969, Permutação 0,965, JMST 0,972, PPI 0,969, **JVIMP 0,553**.
- **Veredicto com a JVIMP de rfsrc 1.6.1:** **passa.** 96,5 % dos pontos dentro de 0,10, nenhuma inversão de 103, diferença absoluta média de 0,023 e viés médio de +0,001. Por mtry: 10 → 96,1 %; 50 → 97,5 %. JVIMP 0,952; a pior figura tem 86,7 % dos pontos dentro de 0,10.
- **Conclusão:** a reprodução completa confirma o D6/D7. As medidas de ranger e a JMST/PPI reproduzem com o código atual, e a JVIMP só reproduz com a versão da época.
- **Verificação contra o subconjunto (mtry 50, 20 desenhos):**
  - 3.4.1: postos idênticos em 100 % das 10.000 linhas (mesmas sementes).
  - JVIMP 1.6.1: mesmas sementes, mas postos iguais em só 23 % das 2.000 repetições (diferença média de posto 0,05; DP 5,7). As curvas diferem em média 0,024 (máximo 0,14 num ponto), o que é compatível com ruído de Monte Carlo de 100 repetições.
  - Leitura: a `find.interaction` do rfsrc 1.6.1 não é reprodutível por `set.seed` (provavelmente o RNG interno/OpenMP). O resultado é estável em distribuição, mas não por repetição. O veredicto passa nas duas rodadas.
- **Tabelas:** `resultados/tabelas/etapa0_completo_etapa0_comp_rfsrc341*_{pontos,ordens,proporcao_casos,veredito}`.
