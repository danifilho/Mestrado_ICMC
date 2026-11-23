# Seleção arbórea e protocolo da nova comparação

**Versão documental 1.0.1.** [Artefatos fixados em commit](https://github.com/danifilho/Mestrado_ICMC/tree/fea0e2c9307da92aea9a43ee074b913394323f20/experimentos/selecao_arborea_v1).

Registro de 23 de novembro de 2026. Foi construída uma seleção operacional prospectiva, com critérios explícitos, mapa de candidatos, verificação de implementações e estimativa de custo. **Nenhuma nova comparação científica foi executada.** O estado de congelamento está em [CONGELAMENTO.json](https://github.com/danifilho/Mestrado_ICMC/blob/fea0e2c9307da92aea9a43ee074b913394323f20/experimentos/selecao_arborea_v1/CONGELAMENTO.json).

## Pergunta e unidade

**Modelos arbóreos voltados à exploração de interações priorizam os mesmos pares quando avaliados pela mesma perda por permutação conjunta? Como essa concordância se relaciona à proximidade preditiva e à estabilidade de cada método?**

A unidade é o procedimento de ajuste probabilístico, identificado por versão e configuração. O ranking principal mede dependência preditiva conjunta, incluindo efeitos individuais. Ele não identifica automaticamente interação pura. Extratores do mesmo modelo não serão contados como novos preditores.

## O que ficou definido

| Etapa solicitada | Entrega | Estado |
|---|---|---|
| Pergunta e unidade | [Critérios anteriores aos testes](https://github.com/danifilho/Mestrado_ICMC/blob/fea0e2c9307da92aea9a43ee074b913394323f20/experimentos/selecao_arborea_v1/CRITERIOS_ANTES_DOS_TESTES.md) | Definidas |
| Recorte e elegibilidade | Classificação binária, entrada numérica, árvores ou componentes ajustados por árvores e foco publicado em interação | Delimitados; não cobrem toda a literatura |
| Mapeamento e decisões | [Mapa](https://github.com/danifilho/Mestrado_ICMC/blob/fea0e2c9307da92aea9a43ee074b913394323f20/experimentos/selecao_arborea_v1/MAPA_CANDIDATOS.md), [matriz CSV](https://github.com/danifilho/Mestrado_ICMC/blob/fea0e2c9307da92aea9a43ee074b913394323f20/experimentos/selecao_arborea_v1/MATRIZ_DECISOES.csv), [fontes e busca](https://github.com/danifilho/Mestrado_ICMC/blob/fea0e2c9307da92aea9a43ee074b913394323f20/experimentos/selecao_arborea_v1/FONTES_E_BUSCAS.md) | 59 registros, incluindo variantes, controles e pendências; não são 59 algoritmos independentes |
| Implementações e configurações | [Auditoria e custo](https://github.com/danifilho/Mestrado_ICMC/blob/fea0e2c9307da92aea9a43ee074b913394323f20/experimentos/selecao_arborea_v1/AUDITORIA_E_CUSTO.md), código e resultados JSON | Sete métodos × dois tamanhos; oito verificações em cada caso, além de dez da régua e cinco dos controles |
| Congelamento prospectivo | [Seleção operacional](https://github.com/danifilho/Mestrado_ICMC/blob/fea0e2c9307da92aea9a43ee074b913394323f20/experimentos/selecao_arborea_v1/SELECAO_V1.md), [protocolo](https://github.com/danifilho/Mestrado_ICMC/blob/fea0e2c9307da92aea9a43ee074b913394323f20/experimentos/selecao_arborea_v1/PROTOCOLO_NOVA_AVALIACAO.md), manifesto SHA-256 | Congelamento documental; execução científica ainda não liberada |

## Seleção operacional

**RF, IF, iRF, Random Planted Forest, Unity Forests, Reinforcement Learning Trees e EBM.** RF é a referência histórica; os demais entram pelo vínculo publicado com a exploração ou representação de interações e pela implementação auditada. A diversidade de mecanismos descreve o conjunto selecionado; não substitui os critérios de inclusão.

siRF/RIT, H, SHAP e medidas de Wright ficam em um braço de extração separado. NID/MLP está fora do recorte arbóreo. RSRF exige confirmar suporte binário nativo. logicDT requer um braço de recodificação. GUIDE, RIF e SNPInterForest permanecem pertinentes, com lacunas operacionais explicitadas; não foram considerados cientificamente inferiores. A seleção é limitada pelo acesso e pela auditoria, e não sustenta uma afirmação sobre todos os métodos arbóreos.

## O que a auditoria mudou

- IF: o padrão para previsão sem EIM na versão auditada é 2000 árvores. O uso inicial de 20000 foi corrigido a partir do código; tentativas anteriores foram preservadas.
- iRF: instalação resolvida com compilador e caminhos de bibliotecas isolados, sem mudança no código do algoritmo. A previsão usa a última floresta; não é uma auditoria de todo o extrator RIT.
- RPF: a versão nova foi testada com classificação logística nativa. É uma configuração diferente da regressão L2 sobre resposta binária usada anteriormente. Ordem máxima dois é uma escolha explícita deste desenho, não o default de ordem três da versão nova.
- UFO: manteve-se a configuração dos autores durante a ampliação do limite de tempo. Um timeout de engenharia não foi usado como exclusão científica.

## Custo antes de executar

Com 20 cenários, 100 realizações, três sementes e 30 permutações, a extrapolação dos 7 perfis disponíveis é de **aproximadamente 9763 horas de um núcleo para ajuste e régua**. A régua requer 841 chamadas de previsão de 1000 linhas por ajuste. O custo do ajuste isolado subestima fortemente esse desenho.

Essa projeção usa uma máquina, dados de engenharia e execução em uma thread; não é um orçamento garantido nem uma comparação controlada de velocidade. Os fixtures R e Python têm o mesmo desenho, mas não as mesmas realizações. O custo deve ser perfilado na infraestrutura de destino e completado com controles, extração e análise. Conforme a decisão do pesquisador, a prioridade são os padrões dos autores; o teto será definido após a estimativa.

## Antes da nova avaliação

O congelamento preserva a composição operacional, configurações, critérios e planejamento. Ainda faltam definir o orçamento e integrar/verificar o gerador, a régua completa e a análise na execução futura. O manifesto mantém a liberação científica desativada. Alterações exigem nova versão anterior ao acesso aos resultados; o piloto anterior continua exploratório e não recebe pré-registro retrospectivo.

A comparação entre 21 pares dos sete atributos conhecidos será explicitamente condicional a esses candidatos. Ela não equivale a uma busca entre todos os 4950 pares dos 100 atributos. A análise de escalas continua como proposta posterior à qualificação.

## Evidências e reprodução

[Reprodução](https://github.com/danifilho/Mestrado_ICMC/blob/fea0e2c9307da92aea9a43ee074b913394323f20/experimentos/selecao_arborea_v1/REPRODUCAO.md), [decisões e tentativas](https://github.com/danifilho/Mestrado_ICMC/blob/fea0e2c9307da92aea9a43ee074b913394323f20/experimentos/selecao_arborea_v1/DECISOES.md), [código](https://github.com/danifilho/Mestrado_ICMC/tree/fea0e2c9307da92aea9a43ee074b913394323f20/experimentos/selecao_arborea_v1/codigo/), [resultados técnicos](https://github.com/danifilho/Mestrado_ICMC/tree/fea0e2c9307da92aea9a43ee074b913394323f20/experimentos/selecao_arborea_v1/resultados/), [configurações e sementes futuras](https://github.com/danifilho/Mestrado_ICMC/tree/fea0e2c9307da92aea9a43ee074b913394323f20/experimentos/selecao_arborea_v1/configs/). As sementes foram enumeradas, mas os novos dados científicos não foram gerados.

Os princípios de seleção e transparência se apoiam em [Boulesteix et al. (2013)](https://doi.org/10.1371/journal.pone.0061562) e [Weber et al. (2019)](https://doi.org/10.1186/s13059-019-1738-8). A medida de dependência preditiva se relaciona a [Fisher et al. (2019)](https://www.jmlr.org/papers/v20/18-760.html). As regras concretas do protocolo são decisões deste estudo; não foram prescritas literalmente por esses trabalhos.


## Histórico e fontes do registro

Página criada em 23/11/2026 a partir desta conversa, dos dois inventários locais anteriores, de arquivos do Piloto 7, das fontes primárias identificadas e dos testes técnicos desta auditoria. A orientação de priorizar os padrões dos autores e definir o teto após estimativa foi incorporada. Não houve alteração da monografia nem execução da nova avaliação científica.
