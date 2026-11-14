# Geometria, difusão e epistasia de ordem superior

**Discussão e registro: 14/11/2026.** Fonte: conversa do pesquisador com o assistente; consulta dirigida a textos e metadados. Nenhum experimento executado nesta atualização. [Metadados, DOI e citações dos 17 artigos](Catalogo-bibliografico.md).

## Pergunta preservada

Que geometria o conjunto de interações de um único dataset apresenta, como essa geometria se deforma sob transformações da resposta e quais relações entre formas e deformações caracterizam diferentes organizações das interações?

Os objetos de interesse são as interações. Representar células, genes ou genótipos em um espaço é um precedente, mas não valida automaticamente a representação de componentes de interação.

## Coifman et al. (2005): construir a geometria

**Geometric diffusions as a tool for harmonic analysis and structure definition of data: Diffusion maps. PNAS, 102(21), 7426–7431.** [DOI](https://doi.org/10.1073/pnas.0500334102). Consulta: texto e resumo.

O método constrói geometria multiescala a partir de afinidades locais e operadores de difusão. Fornece uma possível base para representar interações por descritores e organizar suas relações. A transferência para interações é uma proposta nossa: a distância inicial e sua relevância precisam ser justificadas. Difusão não demonstra mecanismo comum nem unicidade da assinatura.

## Otwinowski, McCandlish e Plotkin (2018): por que investigar transformações

**Inferring the shape of global epistasis. PNAS, 115(32), E7550–E7558.** [DOI](https://doi.org/10.1073/pnas.1804015115). Já registrado em Trabalhos relacionados; mantido sem duplicação bibliográfica. Consulta: texto e resumo.

Contribuições aditivas latentes passam por uma função monótona não linear para produzir a resposta observada. A curva compartilhada pode explicar numerosos efeitos epistáticos. Isso fundamenta investigar respostas coordenadas às transformações; não prova que trajetórias semelhantes identifiquem uma causa comum. A “forma” do título é a curva de resposta, não a configuração espacial das interações.

## Coifman e Maggioni (2006): geometria e hierarquia

**Diffusion wavelets. Applied and Computational Harmonic Analysis, 21(1), 53–94.** [DOI](https://doi.org/10.1016/j.acha.2006.04.004). Consulta: resumo e introdução do texto.

Constroem representações e bases em diferentes resoluções a partir de operadores de difusão. É uma ligação matemática entre geometria e organização hierárquica. A hierarquia de espaços e bases não deve ser confundida com dendrograma de grupos exclusivos, árvore de decisão ou classificador HMC. [Código dos autores](https://mauromaggioni.duckdns.org/?page_id=105).

## Kuchroo et al. (2022): aplicação biológica multiescala

**Multiscale PHATE identifies multimodal signatures of COVID-19. Nature Biotechnology, 40, 681–691.** [DOI](https://doi.org/10.1038/s41587-021-01186-x). Consulta: resumo e descrição metodológica recuperada; não se declara leitura integral.

Combina condensação por difusão e PHATE para produzir agrupamentos e visualizações de dados biológicos em várias granularidades. É um precedente aplicado para examinar organização geral e subpopulações. Os objetos originais são células; substituir esses objetos por interações requer avaliação própria. [Código](https://github.com/KrishnaswamyLab/Multiscale_PHATE).

## Weinreich et al. (2013): definir componentes e avaliar consequências

**Should evolutionary geneticists worry about higher-order epistasis? Current Opinion in Genetics & Development, 23(6), 700–707.** [DOI](https://doi.org/10.1016/j.gde.2013.10.007). Consulta: Box 1, exemplos, reconstrução e conclusões do texto.

Usa a transformação de Walsh para decompor paisagens combinatoriamente completas em ordens de interação. Retirar termos superiores, reconstruir a paisagem e avaliar caminhos evolutivos permite investigar consequências dos componentes. Também considera uma resposta não linear de dobramento sobre energias aditivas. Limitações reconhecidas incluem dados completos e ausência de avaliação sistemática do erro experimental.

### Consequências para nosso desenho — interpretação e propostas

- Ordem matemática não equivale à complexidade do mecanismo: muitos termos podem compartilhar uma explicação simples.
- Um par médio pode esconder mudanças de contexto. Exemplo ilustrativo nosso: interação A–B igual a +2 sem C e −2 com C, com média zero.
- Geometria apenas dos pares marginalizados não deve ser chamada de geometria completa de todas as interações.
- Walsh é mudança linear de coordenadas da função; log/Box–Cox mudam a escala da resposta. Não confundir essas operações.
- Para variáveis binárias, desenho completo e medida produto uniforme, a expansão ortogonal de Walsh tem correspondência com os componentes por subconjuntos da fANOVA, respeitando normalização e codificação.
- Comparar a geometria proposta com referências simples: coeficientes, energia por ordem e configuração inicial. Testar se a representação preserva ou acrescenta capacidade de prever uma propriedade especificada.

## Hierarquia, HMC e transformações: três distinções

1. Hierarquia aprendida de interações é diferente da hierarquia dos rótulos de HMC. Os trabalhos acima não implementam automaticamente a tarefa IF-HMC.
2. Resolução/tempo de difusão é diferente do parâmetro de uma transformação da resposta. A primeira reorganiza a representação; a segunda exige recalcular as interações.
3. Uma árvore é uma candidata para representar a geometria. Sua fidelidade e utilidade precisam ser comparadas a representações não hierárquicas, especialmente com módulos sobrepostos.

## Decisões e pendências

Usar Coifman como fundamento geométrico; Otwinowski para a hipótese de não linearidade compartilhada; Diffusion wavelets e Multiscale PHATE como precedentes de organização multiescala; Weinreich para a decomposição e para exigir uma consequência científica verificável. Eble continua um precedente próximo, apesar da contagem pequena de citações. Citações não substituem adequação metodológica.

Não foi demonstrada novidade da combinação, identificação de mecanismos, vantagem das trajetórias ou necessidade de árvore. O relato do piloto 6 na conversa não foi reexecutado nem auditado nesta atualização. Nenhuma nova hipótese foi declarada confirmada.
