# Seleção operacional para a primeira comparação arbórea

Data: 23/11/2026. Esta seleção delimita a primeira versão operacional do estudo. Não é uma amostra representativa nem uma lista exaustiva de algoritmos arbóreos. Seu estado de congelamento e liberação consta de `CONGELAMENTO.json`.

## Pergunta fixada

Em classificação binária, modelos arbóreos voltados à exploração de interações priorizam os mesmos pares quando submetidos à mesma perda por permutação conjunta? Como a concordância se relaciona ao desempenho preditivo e à estabilidade dentro de cada método?

A unidade comparada é o **procedimento de ajuste probabilístico com implementação e configuração fixadas**. A função resultante recebe a régua externa comum. Assim, o estudo compara a dependência preditiva de pares; não presume que a perda por permutação conjunta seja uma medida exclusiva de interação. A distinção entre importância conjunta e interação específica é parte central da interpretação.

## Composição da versão operacional

| Procedimento | Papel e vínculo com a pergunta | Implementação auditada |
|---|---|---|
| RF | Referência histórica do desenho de Wright; âncora para comparar modificações | ranger 0.18.0, floresta de probabilidade |
| IF | Exploração de efeitos conjuntos nas divisões bivariadas | diversityForest 0.6.0; previsão sem EIM nesta comparação principal |
| iRF | Reponderação iterativa dos atributos; avaliar a função final antes da extração por RIT | iRF 3.0.0, commit fixado dos autores |
| RPF | Restrição explícita de ordem e decomposição de contribuições | randomPlantedForest 0.5.0.9000, perda logística e ordem máxima dois |
| UFO | Otimização conjunta das raízes para explorar interações com pouco sinal marginal | unityForest 0.2.0; artigo em preprint identificado |
| RLT | Divisões orientadas por modelos internos de reforço, abordagem mencionada na discussão de Wright | RLT 3.2.6 com reforço ativado |
| EBM | Componentes ajustados por árvores, com efeitos principais e termos de pares | interpret-core 0.7.8 |

As referências individuais estão em `FONTES_E_BUSCAS.md`. Os vínculos acima explicam a pertinência dos procedimentos, mas não são usados como garantia de que cada método detecta uma definição universal de interação. As configurações exatas e os resultados técnicos estão nos JSON de auditoria.

Esta composição resulta de elegibilidade científica **e** acesso a uma implementação que foi submetida às mesmas verificações técnicas. Não resulta do desempenho do piloto. A presença de UFO e RLT amplia a lista anterior; NID/MLP não pertencem ao recorte arbóreo. Não há obrigação de manter um participante apenas porque já foi executado.

## O que ficou separado e por quê

siRF, RIT, H, SHAP, PPI, JVIMP e JMST são procedimentos de extração ou leitura que não serão contados automaticamente como novos preditores na régua. O braço de extração deve reutilizar uma função ajustada claramente identificada e protocolar seus próprios parâmetros. Ajustes separados não serão declarados idênticos sem verificação.

RSRF permanece como candidato para regressão ou para uma implementação binária nativa comprovada. logicDT exige um braço com recodificação dos genótipos e permutação conjunta dos indicadores de cada SNP. Modelos neurais, modelos lineares com produtos e pipelines cujo preditor final não seja arbóreo ficam fora do recorte principal, podendo fundamentar extensões.

GUIDE, RIF e SNPInterForest permanecem cientificamente pertinentes, mas não integrados à versão executável: existem lacunas concretas de acesso ou de auditoria de implementação registradas no mapa. Isso é uma limitação operacional da seleção, não uma exclusão por inferioridade. Antes de chamar o estudo de revisão abrangente ou comparação do campo, essas lacunas devem ser resolvidas. Um novo candidato pode entrar em versão posterior, antes da nova avaliação e com as mesmas regras.

BART geral e outros modelos generalistas constituem referências ampliadas. A referência obrigatória nesta versão é RF pela ligação direta com Wright. O artigo específico de DP-Forests foi formulado para regressão; não se infere suporte binário dessa variante a partir do suporte binário de BART. Essas distinções evitam agrupar métodos diferentes sob uma única linha de elegibilidade.

## Padrões e adaptações explícitas

O pesquisador priorizou padrões dos autores, com teto computacional definido depois da estimativa. Não foi aplicada uma contagem uniforme de árvores. IF usa o padrão preditivo de 2000 árvores nesta versão; 20000 é a configuração associada ao cálculo de importância e foi preservada no histórico da auditoria.

“Priorizar padrões” não significa que todos os argumentos são literalmente defaults: os métodos foram configurados para probabilidades, uma thread e preservação do modelo; RLT exige ativar o reforço; RPF usa ordem máxima dois e perda logística explícita; iRF usa cinco iterações e desliga a extração na comparação principal. São escolhas funcionais registradas, não parâmetros ajustados à recuperação do gabarito. A restrição de ordem do RPF deve acompanhar a interpretação e qualquer comparação futura com interações de ordem superior.

As versões de desenvolvimento ou extensões de software são identificadas como tais. A seleção não constitui reprodução literal de todos os artigos de origem.

## Limites do congelamento

O congelamento fixa esta composição operacional, os critérios, as configurações auditadas e o protocolo documental. Ele não autoriza automaticamente uma execução cujo custo total ainda não foi definido. O protocolo futuro ainda requer integração e verificação do gerador, código da análise e execução completa da régua na infraestrutura escolhida. Mudanças de composição, versões, configurações, cenários ou análises exigem nova versão anterior à avaliação científica.

O artigo de UFO harmoniza seu RF comparador, inclusive em 20000 árvores. Esta versão compara os procedimentos nas configurações próprias registradas. Assim, a conclusão recai sobre o procedimento completo, e não sobre o efeito causal isolado de modificar o algoritmo. Igualar a régua não elimina diferenças de hiperparâmetros ou de ajuste.
