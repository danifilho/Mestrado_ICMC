# IF, iRF, RSRF e PRF — o que cada algoritmo chama de interação

**Revisão e documentação: 18/11/2026 (America/Sao_Paulo).** Revisão das fontes primárias identificadas abaixo. Resultados atribuídos aos autores; não são novas execuções do projeto. O objetivo é explicar a definição operacional, o procedimento de busca e a evidência apresentada para cada método.

## Fontes e versões usadas

| Método | Artigo | Texto efetivamente conferido |
|---|---|---|
| IF | Hornung e Boulesteix. *Interaction forests: Identifying and exploiting interpretable quantitative and qualitative interaction effects*. CSDA 171, 107460 (2022). [DOI](https://doi.org/10.1016/j.csda.2022.107460) | [Manuscrito dos autores, Technical Report 237](https://epub.ub.uni-muenchen.de/75432/1/TR.pdf), disponibilizado em 2021. As seções e números de tabelas de IF nesta página referem-se a **essa versão** |
| iRF | Basu, Kumbier, Brown e Yu. *Iterative random forests to discover predictive and stable high-order interactions*. PNAS 115, 1943–1948 (2018). [DOI](https://doi.org/10.1073/pnas.1711236115) | [Manuscrito e suplemento, arXiv v4](https://arxiv.org/pdf/1706.08457v4) |
| RSRF: fundamento | Blum, Hiabu, Mammen e Meyer. *Consistency of Random Forest Type Algorithms under a Probabilistic Impurity Decrease Condition* | [arXiv:2309.01460v2, 20/02/2024](https://arxiv.org/html/2309.01460v2), especialmente §3 |
| RSRF: avaliação empírica | Mesmos autores. *Pure interaction effects unseen by Random Forests*. CSDA 212, 108237 (2025). [DOI](https://doi.org/10.1016/j.csda.2025.108237) | [arXiv:2406.15500v2, 01/08/2025](https://arxiv.org/pdf/2406.15500v2) |
| PRF | Hiabu, Mammen e Meyer. *Random Planted Forest: A Directly Interpretable Tree Ensemble* | [arXiv:2012.14563v3, submetida em 03/08/2023](https://arxiv.org/pdf/2012.14563v3). A primeira página do PDF traz 04/08/2023 |

**Nomenclatura:** PRF é a abreviação usada na conversa; o trabalho usa **Random Planted Forest**, `rpf`, e o pacote `randomPlantedForest`. Esta página trata desse método. Não atribuímos às versões dos artigos funcionalidades que apareçam apenas em versões posteriores de pacotes.

## 1. Mapa das diferenças

| Método | Objeto procurado ou representado | Como o encontra | Resultado diretamente interpretável |
|---|---|---|---|
| IF | Modificação da intensidade ou do sentido do efeito entre duas variáveis | Cortes que examinam duas variáveis; importância por tipo de efeito | Ordenações EIM quantitativa e qualitativa |
| iRF | Conjuntos de variáveis recorrentes em caminhos preditivos | Reponderação de RF, interseções aleatórias e bootstrap | Conjuntos candidatos e estabilidade |
| RSRF | Estruturas de regressão que incluem interações sem efeito marginal isolado | Escolha de uma sequência de cortes pela melhora conjunta | Preditor; o estudo empírico compara erros de previsão |
| PRF/RPF | Componentes funcionais dependentes de subconjuntos de variáveis | Crescimento de árvores plantadas com ajuste dos resíduos | Previsão decomposta em componentes de ordem limitada |

A interpretação comparativa desta página é: **um ranking de pares, uma lista de conjuntos estáveis, um bom preditor e uma decomposição funcional não são o mesmo produto**. Antes de comparar métodos como “detectores”, é necessário definir qual desses produtos será comparado e como será avaliado.

## 2. IF — Interaction Forests

### O que significa interação

Uma interação **quantitativa** muda a intensidade do efeito de uma variável conforme o valor da outra; uma **qualitativa** muda seu sentido. O método representa essas situações com cortes bivariados específicos. A EIM mede quanto determinado tipo de efeito contribui para a previsão. O artigo abrange desfechos categóricos, contínuos e de sobrevivência. [IF, §§1 e 3](https://epub.ub.uni-muenchen.de/75432/1/TR.pdf).

**Exemplos didáticos próprios, não resultados dos artigos:** imagine que aumentar A eleve a resposta em 2 unidades quando B é baixo, mas em 8 quando B é alto: muda a intensidade. Se aumentar A elevar a resposta com B baixo e diminuí-la com B alto, muda o sentido. Em ambos os casos é necessário definir a escala da resposta. Esses exemplos não identificam uma relação causal entre A e B.

### Como busca e atribui importância

1. Sorteia pares de variáveis e limiares candidatos.
2. Compara partições univariadas e bivariadas; estas incluem quatro formas quantitativas e uma qualitativa.
3. Seleciona cortes pelo critério preditivo e combina árvores.
4. Calcula EIM comparando previsão OOB com encaminhamento aleatório proporcional ao tamanho dos nós, aplicado aos cortes do efeito avaliado.
5. Ajusta a EIM quantitativa para reduzir confusão com efeitos individuais fortes. [IF, §§3.2–3.3](https://epub.ub.uni-muenchen.de/75432/1/TR.pdf).

**Como interpretar uma saída:** um par bem colocado é candidato a um tipo de efeito importante para o modelo. Não se deve ler “EIM = 0,3” como “30% de probabilidade de interação biológica”. A ordenação precisa ser acompanhada da forma estimada da resposta conjunta e de controles adequados à pergunta científica.

### Experimentos e resultados conferidos

O manuscrito separa **previsão em dados reais** de **recuperação de efeitos conhecidos em simulação**. [IF, §4](https://epub.ub.uni-muenchen.de/75432/1/TR.pdf).

| Elemento | Desenho confirmado |
|---|---|
| Estudo real | 220 conjuntos; classificação binária; validação estratificada de cinco folds repetida cinco vezes |
| Comparadores de previsão | RF, canonical correlation forests, oblique random forests, rotation forests |
| Métricas | ROC-AUC, acurácia, Brier |
| Simulação | 68 variáveis contínuas; 50 sem efeito; efeitos individuais, quantitativos e qualitativos em três intensidades |
| Repetições | 200 conjuntos para cada n = 100, 500, 1.000 |
| Comparadores de ranking | PA, IMDMS, iRF e RF-V-pairs |

**Recorte numérico da Tabela 1, versão TR237:** mediana entre conjuntos — não desempenho em um único dataset nem intervalo de confiança.

| Método | ROC-AUC | Acurácia | Brier ↓ |
|---|---:|---:|---:|
| IF | 0,9182 | 0,8822 | 0,0890 |
| RF | 0,9140 | 0,8787 | 0,0923 |

**Recorte da Tabela 4:** para interação quantitativa forte e n=500, a posição mediana foi 1 para IF-EIM-quant, 11 para PA e 22 para IMDMS; posições menores são melhores. O resultado é de recuperação do efeito simulado, não de validação biológica. [IF, Tabelas 1 e 4](https://epub.ub.uni-muenchen.de/75432/1/TR.pdf).

**Cuidados na comparação:** o estudo de rankings adapta a saída do iRF, tratando pares não retornados como posições ausentes; portanto, a mediana de posição do iRF não resume sua cobertura. O manuscrito também alerta que nem todos os 220 datasets são independentes. [IF, §§4.1.3 e 4.2.1](https://epub.ub.uni-muenchen.de/75432/1/TR.pdf).

**Limite documentado:** EIM é exploratória; o manuscrito não fornece teste de significância da EIM. Mesmo sem interações, algum par ocupará a primeira posição. [IF, §3.4](https://epub.ub.uni-muenchen.de/75432/1/TR.pdf).

## 3. iRF — iterative Random Forests

### O que significa interação e como busca

O alvo operacional é um **conjunto de variáveis recorrente em caminhos de decisão associados à classe**. O procedimento:

1. Ajusta RF inicialmente com pesos iguais.
2. Repondera a escolha das variáveis usando importância da iteração anterior.
3. Extrai conjuntos de variáveis dos caminhos até as folhas.
4. Usa Random Intersection Trees para procurar subconjuntos recorrentes.
5. Repete a extração em amostras bootstrap e calcula a proporção de repetições que retornam cada conjunto. [iRF, §2 e algoritmo suplementar](https://arxiv.org/pdf/1706.08457v4).

A estabilidade é uma frequência de seleção, não a probabilidade de verdade biológica. O conjunto pode ter dois ou mais fatores. Coocorrer num caminho também não demonstra, por si só, um efeito não aditivo isolado dos efeitos individuais.

**Exemplo didático próprio:** caminhos {A,B,C}, {A,B,D} e {A,B,E} têm interseção {A,B}. Isso explica a operação de interseção. Não basta fazer essa conta em três caminhos para reproduzir iRF: faltam o ajuste supervisionado, a amostragem dos caminhos e a avaliação de estabilidade.

### Experimentos do artigo

| Experimento | Dados e desenho | Resultado reportado |
|---|---|---|
| Simulações | Sete modelos com regras AND, OR e XOR; variações de tamanho, dimensionalidade e ruído | Recuperação de regras até ordem 8 em cenários em que RF recuperava pouco além de pares |
| Drosophila | 7.809 regiões; 3.912 treino / 3.897 teste; previsão de atividade de enhancer | AUC-PR = 0,50, K=5 |
| Splicing humano | 23.823 éxons; 11.911 treino / 11.912 teste | AUC-PR = 0,51, K=2 |

As entradas biológicas são medidas experimentais, incluindo ChIP, e a resposta é atividade regulatória ou inclusão de éxons; não são anotações GO. Nos dados reais, K foi selecionado por validação cruzada. No caso do splicing, o suplemento reporta AUC-PR para a classe 0, minoritária (S3.2). As medidas AUC-PR acima são as reportadas no artigo, não uma declaração de identidade numérica com qualquer implementação de AP. [iRF, §§2.3–5](https://arxiv.org/pdf/1706.08457v4).

### O significado dos “80%” e a relação com nosso teste

O suplemento lista vinte pares de TFs com estabilidade >0,5. Para dezesseis, os autores apontam trabalhos anteriores compatíveis com um fator regular a expressão do outro ou com ligação conjunta associada à expressão de alvos. Os quatro restantes têm traço na referência. Isso é **suporte bibliográfico para 16/20 pares selecionados**, não “80% de acurácia” de um classificador de interações. [iRF, S4/Tabela S1](https://arxiv.org/html/1706.08457v4).

No nosso [teste S1](Drosophila-IF-iRF-Tabela-S1), os vinte pares são uma referência fixa para contar correspondências. A decisão de incluir todos os vinte e usar top 10 pertence ao projeto. A origem da referência deve ser lembrada ao interpretar a vantagem de iRF sobre outros métodos na recuperação dessa lista.

## 4. RSRF — Random Split Random Forests

### A pergunta que motivou o método

RSRF foi introduzido no trabalho teórico de Blum e colaboradores para ampliar a classe de funções coberta por resultados de consistência, incluindo certos casos de interação pura. **Consistência é uma propriedade assintótica sob condições**, não garantia de recuperar todos os pares numa amostra finita. [Fundamento de RSRF, §3](https://arxiv.org/html/2309.01460v2).

O estudo empírico examina situações em que a resposta depende conjuntamente de variáveis que não oferecem sinal marginal suficiente para um corte isolado. O método olha além desse primeiro corte. [Estudo empírico, §2](https://arxiv.org/html/2406.15500v2).

### Como constrói a árvore

Em cada célula, sorteia um primeiro corte; faz um corte CART em cada filha; avalia a redução de impureza conjunta das quatro células. Repete isso para W candidatos e escolhe o melhor. Pode incluir um candidato CART–CART. Depois repete nas novas células. [Fundamento, §3.1](https://arxiv.org/html/2309.01460v2).

**Exemplo didático próprio:** para A e B independentes, com valores −1/+1 equiprováveis, defina Y=A×B. A média de Y para A=−1 e A=+1 é zero; o mesmo ocorre para B. Um corte isolado não separa médias. Ao separar também B dentro de cada grupo de A, aparecem quatro combinações com respostas distintas. Esse cálculo ilustra por que avaliar uma sequência pode revelar sinal escondido do primeiro passo. Não é uma afirmação de que qualquer implementação terá recuperação perfeita nesse exemplo com ruído.

### Avaliação empírica e resultados

O artigo de 2025 compara RSRF, IF, RF e Extremely Randomized Trees (ET): 100 simulações, 500 observações de treino e 500 pontos independentes de teste; cinco modelos; busca de 200 configurações de parâmetros por CV de dez folds e comparação adicional com parâmetros escolhidos em simulações independentes. MSE é calculado contra a função geradora, sem adicionar ruído ao alvo do teste. [Estudo empírico, §3](https://arxiv.org/html/2406.15500v2).

| Cenário pure-3, d=6; Tabela 3 | MSE médio | Desvio-padrão |
|---|---:|---:|
| IF | 0,154 | 0,029 |
| RSRF | 0,190 | 0,030 |
| RF | 0,510 | 0,062 |
| ET | 0,418 | 0,049 |

Não são IC95%. Esse recorte demonstra vantagem preditiva naquele cenário, não precisão de uma lista de pares.

Dados reais: concrete (1.030), airfoil (1.503), abalone (4.177), robot (8.192), california housing (20.640). Validação aninhada 5×5, repetida duas vezes; também versões com 50 covariáveis de ruído. IF/RSRF tiveram vantagens em parte das bases, sem vitória universal. Abalone é biológico, mas mede características do animal, não genética molecular. [Estudo empírico, §4](https://arxiv.org/html/2406.15500v2).

**Implicação para o projeto:** não há aqui uma taxa publicada de confirmação biológica de pares RSRF. Transformar suas árvores numa lista de interações exigiria definir e avaliar um procedimento de extração; não é a mesma avaliação que comparar MSE.

## 5. PRF/RPF — Random Planted Forest

### O que representa e como cresce

O modelo estima uma soma de componentes dependentes de subconjuntos de variáveis, limitados pela ordem máxima r. Com r=1, o modelo é aditivo; r=2 permite termos de pares. Ao introduzir nova variável num corte, preserva a folha anterior e acrescenta componentes; ao refinar uma variável já usada, substitui a folha. Escolhe cortes pelo ajuste dos resíduos e agrega árvores bootstrap. [PRF, condição BI(r) e §2](https://arxiv.org/pdf/2012.14563v3).

A decomposição precisa de restrições de identificação para separar componentes de modo único; a previsão total pode permanecer igual. O suplemento discute normalização/purificação. [PRF, apêndice A.8](https://arxiv.org/pdf/2012.14563v3#page=31).

**Exemplo algébrico próprio:** se uma previsão for escrita como fA(A)+fAB(A,B), podemos somar h(A) ao primeiro termo e subtrair h(A) do segundo sem mudar a previsão. Portanto, não basta encontrar um componente chamado “AB” e declarar que toda sua variação é interação pura. É preciso saber como o modelo separa os efeitos. Essa questão importa quando quisermos comparar uma superfície PRF com uma EIM ou uma estabilidade iRF.

### Experimentos e resultados

Doze cenários combinam estruturas aditivas, interações hierárquicas ou puras, esparsidade/densidade e funções suaves/com saltos. Cada cenário usa 100 repetições, n=500, ruído normal e 500 pontos independentes para MSE contra a função verdadeira. Há configurações pré-escolhidas e versões CV. Comparadores incluem RF, XGBoost, BART, MARS, GAM e smooth backfitting. [PRF, §3, Tabelas 1–2 e apêndice C](https://arxiv.org/pdf/2012.14563v3).

**Recortes do suplemento, d=30; MSE médio (desvio-padrão):**

| Método | Hierárquico esparso suave — Tabela 7 | Puro esparso suave — Tabela 8 |
|---|---:|---:|
| RPF, máximo 2 | 0,408 (0,070) | 1,822 (0,208) |
| RPF-CV | 0,463 (0,083) | 1,313 (0,253) |
| RF | 0,671 (0,080) | 1,295 (0,317) |
| BART-CV | 0,315 (0,047) | 0,223 (0,025) |

As tabelas não autorizam declarar PRF vencedor geral. O trabalho também apresenta resultados teóricos para uma versão idealizada. [PRF, §§3–4 e Tabelas 7–8](https://arxiv.org/pdf/2012.14563v3#page=34).

**Implicação para o projeto:** a decomposição é útil para visualizar como a previsão depende das combinações. Esses resultados sintéticos não constituem validação de mecanismos biológicos. A avaliação publicada de previsão também não equivale automaticamente a medir precisão/recall dos subconjuntos recuperados.

## 6. O que podemos concluir para a comparação do mestrado

Esta é uma síntese metodológica nossa, apoiada nas diferenças documentadas acima:

- **Previsão:** comparar o mesmo alvo, nas mesmas partições, com a mesma métrica. Uma diferença de MSE não pode ser colocada ao lado de uma porcentagem de suporte bibliográfico como se fossem medidas equivalentes.
- **Identificação:** definir unidade e saída — pares nativos, projeções de conjuntos maiores, componentes funcionais ou escore derivado de uma árvore. Registrar cobertura: “não retornado” e “baixo no ranking” não são necessariamente a mesma coisa.
- **Estabilidade:** mudar a semente e mudar os dados são perturbações distintas. Estabilidade interna do iRF e Jaccard entre duas listas respondem a perguntas diferentes.
- **Biologia:** em simulações há uma função conhecida; em dados reais, geralmente não existe uma lista completa de verdadeiros e falsos pares. Suporte experimental localizado, ausência de referência e recuperação de uma lista publicada devem permanecer separados.

Assim, a pergunta “os algoritmos encontram as mesmas interações?” exige antes explicitar **que objeto cada algoritmo fornece**. A comparação pode ser informativa justamente porque eles priorizam objetos distintos, desde que a conversão para uma unidade comum seja descrita e testada.

## 7. Registro da conferência

Foram consultados os textos integrais nas versões indicadas, com leitura das seções de método, desenho experimental, resultados e limitações usadas nesta página. Os recortes numéricos de IF, RSRF e PRF foram conferidos nas tabelas; os números iRF foram conferidos nos estudos de caso e no suplemento. Não foi realizada nova execução dos algoritmos.

As referências foram mantidas junto às afirmações. O manuscrito IF tem paginação própria, incluindo uma capa institucional; os números de páginas PDF podem diferir dos números impressos. Para evitar ambiguidade, citamos seções e tabelas e identificamos a versão. Não apresentamos o manuscrito TR237 como se fosse uma conferência integral da edição diagramada de 2022.

**Histórico:** 18/11/2026 — página criada a pedido do pesquisador para revisão comparativa dos quatro métodos, separada da documentação experimental de Drosophila.
