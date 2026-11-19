# Piloto 7 — código, reprodução e inventário

[Principal](https://github.com/danifilho/Mestrado_ICMC/wiki/Piloto-7-Wright-Documentacao-integral) · [Dicionário semântico](https://github.com/danifilho/Mestrado_ICMC/wiki/Piloto-7-Dados-e-outputs)

Esta página vincula cada fonte e output ao snapshot documental. Os originais do experimento não foram modificados. Arquivos de execução podem conter caminhos do ambiente original; adapte os caminhos explicitamente antes de tentar reproduzir. Não há promessa de ambiente instalado idêntico neste repositório.

## Pipeline e comandos de análise

Descompacte os arquivos `resultados/*_brutos.tar.gz` dentro de `resultados/brutos/`. Os diretórios internos conservam os nomes que os analisadores esperam. Para analisar, use um ambiente com pandas, numpy e scipy; para figuras, matplotlib. R e os pacotes fixados são necessários somente para novos ajustes.

```bash
python scripts/03_comparar_etapa0.py completo --de etapa0_comp_rfsrc341
python scripts/03_comparar_etapa0.py completo --de etapa0_comp_rfsrc341 --jvimp-de etapa0_comp_rfsrc161
python scripts/05_analisar_etapa1.py etapa1
python scripts/06_figuras_etapa1.py
python auditoria/auditar_empates.py . auditoria
```

Esses comandos gravam tabelas/figuras: execute numa cópia de trabalho se quiser preservar o snapshot. **Não execute os geradores de tarefas como se fossem somente leitores:** eles removem JSONs da pasta de tarefas correspondente antes de recriá-los; `04_tarefas_etapa1.py` importa o gerador da Etapa 0 com efeitos colaterais.

## Códigos completos, não pseudocódigo


### scripts

- [scripts/00_verificar_simulacao.py](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/scripts/00_verificar_simulacao.py) — 59 linhas; fonte integral preservada.
- [scripts/01_gabarito_pdf.py](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/scripts/01_gabarito_pdf.py) — 138 linhas; fonte integral preservada.
- [scripts/02_tarefas_etapa0.py](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/scripts/02_tarefas_etapa0.py) — 48 linhas; fonte integral preservada.
- [scripts/03_comparar_etapa0.py](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/scripts/03_comparar_etapa0.py) — 90 linhas; fonte integral preservada.
- [scripts/04_tarefas_etapa1.py](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/scripts/04_tarefas_etapa1.py) — 36 linhas; fonte integral preservada.
- [scripts/05_analisar_etapa1.py](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/scripts/05_analisar_etapa1.py) — 91 linhas; fonte integral preservada.
- [scripts/06_figuras_etapa1.py](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/scripts/06_figuras_etapa1.py) — 178 linhas; fonte integral preservada.
- [scripts/congelar.py](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/scripts/congelar.py) — 35 linhas; fonte integral preservada.
- [scripts/rodar_array.sb](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/scripts/rodar_array.sb) — 18 linhas; fonte integral preservada.
- [scripts/rodar_array_scavenger.sb](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/scripts/rodar_array_scavenger.sb) — 21 linhas; fonte integral preservada.
- [scripts/rodar_etapa1.sb](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/scripts/rodar_etapa1.sb) — 28 linhas; fonte integral preservada.

### src

- [src/etapa0.R](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/src/etapa0.R) — 50 linhas; fonte integral preservada.
- [src/etapa1.R](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/src/etapa1.R) — 130 linhas; fonte integral preservada.
- [src/etapa1_py.py](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/src/etapa1_py.py) — 148 linhas; fonte integral preservada.

### extensao_AD/scripts

- [extensao_AD/scripts/01_gerar_permutacoes.py](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/extensao_AD/scripts/01_gerar_permutacoes.py) — 55 linhas; fonte integral preservada.
- [extensao_AD/scripts/02_tarefas.py](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/extensao_AD/scripts/02_tarefas.py) — 37 linhas; fonte integral preservada.
- [extensao_AD/scripts/03_subconjunto_sementes.py](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/extensao_AD/scripts/03_subconjunto_sementes.py) — 24 linhas; fonte integral preservada.
- [extensao_AD/scripts/lib_rankings.py](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/extensao_AD/scripts/lib_rankings.py) — 75 linhas; fonte integral preservada.
- [extensao_AD/scripts/rodar_ad.sb](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/extensao_AD/scripts/rodar_ad.sb) — 28 linhas; fonte integral preservada.
- [extensao_AD/scripts/teste_lib_rankings.py](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/extensao_AD/scripts/teste_lib_rankings.py) — 40 linhas; fonte integral preservada.

### extensao_AD/src

- [extensao_AD/src/regua_ad.R](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/extensao_AD/src/regua_ad.R) — 136 linhas; fonte integral preservada.
- [extensao_AD/src/regua_ad_py.py](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/extensao_AD/src/regua_ad_py.py) — 113 linhas; fonte integral preservada.

### fontes/codigo_autores

- [fontes/codigo_autores/replication/01_main_simulation/01_sim_main.R](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/fontes/codigo_autores/replication/01_main_simulation/01_sim_main.R) — 123 linhas; fonte integral preservada.
- [fontes/codigo_autores/replication/01_main_simulation/02_plot_main.R](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/fontes/codigo_autores/replication/01_main_simulation/02_plot_main.R) — 126 linhas; fonte integral preservada.
- [fontes/codigo_autores/replication/01_main_simulation/03_sim_fewer_marginal.R](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/fontes/codigo_autores/replication/01_main_simulation/03_sim_fewer_marginal.R) — 123 linhas; fonte integral preservada.
- [fontes/codigo_autores/replication/01_main_simulation/04_plot_fewer_marginal.R](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/fontes/codigo_autores/replication/01_main_simulation/04_plot_fewer_marginal.R) — 134 linhas; fonte integral preservada.
- [fontes/codigo_autores/replication/01_main_simulation/algorithms.R](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/fontes/codigo_autores/replication/01_main_simulation/algorithms.R) — 107 linhas; fonte integral preservada.
- [fontes/codigo_autores/replication/01_main_simulation/helper_functions.R](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/fontes/codigo_autores/replication/01_main_simulation/helper_functions.R) — 0 linhas; fonte integral preservada.
- [fontes/codigo_autores/replication/01_main_simulation/problems.R](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/fontes/codigo_autores/replication/01_main_simulation/problems.R) — 74 linhas; fonte integral preservada.
- [fontes/codigo_autores/replication/01_main_simulation/simulate_snps.R](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/fontes/codigo_autores/replication/01_main_simulation/simulate_snps.R) — 38 linhas; fonte integral preservada.
- [fontes/codigo_autores/replication/02_more_SNPs/01_sim_largep.R](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/fontes/codigo_autores/replication/02_more_SNPs/01_sim_largep.R) — 123 linhas; fonte integral preservada.
- [fontes/codigo_autores/replication/02_more_SNPs/02_plot_largep.R](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/fontes/codigo_autores/replication/02_more_SNPs/02_plot_largep.R) — 124 linhas; fonte integral preservada.
- [fontes/codigo_autores/replication/02_more_SNPs/algorithms.R](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/fontes/codigo_autores/replication/02_more_SNPs/algorithms.R) — 107 linhas; fonte integral preservada.
- [fontes/codigo_autores/replication/02_more_SNPs/helper_functions.R](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/fontes/codigo_autores/replication/02_more_SNPs/helper_functions.R) — 0 linhas; fonte integral preservada.
- [fontes/codigo_autores/replication/02_more_SNPs/problems.R](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/fontes/codigo_autores/replication/02_more_SNPs/problems.R) — 74 linhas; fonte integral preservada.
- [fontes/codigo_autores/replication/02_more_SNPs/simulate_snps.R](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/fontes/codigo_autores/replication/02_more_SNPs/simulate_snps.R) — 38 linhas; fonte integral preservada.
- [fontes/codigo_autores/replication/03_ld_simulation/01_prepare_1000g.R](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/fontes/codigo_autores/replication/03_ld_simulation/01_prepare_1000g.R) — 31 linhas; fonte integral preservada.
- [fontes/codigo_autores/replication/03_ld_simulation/02_sim_ld.R](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/fontes/codigo_autores/replication/03_ld_simulation/02_sim_ld.R) — 119 linhas; fonte integral preservada.
- [fontes/codigo_autores/replication/03_ld_simulation/03_plot_ld.R](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/fontes/codigo_autores/replication/03_ld_simulation/03_plot_ld.R) — 127 linhas; fonte integral preservada.
- [fontes/codigo_autores/replication/03_ld_simulation/04_compute_ld.R](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/fontes/codigo_autores/replication/03_ld_simulation/04_compute_ld.R) — 22 linhas; fonte integral preservada.
- [fontes/codigo_autores/replication/03_ld_simulation/algorithms.R](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/fontes/codigo_autores/replication/03_ld_simulation/algorithms.R) — 107 linhas; fonte integral preservada.
- [fontes/codigo_autores/replication/03_ld_simulation/helper_functions.R](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/fontes/codigo_autores/replication/03_ld_simulation/helper_functions.R) — 0 linhas; fonte integral preservada.
- [fontes/codigo_autores/replication/03_ld_simulation/problems.R](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/fontes/codigo_autores/replication/03_ld_simulation/problems.R) — 69 linhas; fonte integral preservada.
- [fontes/codigo_autores/replication/03_ld_simulation/simulate_ld_snps.R](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/fontes/codigo_autores/replication/03_ld_simulation/simulate_ld_snps.R) — 27 linhas; fonte integral preservada.
- [fontes/codigo_autores/replication/04_marginal_main/01_sim_marginal.R](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/fontes/codigo_autores/replication/04_marginal_main/01_sim_marginal.R) — 123 linhas; fonte integral preservada.
- [fontes/codigo_autores/replication/04_marginal_main/02_plot_marginal.R](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/fontes/codigo_autores/replication/04_marginal_main/02_plot_marginal.R) — 127 linhas; fonte integral preservada.
- [fontes/codigo_autores/replication/04_marginal_main/03_sim_marginal_fewer_SNPs.R](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/fontes/codigo_autores/replication/04_marginal_main/03_sim_marginal_fewer_SNPs.R) — 123 linhas; fonte integral preservada.
- [fontes/codigo_autores/replication/04_marginal_main/04_plot_marginal_fewer_SNPs.R](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/fontes/codigo_autores/replication/04_marginal_main/04_plot_marginal_fewer_SNPs.R) — 142 linhas; fonte integral preservada.
- [fontes/codigo_autores/replication/04_marginal_main/algorithms.R](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/fontes/codigo_autores/replication/04_marginal_main/algorithms.R) — 130 linhas; fonte integral preservada.
- [fontes/codigo_autores/replication/04_marginal_main/problems.R](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/fontes/codigo_autores/replication/04_marginal_main/problems.R) — 74 linhas; fonte integral preservada.
- [fontes/codigo_autores/replication/04_marginal_main/simulate_snps.R](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/fontes/codigo_autores/replication/04_marginal_main/simulate_snps.R) — 38 linhas; fonte integral preservada.
- [fontes/codigo_autores/replication/05_marginal_more_SNPs/01_sim_marginal_largep.R](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/fontes/codigo_autores/replication/05_marginal_more_SNPs/01_sim_marginal_largep.R) — 123 linhas; fonte integral preservada.
- [fontes/codigo_autores/replication/05_marginal_more_SNPs/02_plot_marginal_largep.R](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/fontes/codigo_autores/replication/05_marginal_more_SNPs/02_plot_marginal_largep.R) — 125 linhas; fonte integral preservada.
- [fontes/codigo_autores/replication/05_marginal_more_SNPs/algorithms.R](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/fontes/codigo_autores/replication/05_marginal_more_SNPs/algorithms.R) — 130 linhas; fonte integral preservada.
- [fontes/codigo_autores/replication/05_marginal_more_SNPs/problems.R](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/fontes/codigo_autores/replication/05_marginal_more_SNPs/problems.R) — 74 linhas; fonte integral preservada.
- [fontes/codigo_autores/replication/05_marginal_more_SNPs/simulate_snps.R](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/fontes/codigo_autores/replication/05_marginal_more_SNPs/simulate_snps.R) — 38 linhas; fonte integral preservada.
- [fontes/codigo_autores/replication/06_marginal_ld/01_sim_marginal_ld.R](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/fontes/codigo_autores/replication/06_marginal_ld/01_sim_marginal_ld.R) — 119 linhas; fonte integral preservada.
- [fontes/codigo_autores/replication/06_marginal_ld/02_plot_marginal_ld.R](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/fontes/codigo_autores/replication/06_marginal_ld/02_plot_marginal_ld.R) — 127 linhas; fonte integral preservada.
- [fontes/codigo_autores/replication/06_marginal_ld/algorithms.R](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/fontes/codigo_autores/replication/06_marginal_ld/algorithms.R) — 130 linhas; fonte integral preservada.
- [fontes/codigo_autores/replication/06_marginal_ld/helper_functions.R](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/fontes/codigo_autores/replication/06_marginal_ld/helper_functions.R) — 0 linhas; fonte integral preservada.
- [fontes/codigo_autores/replication/06_marginal_ld/problems.R](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/fontes/codigo_autores/replication/06_marginal_ld/problems.R) — 69 linhas; fonte integral preservada.
- [fontes/codigo_autores/replication/06_marginal_ld/simulate_ld_snps.R](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/fontes/codigo_autores/replication/06_marginal_ld/simulate_ld_snps.R) — 27 linhas; fonte integral preservada.

## Tabelas: nomes reais, dimensões e cabeçalhos

Os significados estão no dicionário de dados; os cabeçalhos abaixo são lidos dos próprios arquivos. Linhas são contadas sem o cabeçalho. Arquivos compactados podem ser grandes na visualização do GitHub; use download.


### etapa0_completo_etapa0_comp_rfsrc341_jvimp_etapa0_comp_rfsrc161_ordens.csv

[Arquivo](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/resultados/tabelas/etapa0_completo_etapa0_comp_rfsrc341_jvimp_etapa0_comp_rfsrc161_ordens.csv) — 103 linhas, 5 colunas.

`regra`, `cenario`, `dif_publicada`, `dif_nossa`, `invertida`


### etapa0_completo_etapa0_comp_rfsrc341_jvimp_etapa0_comp_rfsrc161_pontos.csv

[Arquivo](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/resultados/tabelas/etapa0_completo_etapa0_comp_rfsrc341_jvimp_etapa0_comp_rfsrc161_pontos.csv) — 5,760 linhas, 14 colunas.

`beta`, `beta_effect`, `maf_interaction`, `maf_effect`, `mtry`, `modelo`, `medida`, `nosso`, `n_rep`, `n_na`, `k`, `publicado`, `figura`, `dif`


### etapa0_completo_etapa0_comp_rfsrc341_jvimp_etapa0_comp_rfsrc161_proporcao_casos.csv

[Arquivo](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/resultados/tabelas/etapa0_completo_etapa0_comp_rfsrc341_jvimp_etapa0_comp_rfsrc161_proporcao_casos.csv) — 60 linhas, 9 colunas.

`desenho`, `model`, `beta`, `beta_effect`, `maf_interaction`, `maf_effect`, `prop_casos`, `esperada`, `dentro_0_02`


### etapa0_completo_etapa0_comp_rfsrc341_jvimp_etapa0_comp_rfsrc161_veredito.json

[Arquivo](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/resultados/tabelas/etapa0_completo_etapa0_comp_rfsrc341_jvimp_etapa0_comp_rfsrc161_veredito.json)

```json
{
 "etapa": "completo",
 "n_pontos": 5760,
 "pontos_sem_gabarito": 0,
 "frac_pontos_ate_0_10": 0.9652777777777778,
 "criterio1": true,
 "dif_abs_media": 0.023062361111111113,
 "ordens_avaliadas": 103,
 "ordens_invertidas": 0,
 "criterio2": true,
 "rank_na": 0,
 "proporcao_casos_ok": "60/60",
 "por_medida": {
  "Gini": 0.969,
  "JMST": 0.972,
  "JVIMP": 0.952,
  "PPI": 0.969,
  "Permutation": 0.965
 },
 "P0_passa": true
}
```


### etapa0_completo_etapa0_comp_rfsrc341_ordens.csv

[Arquivo](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/resultados/tabelas/etapa0_completo_etapa0_comp_rfsrc341_ordens.csv) — 103 linhas, 5 colunas.

`regra`, `cenario`, `dif_publicada`, `dif_nossa`, `invertida`


### etapa0_completo_etapa0_comp_rfsrc341_pontos.csv

[Arquivo](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/resultados/tabelas/etapa0_completo_etapa0_comp_rfsrc341_pontos.csv) — 5,760 linhas, 14 colunas.

`beta`, `beta_effect`, `maf_interaction`, `maf_effect`, `mtry`, `modelo`, `medida`, `nosso`, `n_rep`, `n_na`, `k`, `publicado`, `figura`, `dif`


### etapa0_completo_etapa0_comp_rfsrc341_proporcao_casos.csv

[Arquivo](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/resultados/tabelas/etapa0_completo_etapa0_comp_rfsrc341_proporcao_casos.csv) — 60 linhas, 9 colunas.

`desenho`, `model`, `beta`, `beta_effect`, `maf_interaction`, `maf_effect`, `prop_casos`, `esperada`, `dentro_0_02`


### etapa0_completo_etapa0_comp_rfsrc341_veredito.json

[Arquivo](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/resultados/tabelas/etapa0_completo_etapa0_comp_rfsrc341_veredito.json)

```json
{
 "etapa": "completo",
 "n_pontos": 5760,
 "pontos_sem_gabarito": 0,
 "frac_pontos_ate_0_10": 0.8821180555555556,
 "criterio1": false,
 "dif_abs_media": 0.04293166666666667,
 "ordens_avaliadas": 103,
 "ordens_invertidas": 2,
 "criterio2": false,
 "rank_na": 0,
 "proporcao_casos_ok": "60/60",
 "por_medida": {
  "Gini": 0.969,
  "JMST": 0.972,
  "JVIMP": 0.553,
  "PPI": 0.969,
  "Permutation": 0.965
 },
 "P0_passa": false
}
```


### etapa0_subconjunto_jvimp_etapa0_rfsrc161_ordens.csv

[Arquivo](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/resultados/tabelas/etapa0_subconjunto_jvimp_etapa0_rfsrc161_ordens.csv) — 26 linhas, 5 colunas.

`regra`, `cenario`, `dif_publicada`, `dif_nossa`, `invertida`


### etapa0_subconjunto_jvimp_etapa0_rfsrc161_pontos.csv

[Arquivo](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/resultados/tabelas/etapa0_subconjunto_jvimp_etapa0_rfsrc161_pontos.csv) — 960 linhas, 14 colunas.

`beta`, `beta_effect`, `maf_interaction`, `maf_effect`, `mtry`, `modelo`, `medida`, `nosso`, `n_rep`, `n_na`, `k`, `publicado`, `figura`, `dif`


### etapa0_subconjunto_jvimp_etapa0_rfsrc161_proporcao_casos.csv

[Arquivo](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/resultados/tabelas/etapa0_subconjunto_jvimp_etapa0_rfsrc161_proporcao_casos.csv) — 20 linhas, 9 colunas.

`desenho`, `model`, `beta`, `beta_effect`, `maf_interaction`, `maf_effect`, `prop_casos`, `esperada`, `dentro_0_02`


### etapa0_subconjunto_jvimp_etapa0_rfsrc161_veredito.json

[Arquivo](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/resultados/tabelas/etapa0_subconjunto_jvimp_etapa0_rfsrc161_veredito.json)

```json
{
 "etapa": "subconjunto",
 "n_pontos": 960,
 "pontos_sem_gabarito": 0,
 "frac_pontos_ate_0_10": 0.9708333333333333,
 "criterio1": true,
 "dif_abs_media": 0.02649166666666667,
 "ordens_avaliadas": 26,
 "ordens_invertidas": 0,
 "criterio2": true,
 "rank_na": 0,
 "proporcao_casos_ok": "20/20",
 "por_medida": {
  "Gini": 0.978,
  "JMST": 0.98,
  "JVIMP": 0.93,
  "PPI": 0.975,
  "Permutation": 0.994
 },
 "P0_passa": true
}
```


### etapa0_subconjunto_ordens.csv

[Arquivo](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/resultados/tabelas/etapa0_subconjunto_ordens.csv) — 26 linhas, 5 colunas.

`regra`, `cenario`, `dif_publicada`, `dif_nossa`, `invertida`


### etapa0_subconjunto_pontos.csv

[Arquivo](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/resultados/tabelas/etapa0_subconjunto_pontos.csv) — 960 linhas, 14 colunas.

`beta`, `beta_effect`, `maf_interaction`, `maf_effect`, `mtry`, `modelo`, `medida`, `nosso`, `n_rep`, `n_na`, `k`, `publicado`, `figura`, `dif`


### etapa0_subconjunto_proporcao_casos.csv

[Arquivo](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/resultados/tabelas/etapa0_subconjunto_proporcao_casos.csv) — 20 linhas, 9 colunas.

`desenho`, `model`, `beta`, `beta_effect`, `maf_interaction`, `maf_effect`, `prop_casos`, `esperada`, `dentro_0_02`


### etapa0_subconjunto_veredito.json

[Arquivo](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/resultados/tabelas/etapa0_subconjunto_veredito.json)

```json
{
 "etapa": "subconjunto",
 "n_pontos": 960,
 "pontos_sem_gabarito": 0,
 "frac_pontos_ate_0_10": 0.8947916666666667,
 "criterio1": false,
 "dif_abs_media": 0.044480625,
 "ordens_avaliadas": 26,
 "ordens_invertidas": 1,
 "criterio2": false,
 "rank_na": 0,
 "proporcao_casos_ok": "20/20",
 "por_medida": {
  "Gini": 0.978,
  "JMST": 0.98,
  "JVIMP": 0.565,
  "PPI": 0.975,
  "Permutation": 0.994
 },
 "P0_passa": false
}
```


### etapa1_concordancia_por_repeticao.csv.gz

[Arquivo](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/resultados/tabelas/etapa1_concordancia_por_repeticao.csv.gz) — 210,000 linhas, 6 colunas.

`desenho`, `repeticao`, `a`, `b`, `intersecao_top3`, `kendall_tau`


### etapa1_concordancia_resumo.csv

[Arquivo](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/resultados/tabelas/etapa1_concordancia_resumo.csv) — 105 linhas, 5 colunas.

`a`, `b`, `intersecao_top3`, `kendall_tau`, `n`


### etapa1_curvas_deteccao.csv

[Arquivo](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/resultados/tabelas/etapa1_curvas_deteccao.csv) — 14,800 linhas, 12 colunas.

`beta`, `beta_effect`, `maf_interaction`, `maf_effect`, `modelo`, `detector`, `ranking`, `direcao`, `deteccao`, `n`, `na`, `k`


### etapa1_desempenho_modelos.csv

[Arquivo](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/resultados/tabelas/etapa1_desempenho_modelos.csv) — 6 linhas, 3 colunas.

`modelo`, `logloss`, `acuracia`


### etapa1_postos_par_verdadeiro.csv.gz

[Arquivo](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/resultados/tabelas/etapa1_postos_par_verdadeiro.csv.gz) — 148,000 linhas, 12 colunas.

`beta`, `beta_effect`, `maf_interaction`, `maf_effect`, `model`, `desenho`, `repeticao`, `detector`, `ranking`, `direcao`, `posto_verdadeiro`, `modelo`


### etapa1_resumo_deteccao.csv

[Arquivo](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/resultados/tabelas/etapa1_resumo_deteccao.csv) — 1,480 linhas, 10 colunas.

`beta`, `beta_effect`, `maf_interaction`, `maf_effect`, `modelo`, `detector`, `ranking`, `direcao`, `media_curva_k1_10`, `acaso`


### etapa1_resumo_por_modelo.csv

[Arquivo](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/resultados/tabelas/etapa1_resumo_por_modelo.csv) — 74 linhas, 8 colunas.

`detector`, `ranking`, `direcao`, `Redundante`, `SNP modificador`, `Sem interação`, `Sinérgico`, `Só interação`


### piloto1_concordancia_por_repeticao.csv.gz

[Arquivo](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/resultados/tabelas/piloto1_concordancia_por_repeticao.csv.gz) — 525 linhas, 6 colunas.

`desenho`, `repeticao`, `a`, `b`, `intersecao_top3`, `kendall_tau`


### piloto1_concordancia_resumo.csv

[Arquivo](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/resultados/tabelas/piloto1_concordancia_resumo.csv) — 105 linhas, 5 colunas.

`a`, `b`, `intersecao_top3`, `kendall_tau`, `n`


### piloto1_curvas_deteccao.csv

[Arquivo](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/resultados/tabelas/piloto1_curvas_deteccao.csv) — 3,700 linhas, 12 colunas.

`beta`, `beta_effect`, `maf_interaction`, `maf_effect`, `modelo`, `detector`, `ranking`, `direcao`, `deteccao`, `n`, `na`, `k`


### piloto1_desempenho_modelos.csv

[Arquivo](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/resultados/tabelas/piloto1_desempenho_modelos.csv) — 6 linhas, 3 colunas.

`modelo`, `logloss`, `acuracia`


### piloto1_postos_par_verdadeiro.csv.gz

[Arquivo](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/resultados/tabelas/piloto1_postos_par_verdadeiro.csv.gz) — 370 linhas, 12 colunas.

`beta`, `beta_effect`, `maf_interaction`, `maf_effect`, `model`, `desenho`, `repeticao`, `detector`, `ranking`, `direcao`, `posto_verdadeiro`, `modelo`


### piloto1_resumo_deteccao.csv

[Arquivo](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/resultados/tabelas/piloto1_resumo_deteccao.csv) — 370 linhas, 10 colunas.

`beta`, `beta_effect`, `maf_interaction`, `maf_effect`, `modelo`, `detector`, `ranking`, `direcao`, `media_curva_k1_10`, `acaso`


### piloto1_resumo_por_modelo.csv

[Arquivo](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/resultados/tabelas/piloto1_resumo_por_modelo.csv) — 74 linhas, 8 colunas.

`detector`, `ranking`, `direcao`, `Redundante`, `SNP modificador`, `Sem interação`, `Sinérgico`, `Só interação`


## Inventário de arquivos e integridade

[Manifesto SHA-256](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/MANIFESTO_SHA256.csv) · [Inventário dos originais consultados](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/auditoria/inventario_originais.csv). O manifesto documental corresponde aos bytes publicados; o congelamento histórico corresponde ao momento que o originou. Não confundir os dois.

## Downloads e licença


- [etapa0_brutos.tar.gz](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/resultados/etapa0_brutos.tar.gz) — 0.15 MiB, outputs simulados por repetição.
- [etapa0_comp_rfsrc161_brutos.tar.gz](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/resultados/etapa0_comp_rfsrc161_brutos.tar.gz) — 0.34 MiB, outputs simulados por repetição.
- [etapa0_comp_rfsrc341_brutos.tar.gz](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/resultados/etapa0_comp_rfsrc341_brutos.tar.gz) — 0.86 MiB, outputs simulados por repetição.
- [etapa0_rfsrc161_brutos.tar.gz](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/resultados/etapa0_rfsrc161_brutos.tar.gz) — 0.07 MiB, outputs simulados por repetição.
- [etapa1_brutos.tar.gz](https://github.com/danifilho/Mestrado_ICMC/blob/edcbf4cc450583364e69cbe89a738596c7c2762f/documentacao/piloto7-wright2016/resultados/etapa1_brutos.tar.gz) — 15.69 MiB, outputs simulados por repetição.

Os suplementos e figuras de Wright são de Wright, Ziegler e König, 2016, sob CC BY 4.0 conforme o artigo. Os códigos dos autores mantêm os arquivos e avisos originais; a cópia documental não atribui autoria ao projeto. Credenciais, tokens e logs de autenticação não foram incluídos.


---
Snapshot das evidências: [`edcbf4cc4505`](https://github.com/danifilho/Mestrado_ICMC/commit/edcbf4cc450583364e69cbe89a738596c7c2762f). Documentação publicada em 19/11/2026.
