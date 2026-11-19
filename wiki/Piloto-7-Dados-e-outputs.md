# Piloto 7 — dados, pesos, fluxo e dicionário dos outputs

[Voltar à documentação principal](https://github.com/danifilho/Mestrado_ICMC/wiki/Piloto-7-Wright-Documentacao-integral). Snapshot documental em 19/11/2026. **Não existe um único dataset fixo de Wright neste estudo: há um gerador e milhares de realizações simuladas.**

## 1. O que uma linha representa

Uma linha representa um indivíduo simulado, não um paciente real, gene ou fator de transcrição. As colunas são o desfecho `pheno` e 100 genótipos. Não são dados de Drosophila, ChIP-seq ou Gene Ontology. Os genótipos são contagens 0, 1 ou 2 de um alelo; `pheno` é uma resposta binária sorteada da probabilidade dada pela fórmula.

| Coluna(s) | Quantidade | Valores | Papel no gerador | Papel no modelo |
|---|---:|---|---|---|
| pheno | 1 | 0/1 | Sorteio Bernoulli com p individual | Resposta; não entra como atributo |
| interactionSNP1, interactionSNP2 | 2 | 0/1/2 | Par designado, com coeficientes dependentes do cenário | Atributos; o nome não deve ser interpretado como evidência aprendida |
| effectSNP1…effectSNP5 | 5 | 0/1/2 | Efeitos individuais beta_M | Atributos concorrentes relevantes |
| noiseSNP1…noiseSNP93 | 93 | 0/1/2 | Coeficiente zero na fórmula do desfecho | Atributos de ruído disponíveis para os algoritmos |

Ruído significa ausência de efeito no gerador, não coluna constante nem ausência de associação amostral por acaso. O ranking de pares exclui esses SNPs **apenas na avaliação**, enquanto os ajustes recebem todas as 100 colunas.

## 2. Como cada genótipo é sorteado

Para frequência p, as probabilidades dos genótipos são `(1−p)²`, `2p(1−p)` e `p²`. São as proporções de Hardy–Weinberg usadas no gerador. Frequências dos dois SNPs designados são iguais entre si; as cinco variáveis de efeito usam MAF_M. No desenho principal os SNPs são gerados sem uma estrutura de desequilíbrio de ligação imposta.

O parâmetro chamado `maf_noise` é sorteado com `runif(93)` no código original, em (0,1). Estritamente, frequência do alelo *menor* não excede .5; por isso preservamos o nome histórico do parâmetro, mas descrevemos operacionalmente esse sorteio como frequência do alelo codificado. Não corrigimos silenciosamente o gerador dos autores.

Código-fonte: [problems.R](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/fontes/codigo_autores/replication/01_main_simulation/problems.R) e [simulate_snps.R](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/fontes/codigo_autores/replication/01_main_simulation/simulate_snps.R).

## 3. Fórmula, coeficientes e “pesos” dos dados

`eta = beta0 + c1*x1 + c2*x2 + c12*x1*x2 + beta_M*(effectSNP1+…+effectSNP5)`

`p = 1/(1+exp(-eta))`; `pheno ~ Bernoulli(p)`.

| Modelo no arquivo | c1 | c2 | c12 | O que muda |
|---|---:|---:|---:|---|
| no_interaction | beta_I | beta_I | 0 | Sem produto no logit |
| synergistic | beta_I | beta_I | beta_I | Produto na mesma direção |
| interaction_only | 0 | 0 | beta_I | Produto sem termos individuais explícitos |
| modifier_snp1 | 0 | beta_I | beta_I | Primeiro SNP sem termo individual explícito |
| modifier_snp2 | beta_I | 0 | beta_I | Versão simétrica, excluída das figuras históricas |
| redundant | beta_I | beta_I | −beta_I | Produto de sinal oposto aos individuais |

`beta0 = logit(0.5) − 4*beta_I*MAF_I − 10*beta_M*MAF_M`.

Essa fórmula não inclui a contribuição média do produto. Assim, pedir `prop_cases=.5` não produz exatamente 50% de casos em cada modelo. O valor esperado varia aproximadamente de .335 a .570 na grade auditada. A classe majoritária pode superar .5: acurácia .5 não deve ser usada como referência universal sem considerar prevalência.

### Exemplo concreto

Com beta_I=beta_M=.4, MAF_I=.4 e MAF_M=.2, beta0=−1.44. No modelo “Só interação”, as penetrâncias médias sobre os cinco SNPs de efeito são aproximadamente .3526 para (0,0), .4427 para (1,1), .5366 para (2,1) e .7122 para (2,2). O gabarito publicado arredonda a .35, .44, .54 e .72. O erro máximo é .0078, dentro da tolerância .01 do protocolo. Isso verifica cálculo de probabilidades; não exige que a proporção de casos de uma amostra finita seja exatamente igual.

Não há pesos manuais por indivíduo no gerador. A distribuição genotípica define a frequência com que cada combinação aparece. Nas análises agregadas, realizações e configurações são ponderadas igualmente; não se pondera um cenário por ter desempenho melhor.

## 4. Quais datasets existem e onde foram usados

| Material | Tamanho/estrutura | Uso | Não confundir com |
|---|---|---|---|
| Dados originais geráveis pelo suplemento | n=1000, 100 SNPs na grade principal | Desenho de referência | Um arquivo observado de pacientes |
| Etapa 0 subconjunto | 20×100 realizações | Portão de reprodução, mtry 50 | 20 folds de uma mesma amostra |
| Etapa 0 completa | 72×100 datasets; dois mtry por dataset | Comparação com S1–S48 | Todos os 124 ensaios/figuras do suplemento |
| Treino Etapa 1 | 20×100 datasets, n=1000 | Ajuste dos novos métodos; mesmos dados da Etapa 0 correspondente | Novo sorteio diferente para cada algoritmo |
| Teste Etapa 1 corrigida | n=1000 por realização, mesma população, novos indivíduos | Previsão, régua, SHAP amostral e componentes RPF | Dados usados para reajustar árvores |
| Validação interna NID | 20% do treino | Parada antecipada | Teste externo |
| Amostra de SHAP | 50 linhas sorteadas do teste | Média de interações SHAP | 50 repetições independentes |
| H | Até 500 linhas do treino | Dependência parcial e H² | Mesma amostra de SHAP |
| EBM | Treino e partições internas do pacote | Ajuste e importância dos termos | Extração baseada no gabarito |
| v0 | Teste com frequências de ruído novas | Diagnóstico arquivado | Resultado válido do ensaio planejado |
| Suplemento com LD | Estrutura baseada em cromossomo 22/1000 Genomes, simulada com HapSim | Ensaio dos autores | Cenário executado na extensão atual |

Os ensaios adicionais do artigo incluem dois SNPs marginais, 2.500 SNPs totais e correlação genética. Estão no atlas, mas não no nosso veredito de reprodução da grade principal.

### Quatro configurações da Etapa 1

| Configuração | beta_I | beta_M | MAF_I | MAF_M | Interpretação |
|---|---:|---:|---:|---:|---|
| Base | .4 | .4 | .2 | .2 | Referência |
| Frequência maior do par | .4 | .4 | .4 | .2 | Combinações do par aparecem com maior frequência |
| Efeitos concorrentes maiores | .4 | .8 | .2 | .2 | Cinco SNPs individuais mais fortes |
| Coeficiente do par maior | .8 | .4 | .2 | .2 | Aumenta coeficientes associados ao par conforme cada modelo |

Essas quatro configurações cruzadas com cinco modelos produzem 20 cenários. A ordem dos painéis c/d das Figuras 3 e 4 do artigo não é a mesma: na Figura 3, c aumenta beta_M e d aumenta beta_I; na Figura 4 ocorre o inverso. O código da extensão seleciona o conjunto de quatro configurações, não depende da letra c/d para calcular resultados.

## 5. Fluxo de dados e produção de outputs

```text
Suplemento 3 → problems.R + simulate_snps.R → dataset por cenário/repetição
  ├─ Etapa 0 → cinco medidas → postos → curvas → comparação com suplemento 4
  └─ Etapa 1 → modelos ajustados
        ├─ escores nativos → ranking dos 21 pares
        ├─ teste independente → log-loss/acurácia
        └─ teste permutado → contraste I → três direções de ranking
             ↓
      tabelas por repetição → resumos → quatro figuras históricas
```

O suplemento 2 fornece tabelas de penetrância, o suplemento 1 fornece ranger com PPI, o suplemento 3 fornece código e o suplemento 4 fornece figuras. O gabarito numérico é extraído do suplemento 4. Não se treina nenhum detector nos pontos das curvas publicadas.

## 6. Outputs brutos: unidade de cada linha

### Etapa 0 — repNNN.csv

Uma linha é uma medida aplicada a uma realização de um desenho e mtry. Campos:

- `desenho`: índice fixo da grade de 72 desenhos; não é posição no ranking.
- `model`, `beta`, `beta_effect`, `maf_interaction`, `maf_effect`: gerador e seus parâmetros.
- `repeticao`: realização Monte Carlo de 1 a 100; não fold.
- `semente_dados`: número para regenerar a amostra.
- `mtry`: configuração da floresta.
- `algo`: impurity, permutation, jvimp, jmst ou pairwise.
- `rank`: posto do alvo, com definições diferentes para individuais e pares. Não misturar esses dois universos.
- `segundos`: tempo da chamada daquela medida, em segundos; não custo total da tarefa nem CPU-h do estudo.
- `prop_casos`: fração de pheno=1 no dataset de treino.
- `ranger`, `randomForestSRC`: versões efetivamente carregadas.
- `erro`: mensagem capturada; vazio não substitui teste de valores finitos.

### Etapa 1 — repNNN.csv e repNNN_py.csv

Uma linha é **um par × detector × tipo de ranking × realização**. Cada ranking cobre 21 pares.

- `detector`: método de escore. H/SHAP compartilham RF; IF tem duas saídas.
- `ranking`: nativo, global_logloss ou global_acuracia.
- `par`: nomes dos dois SNPs separados por dois-pontos, na ordem canônica.
- `escore`: escore nativo ou I assinado, antes de escolher a direção.
- `modelo`: preditor que sustenta a régua; distinto de `model`, que é a fórmula geradora.
- `posto`: rank decrescente de escore; `posto_abs`: rank decrescente de módulo; `posto_neg`: rank crescente de escore, equivalente a ordenar −I.
- `verdadeiro`: marca o par designado interactionSNP1:interactionSNP2. **No cenário no_interaction essa marca não significa que exista interação.**
- parâmetros, mtry, repeticao e semente: chaves de rastreabilidade.
- `n_pares_ebm_selecionados`: quantidade de termos de pares do EBM no conjunto de atributos, não necessariamente entre os 21 avaliados. O CSV Python repete esse metadado nas linhas; não somar essas repetições.

### Desempenho e tempos

`repNNN_desempenho.csv`/`_py.csv`: uma linha por preditor e realização, com logloss/acuracia no teste. H e SHAP não são novos preditores. `*_tempos.json`: dicionário de durações por ajuste, extração e régua; não somar indicadores já agregados duas vezes.

### Dados de treino/teste e objetos ajustados

Os executores gravam `resultados/dados_etapa1/dXX/repNNN_treino.csv.gz` e `repNNN_teste.csv.gz` no ambiente de execução. Essa pasta não está incluída no snapshot local consultado. Não criamos um link falso de download desses inputs. O gerador, configurações e sementes estão disponíveis para regeneração. Os outputs numéricos locais corrigidos foram anexados em arquivos compactados. Pesos completos de modelos ajustados não foram encontrados nesse conjunto de saídas históricas.

## 7. Tabelas derivadas e sua finalidade

| Família | Uma linha representa | Uso/aviso |
|---|---|---|
| gabarito_wright.csv | figura×modelo×medida×k com parâmetros | Valor publicado extraído; não resultado nosso |
| etapa0_*_pontos.csv | nosso ponto unido ao publicado | `dif=nosso−publicado`; n_rep e n_na auditam denominador |
| etapa0_*_ordens.csv | comparação elegível de duas médias de curvas | `invertida` compara sinais; só diferenças publicadas >.10 |
| etapa0_*_proporcao_casos.csv | desenho e prevalência média | Compara ao esperado teórico; não métrica preditiva |
| etapa0_*_veredito.json | resumo da rodada | Critérios booleanos, cobertura, erros e resultados por medida |
| etapa1_postos_par_verdadeiro.csv.gz | realização×detector×direção | Material para curvas e reanálise; alvo designado no controle nulo |
| etapa1_curvas_deteccao.csv | cenário×detector×direção×k | `deteccao` é proporção posto≤k; `na` registra ausentes |
| etapa1_resumo_deteccao.csv | cenário×detector×direção | Média nos dez k; referência uniforme histórica |
| etapa1_resumo_por_modelo.csv | detector×ranking×direção | Uma coluna por fórmula; médias sobre quatro configurações; arredondamento a três casas |
| etapa1_concordancia_por_repeticao.csv.gz | dois rankings na mesma realização | Interseção top-3 e Kendall |
| etapa1_concordancia_resumo.csv | par de rankings | Médias; `n` é tamanho do grupo, não necessariamente Kendall válido |
| etapa1_desempenho_modelos.csv | preditor | Média das realizações; sem intervalos históricos |
| figuras/dados/e1_fig*.csv | dado diretamente enviado ao desenho | Facilita reconstruir cada PNG; alguns já arredondados |
| piloto1_* | teste de integração de cinco modelos geradores, uma repetição cada | Não misturar aos 2.000 resultados principais |
| v0_teste_outra_populacao | saídas invalidadas para a pergunta planejada | Mantidas no original e no inventário, fora das figuras finais |
| auditoria/sensibilidade_empates.csv | detector×modelo gerador | Reanálise documental posterior, não resultado pré-registrado |

## 8. Arquivos por função e limites de disponibilidade

- `configs/congelamento.json`: hashes registrados naquele congelamento; mudanças posteriores podem não coincidir. O manifesto documental identifica o snapshot efetivamente publicado e não substitui o congelamento histórico.
- `auditoria/verificacao_simulacao.json`: penetrâncias e prevalências esperadas.
- `auditoria/gabarito_extracao.json`: legenda, página e metadados de extração das figuras.
- `resultados/*_brutos.tar.gz`: arquivos históricos corrigidos por repetição, compactados para download; descompactar sob `resultados/brutos/` antes de reexecutar a análise histórica.
- `auditoria/inventario_originais.csv`: caminhos relativos, tamanhos e hashes dos originais locais, incluindo arquivos não republicados. Um inventário não implica que todo arquivo esteja anexado.
- `extensao_AD/`: código preparatório; não há resultados finais inferidos de sua simples presença.

O anexo de código contém um catálogo automático dos arquivos publicados e os cabeçalhos reais das tabelas. O texto acima explica sua semântica; o catálogo permite conferir nomes exatos sem abreviar arquivos longos.


---
Snapshot das evidências: [`edcbf4cc4505`](https://github.com/danifilho/Mestrado_ICMC/commit/edcbf4cc450583364e69cbe89a738596c7c2762f). Documentação publicada em 19/11/2026.
