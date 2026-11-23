# Auditoria executada e estimativa de custo

Data: 23/11/2026. Testes de engenharia com resposta balanceada independente dos atributos. Não foi comparado desempenho nem recuperação de interações. O resultado PASS indica que passaram oito verificações específicas, não validação integral do algoritmo.

| Método | Dimensão | Estado | Primeiro ajuste (s) | Verificações aprovadas |
|---|---|---|---:|---:|
|RF|120×8|PASS|0.696|8|
|RF|1000×100|PASS|0.53|8|
|IF|120×8|PASS|2.191|8|
|IF|1000×100|PASS|28.997|8|
|iRF|120×8|PASS|0.792|8|
|iRF|1000×100|PASS|11.263|8|
|RPF|120×8|PASS|0.573|8|
|RPF|1000×100|PASS|172.488|8|
|UFO|120×8|PASS|46.119|8|
|UFO|1000×100|PASS|305.546|8|
|RLT|120×8|PASS|0.899|8|
|RLT|1000×100|PASS|49.618|8|
|EBM|120×8|PASS|1.6178897919999145|8|
|EBM|1000×100|PASS|21.681914666998637|8|

As oito verificações são: probabilidades finitas e limitadas, repetição com mesma semente, serialização, equivariância à ordem das linhas, preservação da entrada e previsão após permutar A, B e AB. As dez verificações adicionais da régua estão em `resultados/testes_regua.json`. Não se verificou aqui convergência de toda a distribuição de escores, desempenho em todas as distribuições nem igualdade entre máquinas.

## Custo condicional do desenho proposto

O pesquisador escolheu priorizar os padrões dos autores e definir o teto após a estimativa. A conta abaixo usa 20 cenários × 100 realizações × 3 sementes = 6000 ajustes por método. A régua possui 1 + 30×(7+21) = 841 chamadas de previsão de 1000 linhas por ajuste. As sete chamadas de conjuntos individuais permitem calcular o contraste secundário; a medida principal de pares sozinha usaria 631 chamadas.

| Método | Ajuste (s) | Previsão de 1000 linhas (s) | Só ajustes (h de um núcleo) | Ajustes e régua (h de um núcleo) |
|---|---:|---:|---:|---:|
|RF|0.565|0.06780|0.9|96.0|
|IF|28.146|0.62080|46.9|917.1|
|iRF|11.698|0.03370|19.5|66.7|
|RPF|171.979|0.00210|286.6|289.6|
|UFO|313.194|5.51730|522.0|8255.4|
|RLT|49.049|0.01190|81.7|98.4|
|EBM|22.069|0.00192|36.8|39.5|

Total dos 7 métodos com perfil disponível: **9762.7 horas de um núcleo**, por extrapolação.

Essa é uma projeção de tempo de parede em uma thread, não uma medição de CPU-h da execução científica. Parte dos perfis ocorreu com outros testes ativos. A distribuição usada tem resposta independente e pode produzir árvores e componentes diferentes dos cenários de Wright; especialmente a poda do RPF pode modificar muito o custo. A medida não inclui controles, extração nativa, bootstrap, transferência e armazenamento, verificações ou tentativas com falha. Também não é estimativa de incerteza: uma linha de perfil por método é insuficiente para um intervalo de custo.

O perfil faz um ajuste e dez previsões após aquecimento, sem calcular perdas comparativas. Todos os tempos individuais e a configuração estão nos JSON `*_cost.json`. Usar outra máquina, paralelismo ou previsão em lotes exige novo perfil; não prometer aceleração linear. A escolha de um teto menor pode exigir reduzir o desenho ou otimizar a implementação da régua, mas não justifica alterar silenciosamente os algoritmos.

Nenhuma nova avaliação científica foi iniciada. As sementes futuras foram apenas enumeradas.
