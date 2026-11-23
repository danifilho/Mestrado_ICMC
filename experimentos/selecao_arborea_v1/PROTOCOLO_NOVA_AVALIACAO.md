# Protocolo da comparação arbórea

Versão documental 1, 23/11/2026. Ler o estado de liberação em `CONGELAMENTO.json` antes de executar. Este protocolo especifica uma avaliação futura; os arquivos de `resultados/` nesta pasta contêm somente verificações técnicas.

## O que se pretende estabelecer

O estudo compara a dependência preditiva de pares sob uma operação comum, depois do ajuste de modelos diferentes. Investiga se proximidade preditiva acompanha concordância dos pares priorizados e se a divergência entre modelos excede a variabilidade de ajuste do mesmo modelo. O resultado será condicionado aos algoritmos, configurações e geradores examinados. A recuperação de interações específicas é uma pergunta secundária distinta da importância conjunta.

A seleção parte dos critérios datados em `CRITERIOS_ANTES_DOS_TESTES.md`. Preprints são permitidos, com identificação explícita. Uma implementação posterior ao artigo não será apresentada como reprodução daquela publicação. Ser elegível não basta para ser executável: o registro técnico acompanha cada candidato.

## Dados e alcance

O braço confirmatório proposto reutiliza as 20 configurações de geradores de Wright selecionadas no piloto, com novas realizações. São cinco modelos — sem termo produto, sinérgico, apenas termo produto, modificador e redundante — cruzados com quatro combinações de coeficientes e frequências. A comparação é condicional a esse subconjunto previamente conhecido, não uma amostra representativa de sistemas biológicos ou de todas as funções de interação.

Cada realização terá 1000 linhas de treino e 1000 de teste independente, 100 genótipos codificados 0/1/2, dois atributos designados, cinco com efeitos principais e 93 de ruído. As frequências dos atributos de ruído são fixadas por realização e compartilhadas entre treino e teste. A resposta deriva do modelo logístico de Wright; coeficientes de primeira ordem nulos no logit não implicam independência marginal entre atributo e resposta. Antes da liberação, o gerador, cujos fontes originais foram preservados em `fontes/wright/`, precisa ter seu adaptador final vinculado a um arquivo específico com hash e ter suas probabilidades e frequências verificadas.

Todos os preditores recebem os 100 atributos. O universo de avaliação do primeiro braço são os 21 pares dos sete atributos designados pelo gerador. Isso utiliza informação do gabarito para delimitar a pergunta: é uma comparação **condicional a candidatos conhecidos**, não uma busca entre os 4950 pares possíveis. Não se deve relatar taxa de descoberta em dados de alta dimensão com esse braço. A busca sem informação do gabarito exige um braço adicional e orçamento próprio, especificados antes de executá-lo.

Prevê-se 100 realizações por cenário, três sementes de ajuste em cada uma e 30 permutações compartilhadas. Esses números preservam a comparabilidade com o piloto, não resultam de um cálculo de poder. Proporções e diferenças terão incerteza Monte Carlo reportada; nenhum limiar de significância será usado para interromper cedo a execução. A implementação das sementes futuras deverá usar derivação por hash de identificadores separados para dados, ajuste, permutação e bootstrap, com registro de colisões e nenhuma reutilização de sementes do piloto. A lista de sementes foi enumerada em `configs/sementes_futuras.csv`, sem gerar os dados; o adaptador efetivo integra o congelamento executável, ainda distinto deste documento.

## Ajustes e configurações

A comparação principal será de configurações documentadas, sem busca externa de hiperparâmetros por cenário. Seleção interna nativa, como OOB ou validação do próprio pacote, pertence ao procedimento e usa somente o treino. A mesma contagem de árvores não significa esforço, capacidade ou precisão equivalentes.

A auditoria registra uma configuração candidata por procedimento: RF com 500 árvores; iRF com cinco iterações de 500 árvores e previsão da última floresta, sem executar o extrator na comparação principal; IF com 2000 árvores e cálculo de EIM desativado nesta verificação preditiva; UFO com 20000 árvores e 500 raízes candidatas; RLT com reforço ativado e 100 árvores; RPF com perda logística e ordem máxima dois; EBM com configuração da versão fixada e `interactions='3x'`. Demais argumentos são os da implementação fixada e suas assinaturas são preservadas nos resultados técnicos. Esses ajustes não garantem equivalência de capacidade; o estudo compara esses procedimentos concretos.

Parâmetros de IF para extração de EIM e parâmetros de RIT/siRF precisam de auditoria própria antes de integrar o braço secundário. Não reaproveitar automaticamente os máximos entre sinais ou direções usados no piloto. Para RPF, a implementação nova e a perda logística constituem mudança explícita em relação ao ajuste L2 sobre resposta binária anterior. Para RLT, não confundir a distribuição CRAN 3.2.6 com a interface 6.1.1 do repositório de desenvolvimento.

Controles previstos: probabilidade constante estimada no treino e modelo logístico aditivo, ambos fora da lista de competidores arbóreos; RPF de ordem um e EBM sem pares são ablações desejáveis, mas só entrarão após teste técnico e novo registro de configuração anterior à avaliação. O controle logístico será ajustado sem consultar o par verdadeiro; a interface foi verificada em `resultados/CONTROLES.json`. A capacidade de todos os preditores será contextualizada por perda do oráculo probabilístico do gerador, que será avaliado, não ajustado.

## Régua comum

Para perda média L e função ajustada f, definir ΔS como a média, sobre as 30 permutações, de L(y,f(X com colunas S permutadas))−L(y,f(X)). As duas colunas de um par recebem a mesma permutação. Isso preserva a associação interna do par e rompe sua associação com o desfecho e os demais atributos. As permutações são idênticas entre todos os modelos na mesma realização.

Perda principal: log-loss, com corte numérico fixo das probabilidades em [10⁻¹⁵,1−10⁻¹⁵], registrando quantas previsões foram cortadas. Esse corte protege o cálculo, não calibra o modelo. A avaliação de escalas fica para a etapa posterior à qualificação.

Ranking principal: ΔAB decrescente, sem valor absoluto. Pares com valores negativos permanecem na tabela. Análise secundária: contraste C_AB=ΔAB−ΔA−ΔB, com sinal preservado e |C_AB| como resumo explicitamente secundário. Nenhum sinal será escolhido depois de olhar os resultados. Esses contrastes não equivalem automaticamente a um componente de interação na função verdadeira.

Medida principal de concordância: Jaccard dos conjuntos top-3. Top-1 a top-10 serão curva secundária completa, sem escolher o k favorável. Empates na fronteira serão incluídos integralmente, reportando o tamanho efetivo; ranking completamente empatado será marcado como não informativo, sem Jaccard interpretável. O comparador ao acaso usará conjuntos com os mesmos tamanhos efetivos e o mesmo universo. Essa correção é necessária porque conjuntos grandes sobrepõem-se por construção.

## Comparação e incerteza

Relatar todos os pares de métodos. Dentro de cada realização, a concordância entre métodos será a média das três comparações com índices de semente correspondentes. A estabilidade interna será a média dos três pares possíveis de sementes. Ambas usam os mesmos dados de teste e permutações. Não confundir essa estabilidade com replicação em novos dados.

A unidade de reamostragem é a realização completa: bootstrap pareado de 2000 amostras por cenário, mantendo sementes e modelos juntos. Resumos globais terão peso igual para cada um dos 20 cenários e escopo condicionado a esses cenários. Intervalos apresentados lado a lado não autorizam declarar um vencedor global por inspeção. Comparações serão inicialmente estimativas descritivas com intervalos, sem caçar subconjuntos favoráveis.

Proximidade preditiva será apresentada como diferença pareada de log-loss e intervalo de 95%, ao lado da concordância, sem transformar ausência de significância em equivalência. Uma análise descritiva destacará intervalos inteiramente dentro de ±0,005; ±0,0025 e ±0,01 serão sensibilidades completas. São margens operacionais, sem interpretação biológica estabelecida. Uma afirmação confirmatória formal de equivalência entre muitos modelos exige definir família de testes e ajuste de multiplicidade antes da liberação.

O par designado pelo gerador terá posição e presença no topo reportadas separadamente por cenário e por medida. No cenário sem termo produto, a sua presença no topo de ΔAB não é falso positivo de interação: ΔAB não testa a ausência de produto. Um top-k fixo sempre retorna candidatos e, sem regra de decisão calibrada, não estima FDR ou erro tipo I.

## Falhas e salvaguardas

Guardar falhas por método, cenário e realização; nunca substituir por zero. Informar denominadores e análise em casos completos, acompanhada de padrão de falhas. Não excluir algoritmos por perda preditiva ruim. Não modificar a configuração após acessar o teste. Mudanças por incompatibilidade devem abrir nova versão antes de continuar, com preservação das tentativas.

Antes da execução científica devem passar: gerador, controles, todos os adaptadores selecionados, régua, reprodutibilidade, serialização, orçamento de tempo/memória e código da análise. Os testes atuais cobrem apenas parte dessa cadeia. O congelamento documental não libera automaticamente o estudo.

## Fontes e interpretação

Wright et al. (2016), https://doi.org/10.1186/s12859-016-0995-8, motiva a distinção entre efeitos individuais e interação e fornece os geradores. Fisher et al. (2019), https://www.jmlr.org/papers/v20/18-760.html, fundamenta a dependência preditiva medida por perturbação; não demonstra que a medida conjunta identifica interação pura. Weber et al. (2019), https://doi.org/10.1186/s13059-019-1738-8, fundamenta transparência na escolha de métodos e configurações. As escolhas específicas de amostragem, margens e resumos acima são decisões do estudo.

O ensaio poderá revelar concordância ou divergência de dependência preditiva sob esta régua e nestes geradores. A atribuição de significado biológico exigirá dados e evidências externos, em investigação posterior.
