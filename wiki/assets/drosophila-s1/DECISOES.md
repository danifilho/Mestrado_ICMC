# Decisões — detectores_regulacao_drosophila_v1

As decisões D1 a D16 foram tomadas antes de qualquer ranking deste estudo. As posteriores, se houver, ficam marcadas como tal.

| ID | Decisão | Motivo |
|---|---|---|
| D1 | Usar os dados do Zenodo (`enhancer.Rdata`, idêntico a `irfSuppData1.csv` e aos arquivos da comparação anterior) sem transformação | Auditoria: X, Y, partições oficiais e nomes de colunas são idênticos (`resultados/auditoria/auditoria_dados.json`) |
| D2 | Manter os 80 preditores no ajuste e avaliar biologicamente só os 253 pares de fatores; histonas e input à parte | Especificação. O iRF original usou todos os 80 |
| D3 | Partição agrupada 60/20/20 (grupos de sobreposição, mesmo id ou atributos idênticos); partição oficial só como reprodução secundária | 1.165 grupos ficam divididos na partição oficial |
| D4 | Validação usada só para a importância por permutação do RF | Não há ajuste de hiperparâmetros; os métodos usam padrões dos autores |
| D5 | iRF 2.0.0 com a configuração exata de `enhancer.R` (RIT com 500 árvores, `varnames.grp`) | Reprodução da aplicação original. Observação: `enhancer.R` passa `rit.params` e `rit.param`, e só o segundo é argumento do iRF |
| D6 | IF com padrões do pacote (n > 1000: EIM em floresta de profundidade restrita e previsão em floresta separada) | Comportamento documentado pelos autores. A EIM e as previsões vêm de florestas diferentes, o que fica registrado |
| D7 | Pares de fatores: máximo do escore entre réplicas (IF), máximo entre os grupos prdBQ e prdFQ (iRF) | Regra simples e fixa; réplicas do mesmo fator não formam par |
| D8 | iRF: lista principal só com pares retornados; projeção de conjuntos maiores apenas como análise secundária | Especificação; não fabricar pares |
| D9 | Empates desfeitos por sorteio com semente fixa, com sensibilidade de 1.000 resoluções; nunca ordem alfabética | A ordem alfabética criaria estabilidade e concordância artificiais |
| D10 | Referência biológica por busca uniforme (BioGRID + PubMed), revisão manual de até 3 frases por par, categorias A–E (+X, Cneg, N, P) | Esforço comparável para todos os pares. Limites registrados no PROTOCOLO, §4 |
| D11 | Suporte principal = A; regulação cruzada (X) à parte | A pergunta é sobre combinação de fatores em enhancers. A regulação cruzada é uma relação entre fatores, mas não é regulação conjunta |
| D12 | Afirmações do artigo do iRF (P) e de revisões não contam como A | Especificação: rastrear evidência primária |
| D13 | FlyBase não usado | O servidor exige desafio interativo (WAF). Foram usados o `gene_info` do NCBI (IDs FBgn incluídos) e o BioGRID |
| D14 | Permutação por troca de vetores de rótulos entre grupos de mesmo tamanho | Preserva a dependência dentro dos grupos sobrepostos. Grupos de tamanho único não mudam |
| D15 | R = 20 reamostragens de 80% dos grupos, 10 permutações e 3 sementes | Custo estimado no piloto: cerca de 20 CPU-h, dentro do teto de 40 |
| D16 | RPF e RSRF não incluídos | Desfecho binário sem suporte no RSRF 0.1.6; extração do RPF não definida para este caso |

## Depois do congelamento (registradas, sem mudar regras de análise)

| ID | O que mudou | Por quê |
|---|---|---|
| D17 | `grau_preservado` interrompe a cadeia quando nenhuma troca é possível na primeira amostra e devolve a própria lista (sequência de graus degenerada) | A primeira execução ficou presa em listas em forma de estrela (iRF, importância). É uma correção de código. O resultado (controle não informativo) é relatado |
| D18 | Estudos de caso: quando o mesmo par satisfaz os critérios 2 e 3, fica uma linha com os dois rótulos | O par Kni–Twi atendeu aos dois critérios. A regra não foi alterada para buscar um terceiro par |
| D19 | Figura 5: níveis "mínimo + tercis acima do mínimo" em vez de quartis | 37–98% das regiões têm o valor mínimo de ligação, e os quartis colapsavam. É uma mudança só de visualização descritiva |
