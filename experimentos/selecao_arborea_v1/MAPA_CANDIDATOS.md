# Mapa de candidatos e decisões

Registro de 23/11/2026. Os 59 registros são objetos bibliográficos, variantes e controles, não 59 algoritmos independentes. O inventário antigo contém agrupamentos que precisam ser desmembrados. Não se declara revisão sistemática nem exaustividade.

| ID | Candidato | Decisão | Justificativa |
|---|---|---|---|
|M01|Random Forest (RF), floresta de probabilidade|referencia|RF de Breiman como âncora histórica; não selecionado por resultado do piloto.|
|M02|Interaction Forests (IF) com Effect Importance Measure (EIM)|elegivel|Preditor arbóreo com divisões bivariadas; EIM não é pré-requisito da régua.|
|M03|iterative Random Forests (iRF) com RIT e estabilidade por bootstrap|elegivel|Comparar a floresta da última iteração; RIT constitui leitura secundária.|
|M04|signed iterative Random Forests (siRF / s-iRF)|leitura_secundaria|Procedimento de leitura/inferência; não presumir novo preditor.|
|M05|Neural Interaction Detection (NID) sobre MLP|fora_recorte_primario|Inventário anterior: modelo não arbóreo ou pipeline externo à definição; decisão preliminar de triagem, sem alegação de revisão integral.|
|M06|Perceptron multicamadas (MLP) como preditor|fora_recorte_primario|Inventário anterior: modelo não arbóreo ou pipeline externo à definição; decisão preliminar de triagem, sem alegação de revisão integral.|
|M07|Random Planted Forest (RPF), max_interaction = 2|elegivel_software|Classificação logística sustentada pelo software auditado; registrar diferença para o artigo de regressão e para a versão antiga.|
|M08|RPF aditivo (max_interaction = 1) como controle|controle_pendente|Ablação de ordem um; não representa outro algoritmo; exige teste próprio.|
|M09|Explainable Boosting Machine (EBM) / GA²M com FAST|elegivel|EBM é ajuste baseado em árvores com termos individuais e pares; não confundir com floresta de bagging.|
|M10|Estatística H de Friedman|leitura_secundaria|Procedimento de leitura/inferência; não presumir novo preditor.|
|M11|Valores de interação SHAP (TreeSHAP)|leitura_secundaria|Procedimento de leitura/inferência; não presumir novo preditor.|
|M12|Importância por permutação de pares (PPI)|leitura_secundaria|Procedimento de leitura/inferência; não presumir novo preditor.|
|M13|JVIMP e JMST (randomForestSRC find.interaction)|leitura_secundaria|Procedimento de leitura/inferência; não presumir novo preditor.|
|M14|glinternet (logística com pares e hierarquia forte, group-lasso)|fora_recorte_primario|Inventário anterior: modelo não arbóreo ou pipeline externo à definição; decisão preliminar de triagem, sem alegação de revisão integral.|
|M15|hierNet (lasso hierárquico)|fora_recorte_primario|Inventário anterior: modelo não arbóreo ou pipeline externo à definição; decisão preliminar de triagem, sem alegação de revisão integral.|
|M16|Regressão logística penalizada L2 com seleção stepwise de interações (stepPlr)|fora_recorte_primario|Inventário anterior: modelo não arbóreo ou pipeline externo à definição; decisão preliminar de triagem, sem alegação de revisão integral.|
|M17|Reluctant interaction modeling (sprinter/sprintr)|fora_recorte_primario|Inventário anterior: modelo não arbóreo ou pipeline externo à definição; decisão preliminar de triagem, sem alegação de revisão integral.|
|M18|MARS com termos produto (grau 2)|fora_recorte_primario|Inventário anterior: modelo não arbóreo ou pipeline externo à definição; decisão preliminar de triagem, sem alegação de revisão integral.|
|M19|Logic regression (LogicReg)|fora_recorte_primario|Inventário anterior: modelo não arbóreo ou pipeline externo à definição; decisão preliminar de triagem, sem alegação de revisão integral.|
|M20|logicDT (árvores de decisão com termos booleanos)|extensao_recodificacao|Requer preditores binários para a busca lógica; recodificação 0/1/2 deve ser protocolada e permutada por SNP completo.|
|M21|Multifactor Dimensionality Reduction (MDR)|fora_recorte_primario|Inventário anterior: modelo não arbóreo ou pipeline externo à definição; decisão preliminar de triagem, sem alegação de revisão integral.|
|M22|Model-Based MDR (MB-MDR)|fora_recorte_primario|Inventário anterior: modelo não arbóreo ou pipeline externo à definição; decisão preliminar de triagem, sem alegação de revisão integral.|
|M23|Teste de razão de verossimilhança logístico por par / BOOST|fora_recorte_primario|Inventário anterior: modelo não arbóreo ou pipeline externo à definição; decisão preliminar de triagem, sem alegação de revisão integral.|
|M24|Unity Forests (UFO) + unity VIM|elegivel_preprint|Interações motivam otimização conjunta das raízes; preprint identificado, sem presumir VIM como ranking de pares.|
|M25|Variantes de partição para interações puras em RF (Blum et al.)|pendente_classificacao|Implementação histórica simpleRSRF é de regressão; não converter sua saída em probabilidade por recorte; confirmar implementação binária antes de mudar status.|
|M26|Reinforcement Learning Trees (RLT)|elegivel_software|Procedimento de reforço explicitamente ativado; suporte de classificação conferido no pacote; artigo e implementação não são versões intercambiáveis.|
|M27|Random Interaction Forest (RIF)|pendente_implementacao|Resumo institucional do RIF de Guo e Lin confirmado; código dos autores não localizado nesta busca. Não confundir com outro RIF de biomarcadores.|
|M28|BART e DP-Forests (detecção de interação em ensembles bayesianos)|desmembrar_objetos|BART geral é referência ampliada; o artigo primário de DP-Forests formula regressão normal. Classificação nativa de DP-Forests não confirmada; não inferir do suporte binário de BART.|
|M29|Gradient boosting com árvores (XGBoost) + interações SHAP|referencia_ampliada|Modelo generalista ou grupo heterogêneo; separar variantes antes de eventual inclusão.|
|M30|RuleFit / Prediction Rule Ensembles (pre)|fora_modelo_final|Regras originadas de árvores com ajuste final de coeficientes constituem outra classe operacional; escopo futuro possível.|
|M31|SIRUS e FIGS (regras estáveis; soma de árvores)|referencia_ampliada|Modelo generalista ou grupo heterogêneo; separar variantes antes de eventual inclusão.|
|M32|GAMI-Net|fora_recorte_primario|Inventário anterior: modelo não arbóreo ou pipeline externo à definição; decisão preliminar de triagem, sem alegação de revisão integral.|
|M33|Sparse Interaction Additive Networks (SIAN)|fora_recorte_primario|Inventário anterior: modelo não arbóreo ou pipeline externo à definição; decisão preliminar de triagem, sem alegação de revisão integral.|
|M34|Neural Additive Models (NAM)|fora_recorte_primario|Inventário anterior: modelo não arbóreo ou pipeline externo à definição; decisão preliminar de triagem, sem alegação de revisão integral.|
|M35|Integrated Hessians; Archipelago; GEH bayesiano|leitura_secundaria|Procedimento de leitura/inferência; não presumir novo preditor.|
|M36|Diamond (descoberta de interações não aditivas com controle de FDR por knockoffs)|leitura_secundaria|Procedimento de leitura/inferência; não presumir novo preditor.|
|M37|iLOCO (inferência livre de distribuição para interações)|leitura_secundaria|Procedimento de leitura/inferência; não presumir novo preditor.|
|M38|Decomposição funcional ANOVA para caixas-pretas; purificação|leitura_secundaria|Procedimento de leitura/inferência; não presumir novo preditor.|
|M39|Additive Groves (modelos restritos × irrestritos)|pendente_probabilidades|Árvores e detecção por restrição são pertinentes; documentação trabalha com modelo de regressão e critérios RMS/ROC; interface probabilística não verificada.|
|M40|Screen and Clean (SC)|fora_recorte_primario|Inventário anterior: modelo não arbóreo ou pipeline externo à definição; decisão preliminar de triagem, sem alegação de revisão integral.|
|M41|Lasso logístico em duas etapas para GWAS|fora_recorte_primario|Inventário anterior: modelo não arbóreo ou pipeline externo à definição; decisão preliminar de triagem, sem alegação de revisão integral.|
|M42|epiForest (RF + seleção sequencial + estatística B)|fora_recorte_primario|Inventário anterior: modelo não arbóreo ou pipeline externo à definição; decisão preliminar de triagem, sem alegação de revisão integral.|
|M43|TRM (RF → MARS)|fora_recorte_primario|Inventário anterior: modelo não arbóreo ou pipeline externo à definição; decisão preliminar de triagem, sem alegação de revisão integral.|
|M44|RF → redes bayesianas (CaMML)|fora_recorte_primario|Inventário anterior: modelo não arbóreo ou pipeline externo à definição; decisão preliminar de triagem, sem alegação de revisão integral.|
|M45|Triagem por RF → MDR|fora_recorte_primario|Inventário anterior: modelo não arbóreo ou pipeline externo à definição; decisão preliminar de triagem, sem alegação de revisão integral.|
|M46|Boosting L2 em espaço ortogonal aos efeitos principais|fora_recorte_primario|Inventário anterior: modelo não arbóreo ou pipeline externo à definição; decisão preliminar de triagem, sem alegação de revisão integral.|
|M47|Blocos para triagem de interações (subamostragem + RF + ortogonalização) com CoxBoost|fora_recorte_primario|Inventário anterior: modelo não arbóreo ou pipeline externo à definição; decisão preliminar de triagem, sem alegação de revisão integral.|
|M48|Permuted Random Forest (pRF) e redes PRFN|leitura_secundaria|Procedimento de leitura/inferência; não presumir novo preditor.|
|M49|MCFS-ID (Monte Carlo Feature Selection and Interdependency Discovery)|leitura_secundaria|Procedimento de leitura/inferência; não presumir novo preditor.|
|M50|GUIDE (árvore única com testes de interação na escolha do split)|pendente_acesso_implementacao|GUIDE é pertinente, inclusive classificação e florestas. Acesso ao manual oficial exigiu verificação interativa e o download oficial do binário expirou nesta consulta. Não auditaram-se probabilidades nem interface automatizada.|
|M51|Regressão logística só com efeitos principais (controle nulo paramétrico)|controle_pendente|Controle aditivo no logit, fora do estrato de competidores; implementação ainda não auditada nesta rodada.|
|M52|Duas etapas com triagem marginal para G×G (Kooperberg & LeBlanc)|fora_recorte_primario|Inventário anterior: modelo não arbóreo ou pipeline externo à definição; decisão preliminar de triagem, sem alegação de revisão integral.|
|M53|Duas etapas com filtragem independente para G×E (Dai et al.)|fora_recorte_primario|Inventário anterior: modelo não arbóreo ou pipeline externo à definição; decisão preliminar de triagem, sem alegação de revisão integral.|
|M54|Busca exaustiva de dois locos × triagem marginal (Marchini, Donnelly & Cardon)|fora_recorte_primario|Inventário anterior: modelo não arbóreo ou pipeline externo à definição; decisão preliminar de triagem, sem alegação de revisão integral.|
|M55|SNPInterForest|pendente_acesso_implementacao|Artigo primário identifica o software SNPInterForest; endereço oficial indicado não ficou acessível nesta consulta. Não substituir por reimplementação própria.|
|M56|SNPHarvester|fora_recorte_primario|Inventário anterior: modelo não arbóreo ou pipeline externo à definição; decisão preliminar de triagem, sem alegação de revisão integral.|
|N01|LSSFind / Depth Weighted Prevalence|leitura_secundaria|Recuperação de interações em ensemble sob modelo LSS; não contar automaticamente como novo preditor.|
|N02|Extra Trees|referencia_ampliada|Referência generalista adicional; não implica mecanismo específico de detecção de pares. Nenhuma execução nesta rodada.|
|N03|lo-siRF|pendente_evidencia|Pipeline candidato; distinguir triagem, transformação da resposta, ajuste e extração antes de inclusão.|

## Leitura das decisões

O núcleo técnico examinado tem sete procedimentos, incluindo RF como referência. A auditoria desses sete não elimina automaticamente os demais elegíveis. GUIDE, RIF, variantes bayesianas voltadas a interação e pipelines com mudança de representação permanecem lacunas explícitas. A seleção final para uma nova avaliação depende de fechar essas decisões com a mesma regra; não se atribui inferioridade a métodos não executados.

Uma escolha apenas entre pacotes prontamente integráveis é uma amostra de conveniência operacional. Ela pode sustentar um estudo delimitado, mas não a afirmação de que se comparou o universo dos métodos arbóreos.
