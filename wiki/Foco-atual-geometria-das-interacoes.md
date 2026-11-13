# Foco atual — geometria dos padrões de interação sob transformações

**Decisão: 12 de novembro de 2026 (America/Sao_Paulo).**
**Status: direção de pesquisa acordada; hipóteses em investigação.**

## Fonte e alcance deste registro

Fonte primária desta decisão: conversa atual com Daniel, que pediu explicitamente para adotar e documentar esta ideia como foco atual. Trechos orientadores: “representação gráfica não bidimensional dos padrões de interação e transformação desses padrões” e “Mentalize essa ideia como foco atual do projeto e documente isso no github”.

Foram consultados o README, o índice, o registro de discussões e a política deste repositório. O chat separado “Documentar testes dos pilotos 3 e 4” não foi integralmente recuperado; sua documentação publicada foi consultada. Este registro não representa execução de novos testes ou revisão nova da literatura.

## Pergunta que permanece

**Quando um método diz que encontrou uma interação, o que ele encontrou — e o que isso permite concluir sobre a biologia?**

O recorte atual pergunta:

> Existe uma organização dos padrões de interação, revelada por suas respostas a transformações, que permita reconhecer e prever aspectos da organização do sistema que os produziu?

## Ideia central

Estudar o padrão completo de interações como um objeto multidimensional e investigar como ele se reorganiza sob transformações declaradas. A representação deve ir além de uma lista de pares detectados: considerar magnitudes, sinais, ordens, contextos e comportamentos compartilhados.

Dois sistemas podem apresentar os mesmos pares detectados, mas diferentes comportamentos desses pares quando a escala da resposta muda. Em um, muitas interações podem ser compatíveis com uma única curva global; em outro, grupos diferentes podem responder a curvas diferentes; em outro, as dependências podem permanecer sobrepostas e sem hierarquia simples. Essas possibilidades são hipóteses e exemplos conceituais, não resultados biológicos estabelecidos.

A assinatura pretendida é uma representação comparável da organização dos efeitos. Não se pressupõe que seja única para cada dataset ou que identifique um mecanismo. Mecanismos distintos podem produzir a mesma distribuição observada e, consequentemente, a mesma assinatura.

## Dois níveis de representação

1. **Dentro de um conjunto de dados:** representar cada interação pelo seu comportamento sob transformações e contextos. Avaliar proximidades, grupos, sobreposições e outras estruturas.
2. **Entre conjuntos de dados:** comparar essas organizações completas para investigar semelhança, discriminação e transferência preditiva.

Não está decidido se a representação final será um vetor, matriz, grafo, árvore, espaço geométrico ou combinação. Distâncias, normalizações e correspondências entre variáveis ainda precisam ser definidas.

Três dimensões podem servir à visualização; não limitam a dimensionalidade científica do objeto. Projeções 2D/3D podem esconder informação ou produzir proximidades aparentes. Conclusões devem ser testadas no espaço completo.

## Por que transformações?

Elas permitem perguntar se dependências conjuntas são compatíveis com uma curva comum aplicada a contribuições mais simples. Por exemplo, y = exp(A+B) não é aditivo na escala original, mas log(y) = A+B. Encontrar essa representação não torna falsa a interação original e não prova que o organismo executa uma exponencial.

Transformações estritamente monótonas preservam a ordenação e são invertíveis em seu domínio. Isso oferece uma restrição interpretável; ajustes isotônicos com patamares não têm automaticamente essa propriedade.

Devem ser distinguidas:

- **Transformação da resposta:** mudar sua escala e recalcular as interações.
- **Transformação da representação:** normalizar, alinhar ou projetar os descritores geométricos.
- **Composição local:** permitir curvas em contribuições intermediárias; não equivale a aplicar várias curvas à resposta inteira.

O banco de curvas, domínio, regularidade, complexidade e critérios de escolha precisam ser justificados. Resistência às curvas testadas não define “interação biológica verdadeira”. Falha em removê-la pode refletir restrições do banco, ruído ou falha de ajuste.

## Papel da árvore

A árvore é uma hipótese de resumo da geometria por explicações compartilhadas, e não o objetivo obrigatório. Quando houver hierarquia sustentada, nós poderão representar conjuntos de interações compatíveis com uma explicação comum. Sobreposição ou equivalência podem exigir grafos, múltiplas árvores ou ausência de uma árvore identificável.

Não confundir:

- árvore de decisão, que particiona observações;
- árvore de expressão, que compõe operações sobre variáveis;
- árvore de interações, que organiza componentes por explicações ou comportamentos compartilhados;
- hierarquia de rótulos, como GO/FunCat.

A ideia não deve ser reduzida a agrupar observações nem a reconstruir a ontologia biológica. HMC pode voltar posteriormente, sem impor essa estrutura ao núcleo atual.

## O que os pilotos já informam

Fontes: [Piloto 3](Piloto-3.md), [Piloto 4](Piloto-4.md) e [catálogo de evidências](Catalogo-de-testes.md). Esta seção retoma as conclusões documentadas, sem reexecutar os testes.

- **Piloto 3:** os perfis de transformação contêm informação útil para distinguir famílias de funções simuladas; a assinatura da árvore não superou o perfil sem árvore. Classificar famílias não equivale a prever respostas de combinações inéditas nem a identificar mecanismos biológicos.
- **Piloto 4:** composições adequadas ajudaram na previsão dentro do catálogo estudado. Entretanto, a árvore de expressão testada não é a árvore de interações originalmente imaginada. A árvore de componentes permaneceu instável.
- **Consequência para o foco:** investigar primeiro o valor do comportamento multidimensional sob transformações; avaliar empiricamente se uma árvore preserva, comprime ou prejudica essa informação.

Os resultados não demonstram assinatura única, necessidade de hierarquia, novidade científica ou inferência biológica validada.

## O que tornaria a contribuição importante

A ambição é descobrir uma representação que permita recuperar ou prever algo que listas de interações não capturam. AlphaFold é uma referência de ambição e mudança de representação, não uma metodologia a copiar nem uma comparação de desempenho ou impacto já alcançado.

A contribuição precisaria demonstrar pelo menos um ganho delimitado:

- discriminar organizações geradoras apesar de listas de interações semelhantes;
- prever combinações retidas ou transferir entre condições;
- resumir muitos efeitos por poucas explicações sem perder informação relevante;
- estabelecer equivalências e limites que impeçam inferências indevidas.

Uma figura atraente, muitas dimensões ou o reconhecimento de famílias sintéticas favoráveis não bastam. Novidade em relação à geometria de paisagens, epistasia global e modelos composicionais continua pendente de auditoria bibliográfica.

## Avaliações propostas — ainda não executadas como novo estudo

1. Fixar entradas, resposta, distribuição de referência e definição de interação.
2. Definir descritores que preservem informação relevante; energias de fANOVA isoladas perdem sinal e forma.
3. Comparar: lista de pares, componentes na escala original, perfis sem agrupamento, representação geométrica e resumo hierárquico.
4. Separar reconhecimento de família, recuperação de estrutura, previsão e inferência mecanística.
5. Testar ruído, amostragem incompleta, transformações fora do banco, sobreposição e mecanismos observacionalmente equivalentes.
6. Avaliar estabilidade, complexidade e otimização justa; evitar que agrupamentos sejam criados apenas por desempates em componentes quase nulos.
7. Usar projeções somente como visualização, sem confundir separação visual com evidência.
8. Definir uma propriedade biológica e um desenho adequado quando chegar à validação biológica. Não fixar cooperatividade por conveniência nem tratar GO como gabarito mecanístico.

## Decisões de continuidade

- Este é o foco conceitual atual; registros anteriores permanecem como histórico.
- A pergunta original sobre significado e inferência é preservada.
- A árvore deixa de ser uma exigência da representação, mas continua como candidata.
- Não prometer algoritmo superior ao iRF antes de comparar alvos e tarefas compatíveis.
- Não tratar todos os padrões compartilhados como prova de uma causa compartilhada.
- Não iniciar mais um piloto sem explicitar qual hipótese nova ele distingue.
- Manter fatos, resultados, interpretações e propostas separados.

## Histórico

- 2026-11-12: foco registrado a pedido explícito do pesquisador; geometria dos padrões e respostas a transformações passa a ser o objeto central, com hierarquia como hipótese de representação.
