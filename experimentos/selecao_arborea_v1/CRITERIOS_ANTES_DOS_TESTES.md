# Seleção de modelos arbóreos para comparação por uma régua comum

Registro em 23 de novembro de 2026. Este registro antecede os testes técnicos desta auditoria, mas sucede os resultados conhecidos do Piloto 7. Não constitui pré-registro retrospectivo daquele piloto.

## Pergunta e unidade

Pergunta principal: **em classificação binária com atributos tabulares numéricos, em que medida modelos arbóreos voltados à exploração de interações priorizam os mesmos pares de atributos quando avaliados, após o ajuste, pela mesma perda por permutação conjunta? Como essa concordância se relaciona à proximidade do desempenho preditivo e à estabilidade dentro de cada método?**

A unidade de método é o procedimento de ajuste completo, identificado por implementação, versão e configuração. A unidade de repetição é uma realização independente dos dados; sementes de ajuste ficam aninhadas nessa realização. Extratores aplicados à mesma função preditiva não constituem novos modelos na régua comum. Execuções diferentes de iRF/siRF não serão presumidas idênticas: identidade exige comparar a função ajustada e as sementes.

A régua principal é ΔAB, aumento de log-loss ao permutar conjuntamente as duas colunas com a mesma permutação de linhas. Ela mede dependência preditiva conjunta, incluindo efeitos individuais. Não é um teste específico de interação. O contraste ΔAB−ΔA−ΔB e as saídas nativas serão secundários, explicitamente nomeados. Interpretar ΔAB como interação pura invalidaria a pergunta.

## Recorte científico

O universo principal é o de **preditores finais compostos por árvores ou somas de componentes ajustados por árvores**, com mecanismo publicado explicitamente relacionado à exploração, restrição ou recuperação de interações. Incluem-se artigos e preprints identificados como tais até 23/11/2026. A implementação dos autores pode estender o artigo a classificação; essa diferença deve ser declarada e a versão fixada. Não se exige aplicação biológica nem ranking nativo de pares.

O ensaio principal aceita diretamente a matriz numérica original (inclusive genótipos 0/1/2), desfecho binário e previsão de probabilidade para novas linhas. Não se converte uma regressão L2 em classificador por recorte de suas respostas. Recodificação binária externa, triagem externa de variáveis, novos resíduos e calibração adicionada pelo pesquisador definem extensões separadas. Transformações internas nativas e validação interna são permitidas e documentadas.

Modelos de regras com ajuste final linear, redes neurais e procedimentos que devolvem somente listas ficam fora deste recorte primário; continuam no mapa. Modelos arbóreos generalistas ficam no estrato de referências, com RF de Breiman como referência histórica. Essa delimitação não torna os participantes representativos de todos os algoritmos baseados em árvores.

## Busca e decisões

Reaproveitar os dois levantamentos locais como fontes de candidatos, não como comprovação. Complementar por fontes primárias e documentação oficial, registrando consultas, links, nível de leitura e decisões. Percorrer referências de Wright, iRF, IF e Unity Forests, e pesquisar árvores, interação e classificação. Este é um mapeamento dirigido com trilha auditável, não uma revisão sistemática exaustiva.

Para cada candidato registrar separadamente: elegibilidade científica, compatibilidade da tarefa, versão, saída, necessidade de adaptação e resultado técnico. Ausência de implementação auditada não prova inferioridade científica. Não escolher pelo desempenho conhecido do piloto nem pela recuperação do par verdadeiro. Candidatos sem evidência suficiente permanecem pendentes e impedem alegar cobertura integral do universo.

## Viabilidade técnica

Bibliotecas isoladas; preservar ambientes e estudos anteriores. Testes com dados artificiais de engenharia, sem calcular acurácia, log-loss de comparação, recuperação de verdade ou concordância entre métodos. Verificar ajuste, probabilidades finitas em [0,1], comprimento, classe positiva, repetição com mesma semente, ordem das linhas, serialização, aplicação da régua e ausência de alteração dos dados de entrada. Usar uma thread. Medir tempo apenas para planejamento.

Dois tamanhos previstos: 120 linhas e 8 atributos; 1000 linhas e 100 atributos. O teste menor verifica interfaces; o maior aproxima as dimensões do estudo, sem reproduzir seus geradores. Dois ajustes com a mesma semente por método. Limite inicial de 300 segundos por processo de teste; timeout significa pendência operacional, não exclusão científica. Configurações reduzidas verificam interface; a configuração definitiva precisa de ensaio próprio antes da liberação confirmatória.

Instalações e correções de interface são permitidas; alterações no mecanismo de aprendizagem ficam fora desta auditoria. Erros, novas tentativas e diferenças entre versões devem permanecer registrados. Não reduzir parâmetros apenas para um método depois de observar sua qualidade preditiva.

## Congelamento

Congelar por SHA-256 os critérios, o mapa, os adaptadores testados, as versões, os resultados técnicos e o protocolo. Uma configuração só recebe o estado executável após passar no teste correspondente. Se houver candidatos ou configurações obrigatórias pendentes, congelar a versão documental como **bloqueada para avaliação confirmatória**, com lista explícita das pendências. Não simular conclusão dos cinco passos apenas produzindo um hash.

Qualquer alteração posterior exige nova versão e justificativa anterior ao acesso aos novos resultados. A nova avaliação terá sementes e dados diferentes dos estudos já vistos. A análise da escala permanece para depois da qualificação, conforme orientação do pesquisador.

## Fundamentação

- Wright, Ziegler e König (2016), https://doi.org/10.1186/s12859-016-0995-8 — problema motivador e desenho de simulação, não critério suficiente de seleção.
- Fisher, Rudin e Dominici (2019), https://www.jmlr.org/papers/v20/18-760.html — dependência de modelos em relação às variáveis; a comparação finita proposta não estima toda a MCR.
- Boulesteix, Lauer e Eugster (2013), https://doi.org/10.1371/journal.pone.0061562 — comparação metodológica neutra.
- Weber et al. (2019), https://doi.org/10.1186/s13059-019-1738-8 — transparência na seleção e tratamento de configurações.

Os critérios concretos acima são decisões deste estudo, fundamentadas nesses princípios; não foram prescritos literalmente pelos artigos.
