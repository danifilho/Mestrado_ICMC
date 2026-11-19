# PROTOCOLO — Piloto 7: reprodução de Wright et al. (2016) e extensão com detectores de interação

> **Registro:** este é o texto colado pelo pesquisador em 18/11/2026, mantido sem alterações. Ele termina na seção 5.3; a Etapa 2 não estava no texto recebido. Conferências e decisões ficam em `DECISOES.md`.

Status: rascunho para revisão (Daniel e Prof. Cerri). Nada deve ser rodado antes de este documento ser congelado (scripts/congelar.py).

Referência-base: "Do little interactions get lost in dark random forests?" (Wright, Ziegler & König, 2016), BMC Bioinformatics 17:145, DOI 10.1186/s12859-016-0995-8. Todas as especificações abaixo marcadas [W] foram tiradas do texto do artigo; as marcadas [conferir] dependem dos arquivos adicionais ou de pacotes ainda não verificados.

## 1. Perguntas

| Código | Pergunta | Etapa |
|---|---|---|
| P0 | O nosso pipeline reproduz os resultados publicados de Wright et al. para as cinco medidas originais? | 0 |
| P1 | Com o mesmo desenho, como os detectores atuais (IF, iRF/siRF, RPF, RSRF, estatística H, Shapley, NID, EBM) se comparam, (a) pelos seus próprios rankings e (b) por uma régua global comum? | 1 |
| P2 | As conclusões mudam quando (a) a verdade é definida na escala logit ou na escala da probabilidade, e (b) a régua global usa log-loss ou acurácia? | 2 |

P0 é pré-requisito: P1 e P2 só são interpretadas se P0 passar.

## 2. Materiais de Wright et al.

| Item | Conteúdo [W] | Ação |
|---|---|---|
| Arquivo adicional 1 | versão do pacote ranger com a importância por permutação de pares (PPI) | download bloqueado no ambiente de verificação (HTTP 403); baixar pelo navegador |
| Arquivo adicional 2 | tabelas de penetrância de todos os modelos (S1–S20) | usar como verificação da simulação |
| Arquivo adicional 3 | código de reprodução (ZIP, 44 kB) | baixado e lido em 18/11/2026 (ver 2.1) |
| Arquivo adicional 4 | figuras de todos os cenários (S1–S110) | gabarito numérico da Etapa 0 |

URL dos arquivos: https://static-content.springer.com/esm/art%3A10.1186%2Fs12859-016-0995-8/MediaObjects/12859_2016_995_MOESM{1..4}_ESM.*

### 2.1 O que o código do Arquivo adicional 3 contém (verificado)

- **Pastas:** 01_main_simulation, 02_more_SNPs, 03_ld_simulation, 04_marginal_main, 05_marginal_more_SNPs, 06_marginal_ld; cada uma com problems.R (simulação), algorithms.R (medidas), simulate_snps.R e scripts de execução e gráficos.
- **Sementes:** semente mestra 12345 (set.seed e semente do registro do BatchExperiments). Cada tarefa recebe uma semente derivada da do registro.
- **Infraestrutura:** BatchExperiments/BatchJobs, com caminho fixo do cluster dos autores (/imbs/home/wright/batchjobs/registries). Ambos ainda estão no CRAN (BatchExperiments 1.4.4, set/2025; BatchJobs 1.10, set/2025), mas é preciso trocar o caminho e configurar o SLURM do HPCC.
- **Não foi executado aqui:** o ambiente de verificação não tem R. A execução fica para o smoke test no HPCC.

### 2.2 Obstáculos para reprodução numérica exata

- **Gerador de números aleatórios do R.** A simulação de genótipos usa sample(), cujo algoritmo mudou no R 3.6.0. Para recriar os mesmos dados de 2016 é preciso RNGkind(sample.kind = "Rounding").
- **PPI não existe no ranger atual.** O código chama importance = "pairwise", que não está no ranger 0.18.0 do CRAN (conferido no código-fonte). Depende da versão do Arquivo adicional 1, que pode não compilar com R atual.
- **Versões dos pacotes.** Mudanças internas de ranger e randomForestSRC desde 2016 alteram as florestas mesmo com dados idênticos.

Consequência: a meta é reprodução estatística (mesmo desenho, curvas dentro da variação de Monte Carlo), não numérica. Se a PPI original não compilar, reimplementá-la (permutação conjunta das duas colunas, queda de acurácia OOB), validá-la contra as figuras e registrar em DECISOES.md.

### 2.3 Diferenças entre o código e o texto do artigo (seguir o código)

| Item | Texto do artigo | Código |
|---|---|---|
| Modelos | 5 | 6: o "SNP modificador" aparece em duas versões (modifier_snp1, modifier_snp2) |
| Combinações de MAF | 2 × 2 = 4 | 3: (MAF_I, MAF_M) = (0,2; 0,2), (0,2; 0,4), (0,4; 0,2); não há (0,4; 0,4) |
| Número de cenários | 800 (= 160 × 5 medidas) | 6 × 2 × 2 × 3 = 72 desenhos de dados × 2 mtry = 144 cenários, × 5 medidas |
| Proporção de casos | "aproximadamente igual" | β0 calculado ignorando o termo de interação; proporção esperada varia de 0,34 a 0,57 entre cenários (calculado) |

Registrar essas diferenças em DECISOES.md antes de rodar.

## 3. Desenho de dados (idêntico a Wright et al.)

### 3.1 Estrutura de cada conjunto de dados [W]

- n = 1.000 indivíduos, desfecho caso/controle.
- 2 SNPs que interagem, 5 SNPs só com efeito marginal, 93 SNPs de ruído (100 SNPs).
- Genótipos codificados como número de alelos menores (0, 1, 2), em equilíbrio de Hardy–Weinberg (confirmado no código: probabilidades (1−p)², 2p(1−p), p²).
- Fenótipo por modelo logístico com efeitos aditivos na escala logit (confirmado em problems.R):
  logit P(caso) = β0 + β_M·(soma dos 5 SNPs marginais) + c1·x1 + c2·x2 + c12·x1·x2
- β0 = −logit(0,5) − 2·β_I·(2·MAF_I) − 5·β_M·(2·MAF_M) (fórmula do código; usa β_I nos dois SNPs de interação mesmo nos modelos em que o efeito marginal é 0).
- MAF dos SNPs de ruído ~ Uniforme(0, 1) (confirmado: runif(num_noise_snps)).

### 3.2 Os cinco modelos de interação (Tabela 1) [W]

| Modelo | c1 (SNP1) | c2 (SNP2) | c12 (SNP1×SNP2) |
|---|---|---|---|
| Só interação | 0 | 0 | β_I |
| SNP modificador | 0 | β_I | β_I |
| Sem interação | β_I | β_I | 0 |
| Redundante | β_I | β_I | −β_I |
| Sinérgico | β_I | β_I | β_I |

### 3.3 Parâmetros (Tabela 2) [W]

| Parâmetro | Valores |
|---|---|
| β_M (efeito dos SNPs marginais) | 0,4; 0,8 |
| β_I (efeito de interação) | 0,4; 0,8 |
| MAF_M | 0,2; 0,4 |
| MAF_I | 0,2; 0,4 |
| mtry | 10; 50 |

No texto do artigo: 5 modelos × 2⁵ combinações = 160 cenários (× 5 medidas = 800). No código, que é o que gerou as figuras: 6 modelos × 2 β_I × 2 β_M × 3 pares de MAF = 72 desenhos de dados × 2 mtry = 144 cenários, cada um com 100 repetições (ver 2.3). Este protocolo segue o código.

### 3.4 Cenários adicionais [W]

- 2 SNPs marginais em vez de 5.
- 2.493 SNPs de ruído (mtry = 50, β_M = β_I = 0,4, MAF_M = MAF_I = 0,2).
- Desequilíbrio de ligação: 1.000 SNPs do cromossomo 22 (1000 Genomes, fase 3; MAF 0,05–0,2), 100 sorteados por conjunto, haplótipos simulados com HapSim; β_M, β_I ∈ {0; 0,4; 0,8} conforme o artigo.

Prioridade: os cenários adicionais entram só depois de a reprodução principal passar.

### 3.5 Verificação da simulação (antes de qualquer floresta)

Reproduzir a Tabela 3 (Só interação, β_I = β_M = 0,4, MAF_I = 0,4, MAF_M = 0,2). Com o β0 do código (−1,44), as penetrâncias são médias sobre a soma dos 5 SNPs marginais (Binomial(10; 0,2)):

```python
import numpy as np
from math import comb
s = lambda z: 1 / (1 + np.exp(-z))
bI = bM = 0.4; mi, me = 0.4, 0.2
b0 = -2*bI*(2*mi) - 5*bM*(2*me)                                  # -1.44
pE = [comb(10, k) * me**k * (1-me)**(10-k) for k in range(11)]   # soma dos 5 SNPs marginais
for x1, x2 in [(0, 0), (1, 1), (2, 1), (2, 2)]:
    print(x1, x2, round(sum(pE[k] * s(b0 + bM*k + bI*x1*x2) for k in range(11)), 3))
# 0.353  0.443  0.537  0.712   (artigo: 0.35  0.44  0.54  0.72)
```

Critério: penetrâncias das Tabelas S1–S20 reproduzidas com erro ≤ 0,01 (a célula (2,2) acima difere em 0,008; registrar). Proporção de casos simulada dentro de ±0,02 da esperada pela fórmula do código em cada cenário (esperado entre 0,34 e 0,57).

## 4. Etapa 0 — Reprodução exata

### 4.1 Florestas [W]

- 500 árvores; mtry conforme o cenário; árvores de classificação crescidas até a pureza (padrão).
- ranger para Gini, permutação e PPI (versão do Arquivo adicional 1; ver 2.2).
- randomForestSRC::find.interaction com importance = "permute" e method = "maxsubtree" (JMST) ou method = "vimp" (JVIMP).
- Detalhes do código: para as medidas individuais, o posto registrado é o maior dos postos dos dois SNPs; a JVIMP usa o valor absoluto da coluna Difference; na JMST, valores menores indicam interação; os pares são restritos aos SNPs de interação e marginais.

### 4.2 Medidas [W]

| Medida | Tipo | Definição |
|---|---|---|
| Gini | individual | soma da redução de impureza nos nós que dividem pela variável |
| Permutação | individual | queda de acurácia OOB ao embaralhar a variável |
| PPI | par | queda de acurácia OOB ao embaralhar as duas variáveis juntas |
| JMST | par | média das profundidades mínimas normalizadas das subárvores maximais (xj, xi) e (xi, xj) |
| JVIMP | par | soma das importâncias individuais − importância conjunta (procedimento de "noising-up") |

### 4.3 Métricas [W]

- **Captura (individuais):** proporção das 100 repetições em que os 2 SNPs que interagem estão entre os k primeiros, k = 2, …, 10. Também: proporção com os 5 marginais entre os k primeiros, k = 5, …, 15.
- **Detecção (pares):** proporção das repetições em que o par verdadeiro está entre os k primeiros pares, k = 1, …, 10. Pares com SNPs de ruído são excluídos do ranking (ranking entre os 21 pares dos 7 SNPs não ruidosos). Também: proporção com os 10 pares de marginais entre os k primeiros, k = 10, …, 20.

### 4.4 Ordem de execução

1. Subconjunto: mtry = 50 e as quatro combinações das Figuras 3 e 4 (a–d) × 5 modelos = 20 cenários.
2. Se passar, os 144 cenários do código (ver 2.3).

### 4.5 Critério de reprodução (fixado antes)

- **Gabarito:** valores lidos das Figuras 3, 4 e S1–S48. A leitura dos gráficos é feita uma vez, antes de rodar, e salva em gabarito_wright.csv (com a imprecisão de leitura anotada).
- **Erro de Monte Carlo:** com 100 repetições, o erro-padrão de uma proporção é ≤ 0,05.
- **Critério:** passa se |nosso − publicado| ≤ 0,10 em pelo menos 90% dos pontos (cenário × medida × k), e nenhuma curva inverter a ordem relativa das medidas descrita no texto (ex.: Gini acima da permutação; detecção maior em "Sem interação" do que em "Só interação").
- **Reprodução numérica exata não é critério** (ver 2.2). Como verificação secundária, gerar os dados com a semente 12345, RNGkind(sample.kind = "Rounding") e a mesma ordem de tarefas do BatchExperiments, e reportar se os conjuntos de dados coincidem com os de 2016.

## 5. Etapa 1 — Mesmo desenho, detectores atuais

### 5.1 Detectores e como obter um ranking de pares

Situação verificada em 18/11/2026:

| Família | Detector | Ranking nativo de pares | Pacote e versão | Situação |
|---|---|---|---|---|
| Florestas para interação | Interaction Forests | EIM por par (quantitativa e qualitativa) | R diversityForest 0.6.0 (mai/2025), função interactionfor | removido do CRAN em 13/09/2026 (depende de MapGAM, também arquivado); instalar do arquivo do CRAN ou do GitHub do autor; fixar versão |
| | iRF | estabilidade dos conjuntos de tamanho 2 | R iRF 3.0.0, GitHub sumbose/iRF | removido do CRAN em 2022 (última no CRAN: 2.0.0); instalar com remotes::install_github("sumbose/iRF"); fixar commit |
| | siRF | estabilidade de interações com sinal | R iRF 2.0, GitHub karlkumbier/iRF2.0, argumento signed = TRUE | código existe; documentação não detalha a estabilidade do sinal; conferir no código |
| | Random Planted Forest | variância do componente fANOVA de cada par (após purify) | R randomPlantedForest 0.5.0.9000, r-universe plantedml (funções purify, predict_components) | não está no CRAN; instalar do r-universe; fixar commit (4c9c28e392 na verificação) |
| | RSRF | não tem ranking nativo; usar estatística H ou Shapley sobre o modelo | — | nenhum código público encontrado (artigo arXiv 2406.15500 v2 sem declaração de código); pedir aos autores ou reimplementar a partir da descrição; decidir antes de congelar |
| Independentes de modelo | Estatística H (Friedman & Popescu, 2008) | H² por par, sobre uma floresta padrão (ranger) | R hstats 1.2.2 (out/2025); alternativa iml 0.11.4 | disponível no CRAN |
| | Interações de Shapley | média do valor absoluto da interação por par | R treeshap 0.4.0 (abr/2026) | disponível; conferir se calcula interações para ranger |
| Redes neurais | NID (Tsang, Cheng & Liu, 2018) | pontuação de interação dos pesos | GitHub mtsang/neural-interaction-detection (demo.ipynb, PyTorch) | código existe, testado com PyTorch 1.3.1 / scikit-learn 0.21.3 / numpy 1.17.1; adaptar a versões atuais e registrar |
| Aditivos com pares | EBM (GA²M) | importância do termo de par selecionado | Python interpret 0.7.8 | disponível no PyPI |
| Referência | Gini, permutação | Etapa 0 | R ranger 0.18.0 (jan/2026) | disponível |
| | JMST, JVIMP | Etapa 0 | R randomForestSRC 3.10.0 (nov/2026) | disponível |
| | PPI | Etapa 0 | ranger do Arquivo adicional 1 | ausente do ranger atual; ver 2.2 |

Hiperparâmetros: padrões de cada pacote, com 500 árvores e o mtry do cenário onde se aplica. Nenhum ajuste fino por cenário. Registrar todas as versões.

### 5.2 Régua global (proposta do orientador)

Para cada modelo ajustado, em um conjunto de teste independente (n = 1.000, gerado do mesmo cenário, com semente própria):

- **Medida:** interação(A,B) = queda(A e B embaralhados juntos) − queda(só A) − queda(só B).
- **Permutações:** a mesma permutação é aplicada às duas colunas; média de 30 permutações.
- **Métricas:** log-loss (principal) e acurácia (secundária, para comparar com Wright).
- **Pares avaliados:** os 21 pares dos 7 SNPs não ruidosos, como em Wright.

Cada detector gera, portanto, dois rankings: nativo e régua global.

### 5.3 Métricas

- Curvas de detecção top-k (k = 1, …, 10), como na Etapa 0.
- Resumo: média da curva para k = 1, …, 10 (área normalizada).
- Taxa de "detecção" no modelo Sem interação, reportada separadamente (ver Etapa 2).
- Concordância entre detectores: interseção dos 3 primeiros pares e correlação de Kendall entre rankings.

*(fim do texto recebido)*
