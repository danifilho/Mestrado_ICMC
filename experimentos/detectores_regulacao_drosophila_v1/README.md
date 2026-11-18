# Código de origem da comparação exploratória com a Tabela S1

**Publicação: 18/11/2026. Ajustes originais: 17/11/2026.** Este é um recorte do experimento local, restrito às saídas que sustentam a última comparação com os 20 pares da Tabela S1 e suas cinco figuras verdes. Não inclui as figuras nem a avaliação bibliográfica dos testes anteriores.

## Onde está cada coisa

| Etapa | Código | Entradas → saídas |
|---|---|---|
| Construir grupos e partições | `scripts/01_auditar_preparar.py` | Dados dos autores → `data/processed/` e auditoria |
| Configurar execuções | `scripts/02_tarefas.py`, `configs/metodos.json`, `configs/execucao.json` | Configurações → JSON por tarefa |
| Ajustar IF, iRF e RF | `src/executar_tarefa.R`, `src/metodos.R` | Tarefa e matrizes → previsões, escores nativos e `info.json` |
| Converter escores em pares de fatores | `src/rankings.py` | EIM, conjuntos iRF, importâncias e X → rankings |
| Conferir análises que sustentam as figuras | `scripts/verificar_analise_s1.py` | Saídas dos ajustes → recálculo e conferência de 115 rankings, Jaccard@10, AP e IC95% |
| Contar correspondências à S1 e gerar as cinco figuras verdes | [gerar_figuras.py](../../wiki/assets/drosophila-s1/gerar_figuras.py) | 20 pares, rankings e métricas → contagens e PNG/SVG |

`resultados/brutos/principal/` contém CSV/JSON de previsões e escores, não modelos serializados. `resultados/rankings/` não inclui categorias bibliográficas. `resultados/metricas/` contém os números apresentados. `resultados/brutos/oficial/` e a tabela de reprodução registram a comparação secundária com a divisão dos autores. Os arquivos de configuração preservam opções do estudo de origem, mas esta publicação não executa nem apresenta as análises bibliográficas anteriores.

## 1. Refazer as figuras (sem treinar)

Na raiz do repositório:

```sh
python3 -m pip install numpy pandas matplotlib
python3 wiki/assets/drosophila-s1/gerar_figuras.py
```

O script recalcula as interseções com a S1 e as posições, e escreve as cinco figuras PNG/SVG, tabelas e manifesto em `wiki/assets/drosophila-s1/`. Não consulta literatura. Jaccards e IC são lidos das tabelas preservadas. Todos os 20 pares entram, inclusive os quatro sem referência indicada pelos autores.

## 2. Conferir de onde vieram as métricas

Na raiz do repositório:

```sh
python3 -m pip install numpy pandas scipy scikit-learn
python3 experimentos/detectores_regulacao_drosophila_v1/scripts/verificar_analise_s1.py
```

Esta rotina foi acrescentada para documentação em 18/11; não é um novo experimento. Recalcula, sem sobrescrever os resultados, os cinco rankings em três sementes e 20 subamostras; as médias e extremos do Jaccard@10; as concordâncias entre métodos; AP das previsões; e os dois intervalos por 2.000 reamostragens pareadas de grupos do teste. Usa as mesmas regras da análise original. Uma divergência interrompe com erro. As contagens S1 são recalculadas separadamente pelo gerador das figuras.

## 3. Treinar novamente (requer R)

Ambiente usado: R 4.4.3, iRF 2.0.0, diversityForest 0.6.0, ranger 0.18.0, data.table e jsonlite. Versões completas: `environments/hpcc_versoes.txt`. Instale essas versões e suas dependências; os pacotes não estão embutidos no repositório. Uma versão diferente pode gerar resultados diferentes. Não houve treinamento novo nesta publicação.

Dentro da pasta deste estudo:

```sh
export ESTUDO_RAIZ="$PWD"
export IRF2_LIB="/seu/caminho/biblioteca-R-iRF2"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
python3 scripts/02_tarefas.py principal
Rscript src/executar_tarefa.R resultados/logs/tarefas/principal/if_completo_s2026.json
```

Esse último comando executa somente uma tarefa. A lista completa fica em `resultados/logs/tarefas/principal/lista.txt`: 3 métodos × (3 sementes + 20 subamostras) = 69 tarefas. Para a divisão dos autores, use a etapa `oficial` (três tarefas). Faça novas execuções numa cópia separada: o executor grava sobre a pasta de saída indicada no JSON.

No Slurm, `scripts/rodar_array.sb` é o modelo histórico: adapte `/CAMINHO/HPCC`, biblioteca, ambiente e partição. A etapa principal usa array 1–69 e `ETAPA=principal`. Não há submissão automática nesta publicação.

## 4. Dados e limites de reprodução

As matrizes, respostas, partições, identificadores, subamostras e mapeamento de colunas estão em `data/processed/`. `data/raw/irfSuppData1.csv` é o dado processado dos autores usado na análise oficial. Fonte: [Zenodo do estudo iRF](https://doi.org/10.5281/zenodo.1401347); proveniência registrada em `data/manifest.json`.

Para refazer a auditoria 01 desde a origem, também são necessários `enhancer.Rdata` e os demais arquivos do pacote dos autores em `data/raw/`, além da cópia histórica `../comparacao_preditores_v1/data/`, usada pelo script para conferir igualdade entre estudos. Esses arquivos auxiliares não estão incluídos neste recorte. A reexecução dos modelos pode partir diretamente das matrizes publicadas; isso não refaz a auditoria inicial.

O código da coleta/avaliação bibliográfica anterior não participa da análise S1 e não foi incluído. A lista S1 é uma referência publicada, não um conjunto completo de interações verdadeiras e falsas.

## Proveniência

`MANIFESTO_PUBLICACAO.json` liga arquivos importados aos hashes locais originais e publicados. Caminhos pessoais foram substituídos por `/CAMINHO/LOCAL` e `/CAMINHO/HPCC`; nomes dos nós foram removidos de `info.json`; categorias bibliográficas foram removidas dos rankings. As regras dos adaptadores originais não mudaram. Hashes de congelamento históricos referem-se à execução de origem, não à cópia higienizada. Nenhuma nova licença é atribuída aos dados ou pacotes de terceiros.

[Estudo e resultados na Wiki](https://github.com/danifilho/Mestrado_ICMC/wiki/Drosophila-IF-iRF-Tabela-S1) · [Guia detalhado das cinco figuras](https://github.com/danifilho/Mestrado_ICMC/wiki/Drosophila-S1-Guia-das-figuras)
