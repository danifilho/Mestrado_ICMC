# Piloto 7 — Wright, régua global e documentação integral dos ensaios

**Documentação: 19/11/2026, America/Sao_Paulo.** Execuções históricas: 18–19/11/2026; horários EST nos logs foram preservados com seu fuso. Esta página é uma auditoria documental e uma reanálise localizada dos empates, não uma nova execução dos modelos no HPCC.

## Como navegar

1. [Explicação simples e resultados](#explicação-simples).
2. [Dados, pesos e fluxo de uso](https://github.com/danifilho/Mestrado_ICMC/wiki/Piloto-7-Dados-e-outputs).
3. [Todas as figuras principais, explicadas](https://github.com/danifilho/Mestrado_ICMC/wiki/Piloto-7-Figuras-comentadas).
4. [Atlas completo do suplemento de Wright: S1–S124](https://github.com/danifilho/Mestrado_ICMC/wiki/Piloto-7-Atlas-Wright).
5. [Decisões, adaptações, limitações e próximos ensaios](#decisões-e-histórico).
6. [Anexo técnico: código, arquivos, reprodução e integridade](https://github.com/danifilho/Mestrado_ICMC/wiki/Piloto-7-Codigo-e-reproducao).

**Escopo:** reprodução Etapa 0, extensão Etapa 1, auditorias posteriores e proposta A–D. O pré-piloto Drosophila/splicing é contextualizado, mas seus resultados não são misturados aos resultados de Wright. A análise de escala foi adiada pelo pesquisador para depois da qualificação. Nenhum estudo de validação biológica foi executado nesta documentação.

## Fontes e graus de evidência

- **Artigo primário lido:** Wright, Ziegler e König (2016), *Do little interactions get lost in dark random forests?*, BMC Bioinformatics 17:145, [texto integral](https://pmc.ncbi.nlm.nih.gov/articles/PMC4815164/), [DOI](https://doi.org/10.1186/s12859-016-0995-8). Artigo e figuras em CC BY 4.0, com atribuição nesta documentação.
- **Evidências locais:** [protocolo preservado](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/PROTOCOLO.md), [decisões preservadas](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/DECISOES.md), [relatório histórico](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/RELATORIO_ETAPA1.md), código original dos autores, executores locais, tabelas, arquivos por repetição, suplementos e congelamento. Links técnicos desta publicação apontam para um snapshot identificado por commit.
- **Conversa atual:** pedidos do pesquisador, esclarecimento da orientação do Prof. Cerri, revisão crítica e prompt A–D. A atribuição ao orientador é **relato do pesquisador**, não transcrição de reunião acessada diretamente.
- **Outro chat consultado:** “Análise crítica de interações”, leitura disponível dos turnos recentes relativos ao piloto de plausibilidade funcional em expressão de rato. Esse histórico ajuda a explicar por que separar desempenho, estabilidade e biologia; não é fonte dos números de Wright. O acesso retornou somente os turnos disponíveis; não afirmamos leitura integral de todos os chats.
- **Mensagens de execução fornecidas pelo pesquisador:** registros do problema de população, reenvio e conclusão do HPCC. A documentação prefere código/tabelas para números, e identifica as explicações causais ainda não verificadas.

## Explicação simples

Imagine uma prova para algoritmos. Nós criamos pessoas artificiais e seus genótipos. Sabemos a fórmula que atribui probabilidade de caso ou controle. Em alguns exercícios, um par tem um termo específico de combinação; em outro, cada integrante importa, mas não há esse termo. Todos os métodos recebem o mesmo exercício.

Existem três perguntas que não devem ser confundidas:

1. **Previsão:** o modelo consegue prever o desfecho em pessoas novas?
2. **Priorização:** quais variáveis ou pares o modelo considera importantes, pelo seu próprio critério ou por uma medida externa comum?
3. **Interpretação:** essa prioridade corresponde ao termo do gabarito? E, posteriormente, teria significado biológico?

A proposta relatada do orientador é aplicar uma medida comum **depois do ajuste**, ordenando os mesmos candidatos e examinando a interseção no topo. Um modelo não precisa possuir extrator nativo de pares para participar: basta permitir prever após permutarmos colunas.

### O que Wright fez

Wright separou **capturar variáveis que participam de uma interação** de **detectar a interação como tal**. Gini e importância por permutação avaliam variáveis; PPI, JMST e JVIMP avaliam pares. O artigo encontrou dificuldade em separar efeitos individuais de combinações específicas, nos cenários avaliados. Isso não significa que florestas sejam incapazes de usar relações conjuntas para prever. [Fonte primária](https://pmc.ncbi.nlm.nih.gov/articles/PMC4815164/).

### O que fizemos na Etapa 0

Reproduzimos a grade principal do código publicado. O primeiro portão usou 20 desenhos, 100 realizações e mtry 50. A execução completa usou 72 desenhos e dois mtry, 10 e 50. O mesmo dataset de cada realização é reaproveitado entre medidas e mtry; portanto, não são 14.400 datasets independentes, mas 7.200 datasets e 14.400 avaliações desenho–mtry antes de contar as medidas.

A reprodução passou com a JVIMP histórica, mas não com a JVIMP atual. “Passou” significa cumprir as tolerâncias de curvas e ordenações definidas no estudo, não obter cada número exatamente igual ao artigo.

| Rodada | Pontos com diferença ≤0,10 | Ordens invertidas | Veredito |
|---|---:|---:|---|
| Subconjunto, rfsrc 3.4.1 | 89,5% de 960 pontos | 1/26 | Não passou |
| Subconjunto, substituição pela JVIMP 1.6.1 | 97,1% | 0/26 | Passou no diagnóstico posterior |
| Completa, rfsrc 3.4.1 | 88,2% de 5.760 pontos | 2/103 | Não passou |
| Completa, substituição pela JVIMP 1.6.1 | 96,5% | 0/103 | Passou |

As quatro outras medidas não foram todas recalculadas com a versão antiga: a rodada alternativa substitui **apenas a JVIMP**. O conjunto completo incluiu a versão simétrica do modificador; as figuras avaliadas excluem essa versão, resultando em 60 desenhos distintos nos relatórios de proporção de casos.

### O que fizemos na Etapa 1

Reutilizamos 20 desenhos do subconjunto, cada um com 100 realizações. Treinamos os modelos, avaliamos previsão em teste independente e construímos rankings de 21 pares. Fizemos duas avaliações: escores particulares de cada método e contraste de permutação comum.

| Modelo preditivo | Log-loss média, menor melhor | Acurácia média |
|---|---:|---:|
| RF | 0,657 | 0,610 |
| iRF | 0,658 | 0,608 |
| IF | 0,663 | 0,609 |
| NID | 0,680 | 0,579 |
| RPF | 0,685 | 0,616 |
| EBM | 0,819 | 0,588 |

Essas médias não estabelecem equivalência. O EBM tem boa recuperação do par do gabarito no resumo histórico, mas pior log-loss; isso não prova, sem examinar calibração, que a causa seja exclusivamente excesso de confiança.

### O resultado de pares em palavras

Os métodos não responderam igualmente aos cinco tipos de cenário. Vários tiveram resultados melhores no cenário sinérgico e fracos em “Só interação” e “Redundante”. O EBM apresentou o contraste descritivo mais favorável no resumo histórico. Porém, a análise dos empates muda sua posição em relação à referência aleatória no controle sem interação. Por isso, frases como “EBM detecta sem falsos positivos” não são sustentadas.

A régua comum produziu **médias de recuperação próximas** em RF, IF, iRF e EBM. Isso não significa rankings iguais: as correlações entre rankings da régua variaram aproximadamente de 0,12 a 0,50. A figura 4 histórica mostra os **escores nativos**, não a concordância da régua comum. Esse ponto é decisivo para não atribuir à figura uma resposta que ela não oferece.

## Metodologia técnica da Etapa 0

### Grade, medidas e gabarito

O executor [etapa0.R](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/src/etapa0.R) carrega `simulate_snps.R`, `problems.R` e `algorithms.R` dos autores. Não reimplementa silenciosamente a PPI: usa o ranger distribuído no suplemento, 0.1.6.33. A infraestrutura BatchExperiments dos autores foi substituída por arrays SLURM; isso muda a orquestração e o esquema de sementes, não a fórmula do desfecho.

A grade é definida em [02_tarefas_etapa0.py](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/scripts/02_tarefas_etapa0.py). A ordem fixa é modelo × beta_I × beta_M × par de frequências. Há seis modelos no código, dois níveis de cada beta e três pares de frequência: 6×2×2×3=72. O artigo descreve cinco modelos e uma grade textual diferente; seguimos o código e preservamos a discrepância em D1/D3.

- 500 árvores por floresta da Etapa 0.
- mtry 10 ou 50: número de variáveis candidatas a cada divisão, não número total de variáveis usadas.
- Gini: redução de impureza acumulada; permutação: prejuízo OOB individual.
- PPI: prejuízo OOB ao perturbar conjuntamente o par; não subtrai os efeitos individuais.
- JMST: média das profundidades nas duas direções; menor valor indica prioridade.
- JVIMP: diferença entre soma individual e efeito conjunto no procedimento de perturbação interno do pacote; o código ordena pelo módulo. Não é idêntica ao nosso executor de permutação no teste.
- Individuais: posto é o máximo dos postos dos dois SNPs designados, entre 100 variáveis. Ambos precisam estar no top-k.
- Pares: posto do par designado entre os 21 candidatos, sem pares contendo SNPs de ruído.

O gabarito não veio de leitura a olho. [01_gabarito_pdf.py](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/scripts/01_gabarito_pdf.py) extrai as polilinhas vetoriais do PDF, identifica painéis e cores Set1 e converte coordenadas em probabilidades. São **5.760 pontos**: 24 figuras individuais ×5 modelos ×2 medidas ×9 cortes, mais 24 figuras de pares ×5 modelos ×3 medidas ×10 cortes. Pontos de uma mesma curva são dependentes.

### Critério operacional de reprodução

[03_comparar_etapa0.py](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/scripts/03_comparar_etapa0.py) reúne as repetições, calcula a fração com posto≤k e une ao gabarito por parâmetros, modelo, medida e k. Exige pelo menos 90% dos pontos com diferença absoluta≤0,10 e nenhuma inversão das comparações elegíveis.

A segunda regra é mais específica que “nenhuma inversão de qualquer curva”: compara Gini versus permutação e “Sem interação” versus “Só interação” para as medidas de pares, **apenas quando a diferença das médias publicadas supera 0,10**. O número de ordens elegíveis é 26 no subconjunto e 103 no completo. A verificação de proporção de casos é reportada à parte; o booleano `P0_passa` combina os dois critérios de curvas.

A tolerância de 0,10 é um critério operacional de reprodução estatística, não um teste formal de equivalência. Não devemos tratar 5.760 pontos como 5.760 replicações independentes.

### Sementes e reprodutibilidade

Semente dos dados = `12345 + 1000*desenho + repeticao`. Cada medida reinicia o gerador com a semente dos dados +100×índice da medida +mtry. Os arquivos por tarefa fixam a ordem das medidas; alterar essa ordem pode alterar o número efetivo da semente do método.

O executor admite `RNGkind(sample.kind="Rounding")`, mas o gerador de tarefas preservado define `rng_rounding=False`. Não afirmamos ter reproduzido as amostras exatas de 2016. A reprodução é estatística. Na versão 3.4.1, os postos do subconjunto repetiram na rodada completa. Na JVIMP 1.6.1, apenas 23% repetiram; o motivo interno do RNG/OpenMP é uma hipótese não demonstrada.

## Metodologia técnica da Etapa 1

### Configurações efetivas, escores e escolhas

| Procedimento | Configuração observável | Escore nativo utilizado | Adaptação/limitação |
|---|---|---|---|
| RF | ranger 0.18.0, 500 árvores, mtry 50, probabilidade, uma thread | Não tem escore nativo de par neste estudo | Base comum de H e SHAP |
| H | hstats 1.2.2, sete variáveis, n_max=500, normalizado, ao quadrado | H² | Calculado sobre probabilidade de classe 1, no treino |
| SHAP | treeshap 0.4.0, unificação do RF com treino | média do módulo da interação | Somente 50 observações sorteadas do teste |
| IF | diversityForest 0.6.0, 500 árvores, importance=both, probabilidade | EIM quantitativa e qualitativa separadas | Máximo entre versões/direções do mesmo par; chamada não passa mtry explicitamente |
| iRF | iRF 3.0.0, cinco iterações, 500 árvores, mtry 50, 30 bootstraps, int.return=5 | estabilidade de conjuntos exatamente de tamanho 2 | Ausente recebe zero; conjuntos maiores não contam como pares |
| siRF | mesmo pacote, signed=TRUE | maior estabilidade entre sinais do par | Remove sinais para comparar pares; régua reaproveita o preditor iRF, não é avaliação independente de outro preditor |
| RPF | randomPlantedForest 0.2.1.9000, commit 6d6375d, max_interaction=2, demais padrões | variância do componente purificado no teste | 50 árvores/splits 30 conforme D8; não 500; resumo de componente é uma operacionalização nossa |
| NID | código ae974e1, MLP 256–128–64, BCEWithLogitsLoss, Adam lr .01, L1 1e-4, batch 100, até 100 épocas, paciência 5 | escore de pesos do procedimento pairwise | Padronização; 20% do treino para validação; main-effect nets desligadas |
| EBM | interpret 0.7.8, ExplainableBoostingClassifier, padrões e n_jobs=1 | term_importances do termo do par | Pares não selecionados recebem zero; padrões dependem da versão |

**Pesos não se resumem a uma tabela de constantes.** Os coeficientes beta do gerador são fixados por cenário; pesos da rede NID, funções do EBM, pesos iterativos do iRF e divisões das árvores são aprendidos a cada ajuste. Os executores históricos salvam escores, postos, desempenho e tempos, mas não um dump completo de todos os objetos ajustados/pesos aprendidos. Portanto, não inventamos os valores desses pesos nem prometemos reconstruir cada árvore a partir de uma tabela de ranking. A reprodução exige dados/sementes e ambiente compatíveis.

Não há pesos de classe explícitos nas chamadas auditadas. As amostras entram com os padrões das implementações; bootstraps internos não são pesos de cenário. No resumo, cada realização recebe o mesmo peso; cada uma das quatro configurações de um tipo de modelo recebe peso 1/4; cada tipo com interação recebe peso 1/4 no resumo “com interação”. Cada corte k recebe peso 1/10.

A versão RPF indicada inicialmente no protocolo era diferente da executada; D8 registra a substituição. O relatório resume RSRF como excluído por ausência de código, mas D8 também registra `simpleRSRF` com regressão e custo impeditivo para esta tarefa de classificação. A formulação precisa é: RSRF não participou, por incompatibilidade/custo da implementação considerada, conforme decisão registrada; não afirmamos inexistência universal de código.

### Treino, teste e as duas linguagens

[etapa1.R](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/src/etapa1.R) gera e grava os dados. Python lê os mesmos CSVs. Teste usa semente dos dados+500000 e as mesmas frequências populacionais dos SNPs de ruído. O mecanismo intercepta `runif` no ambiente da função geradora para capturar/reutilizar frequências, preservando a geração do treino. O registro relata verificações em d01 e d16; não afirma comparação byte a byte de todos os datasets.

A semente de permutação é dados+900000. R usa `sample.int`, Python usa `default_rng`: os índices são compartilhados dentro de cada linguagem, mas **não são os mesmos entre linguagens**. A intenção de permutações integralmente compartilhadas será corrigida na extensão A–D, não retroativamente atribuída à execução histórica.

### Definição e direção da régua

Para log-loss, ΔA = perda após embaralhar A − perda original. Para acurácia, ΔA = acurácia original − acurácia após embaralhar A. Média de 30 permutações, sem reajustar o modelo. A e B recebem a mesma permutação na perturbação conjunta.

`I(A,B) = ΔAB − ΔA − ΔB`.

Ranking principal histórico por módulo `|I|`; sensibilidades por `−I` e por `I`. O módulo não distingue direções, e pode priorizar efeitos conjuntos de natureza diferente. A direção foi fixada em D8 após a experiência do pré-piloto e antes da execução principal desta etapa; não está especificada no protocolo originalmente recebido. Não é uma propriedade universal que “interação implica I<0” ou “aditivo implica I=0”.

Log-loss usa logaritmo natural e probabilidades cortadas em [1e-15,1−1e-15]. Isso evita infinito, mas previsões extremas ainda recebem grande penalidade. Acurácia usa `p>0.5` (p exatamente .5 cai na classe zero). `log-loss` não equivale a “medir interação no logit”.

As quedas individuais/conjuntas são intermediárias do executor histórico; o CSV histórico salva I e postos, não todas as 30 perdas por variável/par. Não é possível obter ΔAB apenas de I sem os outros componentes. A extensão A–D precisa salvar esses intermediários.

### Construção das curvas e concordância

Os escores são convertidos em postos decrescentes com empates pelo posto médio. Para cada realização, a análise testa posto≤k, k=1,…,10. Calcula a proporção por cenário e depois a média dos dez cortes. Essa média não é AP, ROC-AUC, acurácia ou taxa de acerto em primeiro lugar.

A referência uniforme sem empates é média(k/21)=5,5/21≈0,261905. Com a regra histórica de postos médios, essa referência requer cautela: se os 21 escores empatarem, todos têm posto 11 e nenhum entra no top-10. Isso não corresponde ao comportamento de um desempate aleatório.

Kendall é calculado sobre os escores dos 21 pares na mesma realização. Rankings constantes geram NaN. A média ignora NaN, enquanto `n` usa size e conta linhas: o denominador efetivo de Kendall pode ser menor que o n impresso. O top-3 histórico usa ordenação seguida de head(3), sem desempate probabilístico no limite. As réguas herdadas de um mesmo preditor são deduplicadas para não multiplicar artificialmente RF/H/SHAP ou IF quantitativo/qualitativo.

### Auditoria posterior dos empates

A sensibilidade publicada aqui é calculada diretamente dos arquivos nativos corrigidos, sem retreino. Se b pares têm escore maior e e empatam com o par, sua inclusão esperada no top-k sob desempate uniforme é `max(0,min(e,k−b))/e`. O script e os resultados estão em [auditar_empates.py](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/auditoria/auditar_empates.py) e [sensibilidade_empates.csv](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/auditoria/sensibilidade_empates.csv).

| EBM | Convenção histórica | Desempate fracionário |
|---|---:|---:|
| Média dos quatro tipos com interação | 0,649 | 0,668 |
| Sem interação | 0,270 | 0,311 |

Cada tipo agrega 400 realizações. O EBM continua forte descritivamente, mas a afirmação “fica no acaso sem interação” depende da convenção. Os PNG históricos não foram substituídos; suas legendas precisam ser lidas com esta ressalva.

## Decisões e histórico

| Registro | O que foi decidido/verificado | Motivo e efeito na interpretação |
|---|---|---|
| D0 | Protocolo recebido terminava em 5.3; Etapa 2 ausente | Não atribuir execução ao texto que só chegou depois |
| D1 | Seguir código quando difere da descrição textual | Preserva a grade geradora das figuras; discrepâncias continuam visíveis |
| D2 | Download dos quatro suplementos e hashes | Rastreabilidade dos autores |
| D3 | Confirmação de coeficientes, nomes, postos e instâncias | Corrige hipótese provisória do modificador; versão simétrica não plotada |
| D4 | Extração vetorial de S1–S48 | Evita erro de leitura visual, sem eliminar Monte Carlo |
| D5/D6 | Congelamento/pilotos e ajustes de compatibilidade | Detalhes integrais no registro preservado; não confundir adaptações técnicas com resultados científicos |
| D6 | Registro S3 de importance.ranger, troca de rfsrc 3.10.0 sem find.interaction para 3.4.1, e sorted=FALSE | Primeiro piloto falhou; segundo teve 11/20 postos JMST ausentes; terceiro passou. A compatibilidade não redefine o escore |
| D7 | Versão atual não passa; diagnóstico com 1.6.1 passa | Seleção da versão histórica foi posterior ao primeiro resultado |
| D8 | Inclusão dos detectores, adaptações e direção da régua | Define o que cada resultado realmente representa |
| Incidentes de fila | Preempções/timeouts e dependência aftercorr bloqueada | Reenvio com retomada por repetição; COMPLETED não substitui auditoria dos arquivos |
| D9 | v0 usava população de teste diferente | Invalida régua/previsão e escores dependentes do teste para a pergunta planejada; rodada foi preservada e refeita |
| D10 | Ampliação da reprodução para mtry 10 e 50 | Não amplia automaticamente a Etapa 1, que continua com 20 cenários |
| Conversa de 19/11 | Priorizar avaliação comum e interseção no topo | Reorganiza a pergunta para a qualificação |
| Conversa de 19/11 | Escala adiada para pós-qualificação | Não executar Etapa 2 nesta documentação |
| Auditoria documental de 19/11 | PDF contém S1–S124, não apenas S1–S110 | Corrige catálogo; o gabarito numérico continua S1–S48 |

### O incidente de população, sem simplificações

A função dos autores sorteia frequências dos SNPs de ruído a cada nova chamada. Criar teste com outra semente, sem preservar essas frequências, criou mudança de distribuição. O diagnóstico registrou RF com 100 SNPs em 0,446 em um caso, contra 0,662 após a correção. Isso foi uma verificação localizada, não a média do estudo. A v0 inteira teve RF médio 0,479; a rodada corrigida, 0,610.

A mudança afetava previsão, régua, SHAP e componentes RPF calculados no teste. Escores nativos calculados só no treino não dependiam diretamente dessa falha. Mesmo assim, a rodada completa foi refeita. O arquivo antigo continua no inventário e não é misturado ao final.

## Limitações e interpretação cientificamente permitida

- **Escala:** ausência de termo AB no logit não garante aditividade na probabilidade. H foi aplicado à probabilidade; EBM modela termos em logit. Não atribuir automaticamente toda divergência a erro do detector.
- **“Só interação”:** significa coeficientes individuais zero na parametrização; não garante associação marginal estatística nula, pois os genótipos são não negativos e o produto pode gerar associação após marginalização.
- **Configuração:** 500 árvores não equaliza custo; RPF usou 50; iRF inclui iterações e bootstraps. IF requer sensibilidade para a precisão da EIM; aumentar árvores não garante melhora.
- **Universo:** excluir pares com ruído facilita a avaliação e usa o gabarito. O resultado é condicional aos 21 candidatos.
- **Incerteza:** figuras históricas não têm intervalos pareados. Médias próximas não demonstram equivalência; diferenças pequenas não demonstram superioridade.
- **Concordância:** concordar não é acertar; discordar não revela por si só diferença de definição. Falta separar instabilidade interna e mudança de amostra nos novos ensaios.
- **Biologia:** SNPs são simulados; não há validação molecular de pares reais neste piloto.
- **Nativo versus operacionalização:** o RPF fornece componentes; a variância escolhida para ordená-los é um resumo nosso. iRF/siRF foram reduzidos a pares. A régua externa não exige saída nativa de interação.

## Ensaios A–D: situação e escopo

Na consulta local de 19/11 existe `extensao_AD/` com configurações, seleções de subconjuntos, scripts de tarefas/permutação e executores da régua. Não foram localizados nessa pasta relatório final ou figuras finais. Portanto, **há implementação preparatória identificada; não há conclusão A–D comprovada por esses artefatos**. Um snapshot do código está anexado com esse rótulo.

- **A — previsão:** diferenças pareadas, margens de semelhança justificadas e referências constantes.
- **B — régua comum:** ΔA, ΔAB e contraste I salvos separadamente; importância conjunta não chamada automaticamente de interação; permutações idênticas entre linguagens.
- **C — concordância e estabilidade:** comparar métodos sob a mesma régua e comparar ajustes do mesmo método; top-3 principal e sensibilidades; tratamento explícito de empates.
- **D — gabarito:** caracterizar se os consensos recuperam o par do gerador ou pares de efeitos individuais; não exigir que ΔAB seja detector de não aditividade.

A análise de escala, os dados semissintéticos e a interpretação biológica permanecem propostas posteriores. O fundamento da régua externa é a dependência preditiva do modelo; esta comparação não implementa a model class reliance inteira de [Fisher, Rudin e Dominici (2019)](https://www.jmlr.org/papers/v20/18-760.html).

## Referências e crédito

1. Wright MN, Ziegler A, König IR (2016). DOI 10.1186/s12859-016-0995-8. Texto, quatro figuras principais, suplementos e código examinados. Figuras reproduzidas sem redesenhar os valores; páginas suplementares apenas rasterizadas para leitura. [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
2. Fisher A, Rudin C, Dominici F (2019). *All Models are Wrong, but Many are Useful*. JMLR 20(177), [artigo](https://www.jmlr.org/papers/v20/18-760.html). Fundamenta a avaliação de dependência de modelos, não garante identidade entre essa teoria e o contraste I.
3. Documentação dos pacotes e versões: [registro de execução](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/DECISOES.md). Não se substituem versões efetivas por padrões atuais de websites.
4. Os scripts e tabelas do projeto são evidência da implementação, não prova independente das explicações causais dadas no relatório histórico.

**Histórico desta página:** 19/11/2026 — documentação integral com Etapa 0, Etapa 1, dados/output por campo, galeria original, atlas do suplemento, decisões, auditoria de empates e plano A–D. Sem retreino e sem publicação de credenciais.

## Detalhes operacionais adicionais e custos

O orçamento inicial era 150 CPU-h. O registro do subconjunto informa 38,7 CPU-h da execução principal, cerca de 25,5 CPU-h do diagnóstico JVIMP e aproximadamente 65 CPU-h acumuladas com instalações/pilotos. A projeção inicial da Etapa 0 completa ultrapassava esse teto. A mudança para scavenger foi autorizada no registro; não confundir “não debita a cota dessa conta” com “não consome recursos computacionais”.

O piloto da Etapa 1 registrou cerca de 25 minutos por realização em R e 1,3 minuto em Python, projetando aproximadamente 870 CPU-h para 2.000 realizações. **Isso é projeção, não medição final consolidada.** Não inferimos custo final apenas da duração de parede ou do número máximo de tarefas solicitadas. A primeira tentativa de submissão com apenas `--partition=scavenger` foi reescrita para a fila comum; D8 registra cerca de 2,2 CPU-h consumidas nessa tentativa e correção com conta/QOS apropriadas.

A execução usa blocos de dez realizações por tarefa na Etapa 0 e cinco na Etapa 1. Arquivo existente por repetição permite retomar. Uma tarefa “COMPLETED” só informa término do processo; integridade científica exige verificar quantidade de linhas, valores finitos e chaves. As 1.440 tarefas da reprodução completa correspondem a duas rodadas de 720 tarefas; não são 1.440 cenários.

No NID, foi necessário usar a classe MLP do demo para compatibilidade com `get_weights`; a rotina alternativa do repositório tinha nomes de camadas incompatíveis. Foi instalado R.utils para leitura dos arquivos gzip. A sensibilidade do IF com 20.000 árvores foi sugerida, mas não há resultado final dela no snapshot. As alterações de compilação C da biblioteca histórica e os reenvios detalhados permanecem no registro D6–D10.

### O que significa ausência de um output

Não há lista consolidada de todos os pesos de rede, árvores completas, curvas de calibração, intervalos pareados finais, p-valores de interação ou certificados de equivalência nesta rodada. Não são resultados negativos: são outputs não produzidos/preservados no material consultado. A documentação não preenche essas lacunas com valores estimados ou explicações presumidas.


---
Snapshot das evidências: [`edcbf4cc4505`](https://github.com/danifilho/Mestrado_ICMC/commit/edcbf4cc450583364e69cbe89a738596c7c2762f). Documentação publicada em 19/11/2026.
