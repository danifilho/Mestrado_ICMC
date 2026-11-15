# Algoritmo

**Documentado em:** 14 de novembro de 2026 (America/Sao_Paulo).

**Status:** procedimento candidato e hipóteses em investigação; não é um algoritmo definitivo nem um protocolo congelado.

**Origem:** texto fornecido pelo pesquisador nesta conversa, com solicitação de publicação em tópico próprio. Conteúdo e links preservados abaixo. As menções a pilotos são relatos do texto fornecido; esta publicação não inclui reexecução de testes ou nova verificação bibliográfica.

---

**Estamos propondo um algoritmo para construir uma geometria das interações de um único conjunto de dados e acompanhar como essa geometria muda quando transformamos a resposta.** A hierarquia seria uma forma de organizar essa geometria, cuja utilidade precisamos testar.

Ainda não temos um algoritmo definitivo. Temos um procedimento candidato, algumas alternativas metodológicas e hipóteses que os pilotos estão ajudando a separar. Vou escrever essa versão sem apresentar escolhas ainda abertas como decisões tomadas.

**1. Receber os dados e definir qual resposta estamos estudando**

A entrada seria uma tabela com variáveis explicativas e uma resposta:

| A | B | C | D | Resposta |
|---|---|---|---|---|
| Ausente | Ausente | Ausente | Ausente | Valor medido |
| Presente | Ausente | Ausente | Ausente | Valor medido |
| Presente | Presente | Ausente | Ausente | Valor medido |
| … | … | … | … | … |

As variáveis poderiam representar mutações, perturbações de genes ou fatores simulados. A resposta poderia ser crescimento, atividade de uma proteína ou outra medida definida.

**Nesta primeira versão, começaríamos com combinações completamente observadas e uma resposta escalar.** Isso permite estudar a representação sem misturar imediatamente os problemas de dados faltantes e erro de um modelo preditivo.

Com dados ruidosos e réplicas, estimaríamos primeiro a resposta média de cada combinação. Depois transformaríamos essa média. Transformar cada observação antes de calcular a média define outro objeto.

**Fundamento:** Weinreich et al. (2013) trabalham com paisagens combinatoriamente completas para decompor seus efeitos. Essa é uma referência para começar com um problema controlado, não uma exigência universal para toda extensão futura. [gwern.net](https://gwern.net/doc/genetics/heritable/2013-weinrich.pdf?utm_source=chatgpt.com)

**2. Definir e calcular os componentes de interação**

Antes de construir pontos no espaço, precisamos dizer precisamente o que cada ponto representa.

A proposta inicial é usar **componentes de interação da fANOVA**, com uma distribuição de referência declarada. No fatorial completo, começaríamos com pesos uniformes.

Isso separaria a resposta em:

- Uma constante.
- Efeitos individuais de A, B, C e D.
- Componentes de pares, como AB e AC.
- Componentes de trios e ordens superiores.

O componente AB é uma função que descreve a contribuição conjunta atribuída a A e B depois de retirar as contribuições de ordem inferior, conforme as regras da decomposição.

**Fundamento:** Lengerich et al. (2020) mostram por que precisamos dessas restrições: sem elas, efeitos podem ser redistribuídos entre termos sem alterar a previsão. A geometria seria ambígua se seus objetos não estivessem bem definidos. [proceedings.mlr.press](https://proceedings.mlr.press/v108/lengerich20a.html?utm_source=chatgpt.com)

Para variáveis binárias e pesos uniformes, a expansão de Walsh discutida por Weinreich oferece uma formulação relacionada. **Não precisamos tratar Walsh e fANOVA como dois detectores concorrentes.**

**3. Representar cada interação por sua superfície de efeitos**

Um único número de intensidade é insuficiente para descrever a forma de uma interação.

Se A e B têm cinco níveis cada, o componente AB contém uma tabela de **25 valores**. Essa tabela descreve onde o efeito conjunto é positivo, negativo, forte ou fraco.

Podemos organizar esses 25 valores como coordenadas de um ponto. Fazemos o mesmo para AC, AD e os demais pares. Assim:

> **Cada ponto representa uma interação; a posição resulta do padrão de seus efeitos.**

Isso exige comparar domínios compatíveis. Não podemos alinhar arbitrariamente concentrações, categorias ou estados biológicos diferentes.

Também precisamos começar comparando interações da mesma ordem: pares têm superfícies diferentes de trios. Misturar os dois sem uma representação adequada pode produzir grupos que refletem apenas a ordem.

**Fundamento:** Beerenwinkel, Pachter e Sturmfels (2007) mostram como definir um objeto geométrico para caracterizar epistasia. **Nossa escolha de usar componentes de interação como pontos é diferente da deles**, que parte dos genótipos. Portanto, o artigo fundamenta o interesse da geometria, mas não fornece diretamente nossas coordenadas. [www3.stat.sinica.edu.tw](https://www3.stat.sinica.edu.tw/statistica/oldpdf/A17n43.pdf?utm_source=chatgpt.com)

**4. Aplicar uma família comum de transformações à resposta**

Escolhemos uma família declarada de transformações e aplicamos cada uma à mesma resposta original.

Para cada transformação, **recalculamos toda a decomposição**. Não basta transformar separadamente um componente que já foi calculado: em geral, isso não produz a decomposição da resposta transformada.

O propósito é perguntar:

> **Quais interações mudam de maneira coordenada quando alteramos a representação da resposta?**

Por exemplo, alguns componentes podem diminuir juntos; outros podem conservar sua forma ou mudar de sinal.

A família Box–Cox usada no piloto é uma candidata, não uma escolha definitiva. Sua utilização depende do domínio da resposta, e ajustes para torná-la aplicável precisam ser registrados. Uma curva aprendida nos dados também seria possível, mas exigiria separar ajuste e avaliação.

**Fundamento:** Otwinowski, McCandlish e Plotkin (2018) demonstram como uma não linearidade compartilhada sobre efeitos aditivos latentes pode explicar padrões extensos de epistasia. Isso justifica investigar explicações compartilhadas; **não demonstra que qualquer semelhança sob transformações identifique um mecanismo comum**. [openalex.org](https://openalex.org/works/W2790509526?utm_source=chatgpt.com)

**5. Separar magnitude e forma antes de definir proximidade**

Duas interações podem apresentar o mesmo desenho, mas intensidades muito diferentes. Precisamos decidir se essa diferença deve afastá-las.

Por isso, compararíamos pelo menos duas representações:

| Representação | O que preserva |
|---|---|
| Superfície original | Forma e magnitude |
| Superfície normalizada | Forma relativa, removendo uma medida de magnitude |

Uma terceira opção é guardar **forma e magnitude em canais separados**, permitindo avaliar a contribuição de cada uma.

Essa escolha é particularmente importante depois do piloto 6: pelo relato apresentado, a magnitude dominou a geometria principal, enquanto a análise exploratória da forma mostrou resultados mais promissores. Isso justifica um teste confirmatório; não estabelece que normalizar seja sempre melhor.

**Cuidado:** componentes quase nulos não têm uma direção confiável. Normalizá-los pode amplificar ruído. O procedimento precisa poder marcar uma interação como insuficientemente determinada, em vez de lhe atribuir uma forma artificial.

Esta etapa é uma **escolha metodológica nossa a avaliar**, e não uma consequência automática dos trabalhos de geometria.

**6. Construir a geometria de cada configuração e acompanhar suas mudanças**

Aqui existem dois objetos complementares:

- **Geometria em uma escala:** como as interações se distribuem após uma transformação específica.
- **Geometria das trajetórias:** quais interações apresentam comportamentos semelhantes ao longo de toda a família de transformações.

Primeiro, precisamos de uma distância explícita entre superfícies comparáveis. A distância euclidiana é uma referência simples. Depois, podemos testar uma construção por difusão:

1. Conectar interações semelhantes.
2. Atribuir pesos às conexões.
3. Construir um operador de difusão.
4. Obter distâncias e coordenadas que considerem a organização do conjunto.

**Fundamento:** Coifman et al. (2005) fornecem esse caminho de afinidades locais para uma geometria multiescala. Aplicá-lo às nossas superfícies é uma adaptação proposta. [www.wisdom.weizmann.ac.il](https://www.wisdom.weizmann.ac.il/~nadler/Publications/bn12_pnas1.pdf?utm_source=chatgpt.com)

Para estudar deformações, manteríamos a identidade de cada interação ao longo das transformações. Compararíamos mudanças nas distâncias e nas vizinhanças, além das trajetórias dos descritores.

**Não interpretaríamos o movimento em projeções 2D ou 3D independentes como deformação real.** Eixos podem girar ou inverter entre projeções. A evidência principal deve vir do espaço completo e de comparações consistentes.

**7. Construir uma hierarquia que resuma essa organização**

A árvore entraria depois de definir o objeto e sua proximidade. Suas folhas poderiam representar interações; os níveis superiores reuniriam comportamentos progressivamente mais abrangentes.

Precisamos, porém, distinguir duas possibilidades:

- Uma hierarquia de agrupamentos das interações.
- Uma hierarquia de representações matemáticas em diferentes resoluções.

**Diffusion wavelets**, de Coifman e Maggioni (2006), fundamenta especialmente a segunda. **Multiscale PHATE**, de Kuchroo et al. (2022), oferece um precedente aplicado para agrupamentos e visualizações multiescala. [www.math.ucdavis.edu](https://www.math.ucdavis.edu/~saito/data/diffgeomharm/ACHA-Special/diffusionwavelets.pdf?utm_source=chatgpt.com)

Ainda não escolhemos qual dessas construções será o algoritmo final. E a árvore precisa ser avaliada: se dois grupos se sobrepõem, uma estrutura de grupos exclusivos pode distorcer essa organização.

**Um ramo significaria inicialmente “interações semelhantes segundo o critério escolhido”.** Para chamá-lo de “explicação compartilhada”, precisaríamos mostrar, por ajuste e avaliação independentes, que uma explicação comum realmente descreve seus componentes.

**8. Entregar uma assinatura acompanhada de evidências**

A saída proposta seria:

- As interações calculadas e suas incertezas.
- A configuração espacial em cada transformação.
- As trajetórias e mudanças de proximidade.
- Uma hierarquia candidata, quando representar adequadamente essas relações.
- Medidas de estabilidade, distorção e informação preservada.

**“Assinatura” significa aqui uma representação comparável, não uma identidade única do sistema.** Sistemas diferentes podem produzir a mesma assinatura.

HMC não entra automaticamente nessa saída: uma hierarquia de interações não é a hierarquia dos rótulos. Uma aplicação posterior à classificação seria outra etapa de avaliação.

**9. Testar se essa representação acrescenta algo**

A pergunta experimental principal seria:

> **A organização geométrica e sua deformação permitem recuperar ou prever uma propriedade previamente definida do sistema gerador melhor do que representações mais simples?**

Para respondê-la, precisamos separar as contribuições:

| Comparação | O que queremos descobrir |
|---|---|
| Intensidades isoladas × superfícies completas | A forma acrescenta informação? |
| Configuração original × trajetórias | Transformar acrescenta informação? |
| Descritores diretos × geometria por difusão | As relações geométricas acrescentam informação? |
| Geometria × árvore | A hierarquia preserva ou melhora algo? |
| Dados ideais × ruído e dados faltantes | A conclusão permanece estável? |

Os geradores incluiriam curvas globais, módulos separados, módulos sobrepostos e efeitos dependentes de contexto. As avaliações usariam geradores e parâmetros não utilizados para escolher a representação.

Também precisamos de sistemas sem módulos e de casos em que mecanismos diferentes produzem observações indistinguíveis. Neles, não esperamos que o método invente uma distinção.

**Fundamento experimental:** Weinreich et al. avaliam consequências de retirar componentes e reconstruir paisagens. A inspiração para nós é exigir que a representação preserve algo relevante, além de produzir agrupamentos visualmente convincentes. [gwern.net](https://gwern.net/doc/genetics/heritable/2013-weinrich.pdf?utm_source=chatgpt.com)

**A contribuição que estamos tentando demonstrar é esta:** uma geometria das interações, acompanhada sob transformações da resposta, pode revelar regularidades coletivas úteis que não aparecem nas intensidades isoladas. A árvore é uma candidata para organizar essas regularidades. Se ela distorcer a geometria, ou se as trajetórias não acrescentarem informação à escala inicial, isso precisa aparecer como resultado — sem trocar a pergunta apenas para obter uma figura favorável.
