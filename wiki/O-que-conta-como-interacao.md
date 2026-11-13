# O que conta como interação?

**Data:** 13 de novembro de 2026 (America/Sao_Paulo).

**Status:** revisão bibliográfica dirigida e proposta metodológica para discussão; não constitui protocolo congelado, revisão sistemática ou resultado experimental novo. Fonte da pergunta: conversa com o pesquisador sobre definição de interação, adaptação dos trabalhos relacionados e visualização. Não foram publicados resultados locais dos pilotos nesta atualização.

## Definição e exemplo

Uma interação exige declarar uma referência de ausência de interação. Para a abordagem funcional do projeto, propõe-se definir uma interação de um conjunto de variáveis como a parte da resposta que não pode ser representada pela combinação aditiva dos efeitos de seus subconjuntos próprios, sob uma escala, distribuição de referência e regras de decomposição especificadas. Essa formulação segue a purificação por ANOVA funcional de Lengerich et al. (2020), não uma definição universal de mecanismo biológico. O trabalho mostra que previsões idênticas podem admitir atribuições diferentes aos termos antes de impor as restrições da decomposição. [Fonte](https://proceedings.mlr.press/v108/lengerich20a.html).

Exemplo didático inventado, sem dados experimentais:

| Condição | Resposta |
|---|---:|
| Nenhuma alteração | 10 |
| Apenas A | 12 |
| Apenas B | 13 |
| A e B | 19 |

A acrescenta 2 sem B, mas acrescenta 6 com B. Sob o referencial aditivo, esperaríamos 15 para A e B; a diferença de diferenças é 19 − 12 − 13 + 10 = 4. Esse contraste representa interação nessa escala. Com variáveis adicionais, é necessário especificar se o contraste é condicionado a um contexto ou calculado sobre uma distribuição de contextos.

Para três variáveis, um efeito conjunto não é automaticamente uma interação de terceira ordem: é necessário retirar também os efeitos dos pares. Duas variáveis correlacionadas não bastam para estabelecer interação na resposta, e uma curva não linear de uma variável isolada tampouco basta: A² + B continua aditivo entre A e B.

Para cada análise, registrar: resposta ou função modelada; variáveis e domínio; escala; referência sem interação; distribuição usada para ponderar os contextos; tratamento da dependência entre variáveis; restrições da decomposição; incerteza e regra de detecção. Hooker (2007) fundamenta a atenção à dependência: procedimentos inadequados podem enfatizar regiões pouco sustentadas pelos dados. A fórmula usual para entradas independentes não deve ser transferida automaticamente para variáveis correlacionadas. [Fonte](https://doi.org/10.1198/106186007X237892).

## O que o detector pode afirmar

Distinguir três níveis:

1. **Componente funcional:** termo definido matematicamente na função e referência escolhidas.
2. **Detecção com dados:** estimativa desse componente, sujeita a erro de medição, amostragem e ajuste. Um valor estimado diferente de zero não basta; a regra estatística e a relevância do efeito precisam ser definidas.
3. **Interpretação biológica:** hipótese sobre processos que originam o padrão. A geometria pode apoiar essa hipótese, mas não equivale por si a demonstrar contato físico, causalidade ou pertencimento a uma via.

Essa distinção é uma síntese proposta para orientar o projeto.

## Por que a escala e as transformações importam

Otwinowski, McCandlish e Plotkin (2018) ajustam modelos em que contribuições mutacionais aditivas numa característica latente passam por uma curva monótona não linear até o fenótipo observado. Assim, diversos efeitos epistáticos podem compartilhar uma explicação funcional. Uma transformação pode testar essa hipótese; não estabelece sozinha o mecanismo. [Fonte](https://pmc.ncbi.nlm.nih.gov/articles/PMC6094095/).

Sailer e Harms (2017) ajustam a não linearidade do mapa genótipo–fenótipo antes de avaliar os termos epistáticos restantes, encontrando epistasia de ordem superior mesmo após o ajuste. A não aditividade original não se torna falsa: ela pertence à escala original. [Fonte](https://pmc.ncbi.nlm.nih.gov/articles/PMC5340324/).

Otwinowski (2018) oferece uma cautela concreta: um modelo biofísico com contribuições aditivas para dobramento e ligação pode produzir epistasia na fração ligada. Diferentes propriedades latentes participam da resposta; por isso, falhar em remover a epistasia com uma única transformação escalar não prova um acoplamento específico. A interpretação biológica exige hipóteses físicas e validação independente. [Fonte](https://pmc.ncbi.nlm.nih.gov/articles/PMC6188545/).

## Como adaptar os trabalhos anteriores

| Trabalho | Construção realizada | Adaptação proposta e limite |
|---|---|---|
| Beerenwinkel, Pachter e Sturmfels (2007) | Genótipos ocupam vértices de um politopo; aptidões funcionam como alturas, induzindo subdivisões regulares e, genericamente, triangulações. | Usar como precedente de uma geometria definida a partir dos dados. Trocar genótipos por componentes de interação exige definir novas coordenadas e proximidades; não é uma aplicação automática da mesma construção. |
| Eble et al. (2019) | Regiões adjacentes da subdivisão recebem pesos epistáticos. A inclusão de conexões por limiares produz componentes conectados e partições aninhadas. | É o precedente mais direto para passar de geometria a hierarquia. Na proposta, definir primeiro relações entre interações, depois investigar agrupamentos por níveis. A hierarquia original agrupa regiões da paisagem; não demonstra uma classificação multirrótulo de interações. |
| Costanzo et al. (2016) | Genes são comparados pelos seus perfis de interações genéticas, com organização associada a níveis da função celular. | Construir perfis comparáveis para as próprias interações e confrontar a organização com evidência biológica. A mudança de genes para interações é uma hipótese metodológica nossa. |
| Carlsson e Mémoli (2010) | Formalizam dendrogramas como espaços ultramétricos e estudam estabilidade e convergência de procedimentos hierárquicos. | Avaliar fidelidade e estabilidade da hierarquia, sem supor que toda geometria se acomode numa árvore. Suas garantias dependem do procedimento e das hipóteses. |

Fontes: [Beerenwinkel et al.](https://www3.stat.sinica.edu.tw/statistica/oldpdf/A17n43.pdf), [Eble et al.](https://doi.org/10.1007/s00285-019-01381-0), [Costanzo et al.](https://pubmed.ncbi.nlm.nih.gov/27708008/), [Carlsson e Mémoli](https://jmlr.org/papers/v11/carlsson10a.html).

A sequência proposta é: definir componentes → descrevê-los por propriedades comparáveis → definir proximidades → estudar organização geométrica → investigar hierarquia e sobreposição → confrontar com evidência funcional ou biológica. O objeto coletivo é o padrão de interações de um dataset; cada componente é um objeto dentro dessa configuração. Isso não exige começar por comparar datasets inteiros.

A construção de uma hierarquia e o treinamento de um classificador hierárquico multirrótulo são etapas distintas. Se uma interação participar de vários grupos, precisamos explicitar como representaremos a sobreposição. Atribuir vários rótulos não garante que uma árvore de agrupamentos represente todas as relações.

## Visualização e papel das transformações

Uma visualização é um produto de pesquisa legítimo se permitir inspecionar relações, formular hipóteses e rastrear seus fundamentos, mesmo antes de existir um detector supervisionado. Proposta ainda não implementada:

- Mapa de interações, com pontos selecionáveis, sinais, magnitudes, ordens e incerteza.
- Matriz de distâncias como referência para conferir a projeção espacial.
- Hierarquia vinculada ao mapa, exibindo pertencimentos múltiplos quando necessários.
- Acesso ao efeito original e às observações que sustentam cada componente.
- Comparação entre escalas ou contextos, preservando a correspondência dos objetos.

Uma projeção 2D ou 3D pode distorcer distâncias; um grupo visual não é evidência suficiente de módulo biológico. As proximidades precisam ser verificadas no espaço original dos descritores e em reamostragens. Descritores de ordens diferentes exigem comparabilidade; não basta calcular produtos internos entre componentes ortogonais de uma fANOVA e esperar encontrar módulos.

Transformações têm dois usos diferentes: sondar sensibilidade à escala, ou representar uma hipótese explícita de ligação entre propriedades latentes e resposta observada. Para estudar seu efeito, transformar a resposta e recalcular a decomposição sob regras consistentes; mover apenas pontos de um gráfico não equivale a essa análise. Normalização dos descritores também é outra operação. Uma sequência de transformações não é necessária: cada membro de uma família pode ser aplicado diretamente à resposta original.

Os limiares que formam a hierarquia de Eble não são transformações da resposta. Uma animação das mudanças geométricas só terá interpretação se mantiver coordenadas comparáveis; projeções refeitas livremente podem aparentar movimento por rotação ou reorganização do desenho. O uso de trajetórias permanece hipótese a testar, não requisito para justificar toda visualização estática.

## Referências e alcance da consulta

Consulta dirigida em 13/11/2026. Foram consultados trechos pertinentes dos textos de Lengerich, Sailer e Harms, dos dois trabalhos de Otwinowski e de Beerenwinkel; resumo e seções metodológicas recuperadas de Eble; resumo/figuras e material oficial de Costanzo; resumo e trechos de Carlsson e Mémoli. Para Hooker, a fundamentação aqui se limita ao resumo consultado. Não se afirma leitura integral de todos os artigos.

- Lengerich et al. (2020). *Purifying Interaction Effects with the Functional ANOVA: An Efficient Algorithm for Recovering Identifiable Additive Models*. PMLR 108:2402–2412. https://proceedings.mlr.press/v108/lengerich20a.html
- Hooker (2007). *Generalized Functional ANOVA Diagnostics for High-Dimensional Functions of Dependent Variables*. DOI: 10.1198/106186007X237892.
- Sailer e Harms (2017). *Detecting High-Order Epistasis in Nonlinear Genotype-Phenotype Maps*. DOI: 10.1534/genetics.116.195214.
- Otwinowski, McCandlish e Plotkin (2018). *Inferring the shape of global epistasis*. DOI: 10.1073/pnas.1804015115.
- Otwinowski (2018). *Biophysical inference of epistasis and the effects of mutations on protein stability and function*. DOI: 10.1093/molbev/msy141.
- Beerenwinkel, Pachter e Sturmfels (2007). *Epistasis and shapes of fitness landscapes*. Statistica Sinica 17:1317–1342. https://www3.stat.sinica.edu.tw/statistica/oldpdf/A17n43.pdf
- Eble et al. (2019). *Cluster partitions and fitness landscapes of the Drosophila fly microbiome*. DOI: 10.1007/s00285-019-01381-0.
- Costanzo et al. (2016). *A global genetic interaction network maps a wiring diagram of cellular function*. DOI: 10.1126/science.aaf1420.
- Carlsson e Mémoli (2010). *Characterization, Stability and Convergence of Hierarchical Clustering Methods*. JMLR 11:1425–1470. https://jmlr.org/papers/v11/carlsson10a.html

## Pendências

Escolher resposta e distribuição de referência para o próximo estudo; definir a comparabilidade entre interações; especificar distâncias e critérios de estabilidade; separar evidência funcional de interpretação mecanística; determinar quais anotações ou experimentos permitirão validação biológica. As escolhas acima são propostas do assistente fundamentadas nas fontes, ainda sujeitas à decisão do pesquisador.

## Complemento de 13/11/2026 — O que significa estar perto?

O pesquisador apontou que a resposta anterior não explicitava as definições de proximidade existentes na literatura. A correção é: há definições operacionais concretas e procedimentos de validação; o que permanece aberto é sua transferência para componentes de interação como objetos.

**Costanzo et al. (2016): semelhança de perfis relacionais.** Cada gene é descrito por um vetor de escores de interação com outros genes. A similaridade é calculada pela correlação de Pearson entre esses vetores. Alta correlação positiva significa que os perfis variam de maneira semelhante ao longo dos mesmos parceiros, após centralização e normalização. O significado funcional é avaliado com referências externas, incluindo processos GO, complexos e vias. Não se trata de definir proximidade como “mesmo mecanismo” por convenção. O suplemento explicita os coeficientes e a avaliação por enriquecimento. [Fonte primária: suplemento oficial](https://boonelab.ccbr.utoronto.ca/supplement/costanzo2016/).

Exemplo inventado: perfis (−2, 0, 2) e (−4, 0, 4) têm correlação 1, embora magnitudes diferentes. A escolha da medida determina se essa diferença conta. Para perfis não constantes, uma opção matemática de distância é a distância euclidiana entre vetores centralizados e normalizados para norma 1: d = sqrt(2(1 − r)). Essa expressão é uma possibilidade de adaptação; não se afirma que foi a distância usada por Costanzo na hierarquia. Ela identifica perfis que diferem apenas por escala positiva e deslocamento; portanto é uma métrica nos perfis normalizados, não uma métrica que distingue todos os vetores originais. Perfis constantes exigem tratamento próprio.

**Eble et al. (2019): pequena separação epistática entre regiões adjacentes.** Os pesos medem quanto os simplexos levantados adjacentes se afastam de uma configuração afim comum, de forma análoga a uma dobra. Regiões ligadas por pesos menores são reunidas primeiro; a filtração gera partições aninhadas. Dois elementos podem entrar no mesmo grupo por uma cadeia de conexões, sem serem adjacentes entre si. Trata-se de um grafo com pesos e uma hierarquia induzida; não de uma distância euclidiana previamente definida entre todas as interações. [Fonte primária, introdução e construção](https://pmc.ncbi.nlm.nih.gov/articles/PMC8174236/).

**Deshpande, VanderSluis e Myers (2013): escolher similaridade por avaliação funcional.** O estudo compara medidas em dados de S. cerevisiae e S. pombe, avaliando recuperação de relações funcionais com uma referência baseada em Gene Ontology, além de estabilidade com perfis parciais e perturbações. O produto interno foi consistentemente competitivo nas condições estudadas; medidas normalizadas mostraram vantagens para pares mais similares e limitações em outras condições. Isso não demonstra superioridade universal de uma medida. [Comparison of Profile Similarity Measures for Genetic Interaction Networks, PLOS ONE 8(7):e68664](https://doi.org/10.1371/journal.pone.0068664).

**Proposta para o projeto, ainda não validada:** definir proximidade entre interações como semelhança de seus perfis de efeito em um conjunto comum de contextos ou sondas. As coordenadas precisam ter o mesmo significado entre objetos; ordens e domínios diferentes não são automaticamente comparáveis. Comparar medidas que preservam magnitudes com medidas que comparam perfis normalizados, mantendo a distinção entre similaridade e distância. Verificar depois se vizinhanças recuperam organizações conhecidas ou relações biológicas externas. Se o perfil for construído sob transformações, proximidade significará resposta semelhante àquelas transformações, e não automaticamente função biológica compartilhada.

Síntese: a literatura oferece pelo menos proximidade por comportamento relacional e proximidade por continuidade geométrica local. Nossa definição pode se apoiar nelas. A afirmação biológica depende de validação além da própria regra usada para aproximar os objetos.

Alcance da consulta adicional: suplemento oficial de Costanzo; trechos indexados do texto de Eble; resumo, resultados e métodos recuperados do artigo primário de Deshpande et al. Algumas aberturas diretas do PMC retornaram verificação de navegador; os trechos do texto foram recuperados pela busca. Não houve experimento novo.
