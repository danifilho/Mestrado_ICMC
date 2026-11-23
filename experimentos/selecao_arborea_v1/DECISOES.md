# Decisões de seleção e auditoria

Todas as entradas abaixo são de 23/11/2026. Nenhuma usa desempenho ou recuperação de pares para escolher métodos.

1. **Unidade:** comparar procedimentos de ajuste probabilístico, com extratores separados. Motivação: a régua aplicada à mesma função não produz um competidor novo.
2. **Recorte:** árvores e componentes ajustados por árvores, classificação binária, entrada numérica sem adaptação externa e foco publicado em interação. RF é a referência histórica. Isso restringe o alcance; não representa todo o campo.
3. **Inventário:** preservar os 56 registros anteriores e acrescentar LSSFind, Extra Trees e lo-siRF como candidatos/leituras, sem declarar revisão integral das 59 entradas.
4. **Pacotes:** aceitar versões arquivadas e preprints identificados. Registrar separadamente artigo, versão, documentação e execução.
5. **iRF:** espelho CRAN 2.0.0 encontrado, mas a execução usa o código dos autores 3.0.0 no commit já documentado. A compilação exigiu Fortran isolado, indicação do assembler do sistema e caminho de bibliotecas no binário. Não houve modificação do código-fonte do algoritmo. Logs das quatro tentativas preservados. O ambiente de compilação é parte da reprodução.
6. **RPF:** testar classificação logística nativa da versão 0.5.0.9000, sem reproduzir a adaptação L2 do piloto. A API mudou e a versão deve constar de toda conclusão.
7. **IF:** auditoria principal da previsão com EIM desligada, preservando 20000 árvores. Isso não audita o extrator EIM. Não reutilizar o resultado como evidência de estabilidade do ranking nativo.
8. **Limite inicial:** IF e RPF passaram no teste pequeno, mas o processo de 1000×100 excedeu 300 segundos. Isso é timeout do conjunto de verificações (dois ajustes e previsões), não necessariamente do primeiro ajuste. Não medir qualidade científica por esse limite.
9. **Diagnóstico adicional de custo:** permitir uma nova tentativa de até 1200 segundos para IF e RPF na mesma configuração, preservando o timeout inicial e o tempo do primeiro ajuste. Essa ampliação é feita antes de qualquer resultado científico, sem reduzir árvores, selecionar pares ou ajustar desempenho. Não altera os critérios científicos. Uma falha persistente mantém pendência operacional.
10. **Congelamento:** distinguir versão documental da liberação executável. Se a auditoria revelar pendências, preservá-las no manifesto em vez de escolher silenciosamente apenas os métodos fáceis de executar.

11. **Correção do padrão de IF:** a inspeção do corpo de `interactionfor` mostrou 2000 árvores quando `importance="none"`, e 20000 quando se calcula EIM. A primeira configuração de 20000 foi excessiva para a política de padrões preditivos. Interrompida a repetição longa e preservadas as tentativas. Nova auditoria preditiva com 2000 árvores; correção baseada no código, não em desempenho. A tentativa ampliada de RPF prevista em D9 ainda não ocorreu.

12. **Resultado da ampliação de RPF:** a tentativa de 1000×100 passou, com 172,488 s no primeiro ajuste e 341,8 s no conjunto de verificações. D11 registrava o estado anterior à execução; esta entrada o atualiza sem apagar o histórico.
13. **Orientação do pesquisador:** priorizar os padrões dos autores e definir o teto após estimativa. Não excluir métodos por ultrapassarem o limite diagnóstico de 300 s nem reduzir hiperparâmetros para caber no orçamento do piloto anterior.
14. **UFO:** ampliar a tentativa de 1000×100 para 1800 s, preservando a configuração e o timeout inicial. O limite vale para verificações de engenharia, não para a avaliação científica futura.

15. **Custos da régua:** medido separadamente o tempo de previsão de 1000 linhas, em dez chamadas após aquecimento, sem métricas científicas. A projeção usa 841 chamadas por ajuste; não confundir custo de ajuste com custo total.
16. **Coorte operacional v1:** documentada em `SELECAO_V1.md`. Os candidatos sem implementação auditada permanecem como lacunas, sem reivindicar cobertura de todo o universo arbóreo. A documentação pode ser congelada; a liberação da avaliação exige orçamento e verificações de integração adicionais.
17. **UFO aprovado:** a repetição ampliada de 1000×100 passou, com 305,546 s no primeiro ajuste e 633,085 s no conjunto de verificações. O perfil separado também foi concluído.
18. **Configurações versus mecanismo:** a seção 4.3 do preprint de UFO usa 20000 árvores também no RF comparador, com subamostragem de 0,7 e nó mínimo cinco. A comparação operacional aqui usa os padrões próprios registrados de cada procedimento, não reproduz aquele controle pareado. Portanto, diferenças não podem ser atribuídas isoladamente ao mecanismo de construção das raízes. Uma ablação com parâmetros harmonizados seria outro ensaio, fixado antes de executar.
