# Artefatos — comparação exploratória de detectores com a Tabela S1 do iRF

Documentado em 17/11/2026 (America/Sao_Paulo). Ajustes originais executados em 17/11/2026 segundo os registros do experimento `detectores_regulacao_drosophila_v1`. Esta publicação recalcula interseções e figuras a partir de saídas existentes; não reexecuta modelos.

## Reproduzir as figuras

Com Python, numpy, pandas e matplotlib instalados, execute `python gerar_figuras.py` nesta pasta. O script lê `dados/`, gera PNG e SVG em `figuras/`, a tabela `dados/recuperacao_S1.csv`, as posições da semente 2026 e um manifesto SHA-256. Não há chamadas à rede nem treinamento.

Os rankings são cópias das seis colunas de identificação, escore, posição e empate das saídas locais. Categorias da revisão bibliográfica anterior foram deliberadamente omitidas, pois não definem o resultado aqui. `tabela_S1.csv` transcreve os 20 pares, estabilidades e referências indicadas pelos autores. Os outros CSV preservam métricas do experimento original. As cópias de PROTOCOLO.md e DECISOES.md são registros históricos: contêm análises bibliográficas e controles mais amplos que a comparação S1 apresentada na nova página.

## Escopo e verificação

- Contagens de recuperação calculadas novamente dos 15 rankings (cinco listas × três sementes).
- Top 10 conferido contra a coluna `na_tabela_S1` da revisão anterior: todas as 15 contagens coincidem.
- 20 pares únicos na referência; listas de posições conferidas nos arquivos.
- Jaccard e intervalos de previsão são métricas preservadas, não recalculadas dos ajustes brutos nesta publicação.
- A comparação S1 é uma análise exploratória posterior, autorizada pelo pesquisador. Todos os 20 pares são incluídos, mesmo os quatro sem referência bibliográfica indicada.
- A ausência na S1 não é um negativo biológico. A referência foi selecionada originalmente pelo iRF.
- Este pacote reproduz as figuras e contagens da página, não o treinamento completo no HPCC.

## Paleta

Verde escuro #14532D, verde médio #15803D, verde claro #86BF91, fundo suave #E7F3E8, texto #18352B, neutro #E9ECE9. `paleta.json` contém os valores. Barras usam padrões; matrizes têm valores escritos; ausência tem cinza e travessão. Cor não codifica comprovação biológica.

## Fontes

- Basu et al. (2018), DOI https://doi.org/10.1073/pnas.1711236115. Lista publicada: suplemento S4/Tabela S1, disponível também em https://arxiv.org/pdf/1706.08457v4. Suplemento e trechos pertinentes consultados nesta conversa; sem nova validação das referências biológicas individuais.
- Dados dos autores: https://doi.org/10.5281/zenodo.1401347.
- Hornung e Boulesteix (2022), DOI https://doi.org/10.1016/j.csda.2022.107460. Definições e configuração de IF conforme protocolo preservado.
- Arquivos locais do experimento: rankings, estabilidade, concordância, previsão, diferenças pareadas e reprodução S1. Fonte da decisão: conversa do pesquisador autorizando o uso dos 20 pares e a publicação na Wiki.
