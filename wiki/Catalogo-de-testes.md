# Catálogo de testes e evidências

Os identificadores abaixo são editoriais, adicionados nesta consolidação. Os resultados são os dos artefatos originais.

## Piloto 3

700 funções independentes, cinco famílias, quatro variáveis em cinco níveis (625 células). Treino: 300 funções; teste semelhante: 200; teste com maior saturação: 200. Cada função observada exata e com 1.000 ensaios binomiais por célula: 1.400 tabelas pareadas. Semente: 20261112.

| ID | Teste | Evidência em `piloto3/` | Resultado / limite |
|---|---|---|---|
| P3-01 | Verificações matemáticas: reconstrução fANOVA, aditividade, par puro, inversão logística, custo de fusões, invariância à renomeação | `experimento.py`, `execucao.log` | Verificações internas relatadas; não reexecutadas nesta consolidação |
| P3-02 | Classificar famílias com sete representações, em dados exatos e ruidosos | `resultados/desempenho.csv`, `previsoes.csv` | Perfil: 100% no teste semelhante; árvore: 98% exato e 99% ruidoso |
| P3-03 | Generalização para maior saturação | mesmos CSVs | Perfil: 97,5% em ambos os regimes; árvore: 93,5% exato e 90,5% ruidoso |
| P3-04 | Diferenças pareadas por bootstrap, 1.000 reamostragens | `resultados/diferencas_pareadas.csv` | No teste ruidoso com maior saturação: árvore − perfil = −7 pontos percentuais; IC 95% −11,5 a −2,5 |
| P3-05 | Rótulos de treino permutados, 20 repetições | `resultados/controle_rotulos_permutados.csv` | Média 20,35%, próxima do acaso de 20% |
| P3-06 | PCA da assinatura da árvore, ajustada no treino | `resultados/pca.json`, `assinatura_3d.png` | Três eixos retêm aproximadamente 41,1%; visualização, não prova mecanística |
| P3-07 | Inspeção de árvores e confusão de famílias | `resultados/arvores_exemplos.json`, `arvores.png`, `confusao.png` | Inspeção descritiva; não valida recuperação de módulos |

## Piloto 4

48 funções independentes (seis famílias × oito geradores). 625 células por função; 125 reservadas para validação, 125 para teste; treino com 100 ou 250. Ruído gaussiano relativo: 0%, 5%, 15%; três réplicas nas condições ruidosas. Semente: 20261113, um parâmetro do protocolo, não uma data de execução.

| ID | Teste | Evidência em `piloto4/resultados/` | Resultado / limite |
|---|---|---|---|
| P4-01 | Gradientes analíticos contra numéricos e execução curta | código `piloto4.py`, log na pasta superior | Verificação de implementação; rodada curta não é evidência principal |
| P4-02 | Recuperação entre 17 estruturas candidatas | `previsao_resumo.csv`, `resumo_por_condicao.csv` | Com 250 células e 15% de ruído: separados 100%; aninhados 95,8% (23/24) |
| P4-03 | Previsão em células retidas: árvore, sem aninhamento, índices livres, ExtraTrees | `previsao_resumo.csv`, `ajustes.csv` | Aninhados: NMSE 0,000984 contra 0,022059 sem aninhamento, aproximadamente 22× menor |
| P4-04 | Estrutura correta versus incorreta com igual número de parâmetros | `previsao_resumo.csv`, `diferencas_bootstrap_geradores.csv` | Aninhados, nove parâmetros: 0,000876 contra 0,010956 |
| P4-05 | Grupos sobrepostos | `previsao_resumo.csv` | Árvore exclusiva 0,054664 contra 0,011014 dos índices livres no ajuste principal |
| P4-06 | Curva geradora fora do banco: arctan | `geradores.json`, `previsao_resumo.csv` | Aproximação por tanh funcionou nesse cenário; não demonstra recuperação da curva verdadeira |
| P4-07 | Repetibilidade das estruturas de expressão sob ruído | `estabilidade_expressoes.csv` | Com 250 células e 15% de ruído: acordo 100% separados, 91,7% aninhados |
| P4-08 | Estabilidade da árvore de componentes em 432 tabelas | `estabilidade_assinaturas.csv`, `estabilidade_assinaturas_pares.csv` | Distância à exata alta: 0,552–0,764 com 1.000 ensaios, conforme família |
| P4-09 | Nó dos componentes internos ao grupo verdadeiro de três variáveis | `estabilidade_assinaturas.csv` | Presença em 25% dos exemplos exatos e 18,75% com 1.000 ensaios |
| P4-10 | Ambiguidade de 15 árvores de somas sob logística global | `controle_ambiguidade.json` | Respostas equivalentes até erro numérico inferior a 1e-14 |
| P4-11 | Auditoria de convergência | `convergencia.csv`, `convergencia_selecionados.csv` | 81,5% dos candidatos e 100% das árvores selecionadas convergiram; não certifica ótimo global |
| P4-12 | Sensibilidade posterior: dez inícios, 500 avaliações, 96 ajustes | `sensibilidade_otimizacao.csv`, `protocolo_sensibilidade.json` | Aninhados: árvore 0,001107 versus livre 0,004052; comparação restrita à réplica zero |
| P4-13 | Bootstrap de diferenças entre modelos por gerador | `diferencas_bootstrap_geradores.csv` | Reamostra oito geradores por família; intervalos exploratórios, sem correção de multiplicidade |

NMSE = MSE nas células de teste / variância da função verdadeira. Não é acurácia. As 672 condições e 12.768 ajustes não equivalem a funções independentes adicionais.

## Pendências científicas

Repetir com novas sementes; avaliar componentes quase nulos e empates; permitir interromper fusões; comparar topologia completa com perfis e grupos planos; ampliar competidores e otimização; estudar células faltantes e maior dimensão; validar em dados biológicos. Essas propostas não devem ser registradas como testes já realizados.

## Fontes e data

Consolidação em 12/11/2026. Cada linha remete aos arquivos dos [pilotos 3 e 4 no commit original](https://github.com/danifilho/Mestrado_ICMC/tree/dbd89c6f516b0aa63e0109357346f4edc0ed4b46). As interpretações foram extraídas dos relatórios preservados, com conferência de contagens e integridade descrita em [Reprodução](Reproducao-e-rastreabilidade.md).
