# Fontes e trilha da busca

Data da consulta: 23/11/2026. Mapeamento dirigido; não corresponde a uma busca exaustiva em bases bibliográficas. Resultados da busca serviram para localizar as páginas primárias abaixo. Resumos e documentação não são tratados como leitura integral do artigo.

## Ponto de partida

Foram consultados a matriz, as recomendações e o arquivo de evidências em `experimentos/levantamento_selecao_metodos_v1`, além da existência do levantamento `levantamento_selecao_metodos_2026-11-20`. O inventário anterior de 56 objetos foi preservado separadamente, sem validar retroativamente todas as suas afirmações. Foram lidos os adaptadores do Piloto 7 e as configurações A–D. Outros chats não foram consultados nesta auditoria; o contexto disponível foi a conversa fornecida e os arquivos locais.

## Consultas complementares

- `"Unity Forests" Hornung Hapfelmeier`
- `"interaction forests" classification Hornung Boulesteix 2022`
- `"random planted forest" classification logit`
- `"logicDT" binary covariates classification interaction paper`
- `"Reinforcement Learning Trees" RLT classification package`
- `"Additive Groves" interaction classification software`
- `tree interaction detection classification "GUIDE" "Additive Groves" algorithms`
- `random split random forest RSRF github regression`
- `benchmark studies computational methods neutral comparison Boulesteix selection methods 2013`
- `iRF 3.0.0 Kumbier github R package`
- `"Additive Groves" Sorokina 2008 interactions software`
- `"GUIDE" classification interactions Loh 2009`
- `"Reinforcement learning trees" Zhu Zeng Kosorok 2015 PMC`
- `"RSRF" "github" Hiabu Blum`
- `"Random Interaction Forest" Guo Lin 2023`

## Evidências verificadas

| Objeto | Fonte primária ou oficial | Leitura e uso |
|---|---|---|
| Comparações neutras | https://doi.org/10.1371/journal.pone.0061562 | Resumo e metadados; fundamenta transparência, não prescreve nossa lista |
| Benchmarking | https://doi.org/10.1186/s13059-019-1738-8 | Página integral disponível; seções de seleção/configuração consultadas |
| Régua | https://www.jmlr.org/papers/v20/18-760.html | Resumo e material anterior do projeto; MR não é MCR da classe inteira |
| iRF | https://arxiv.org/abs/1706.08457 | Resumo, publicação vinculada e código dos autores; ensemble iterativo e extração são objetos diferentes |
| iRF software | https://github.com/karlkumbier/iRF | Clone fixado em e983ca1627a40cfcf4a147278184db18411f93f6; DESCRIPTION e funções de ajuste/previsão examinadas |
| IF | https://doi.org/10.1016/j.csda.2022.107460 | Página do artigo e documentação; divisão bivariada e EIM |
| IF software | https://search.r-project.org/CRAN/refmans/diversityForest/help/interactionfor.html | Assinatura, classificação e execução da versão instalada 0.6.0 |
| UFO | https://arxiv.org/html/2601.07003v1 | Introdução, trabalhos relacionados e descrição das raízes; preprint explicitado |
| RPF | https://arxiv.org/abs/2012.14563 | Resumo e versões; não atribuir ao artigo original cada função nova do pacote |
| RPF software | https://plantedml.com/randomPlantedForest/ | Documentação e clone 4c9c28e3925f7ad04c161ffc32a85de239bfa86c; 0.5.0.9000, API nova |
| EBM | https://interpret.ml/docs/ebm.html | Definição oficial e API executada; boosting de árvores com termos de interação |
| RLT artigo | https://doi.org/10.1080/01621459.2015.1036994 | Resumo/metadados; acesso PMC não disponibilizou texto nesta consulta |
| RLT software | https://search.r-project.org/CRAN/refmans/RLT/html/RLT.html | Interface CRAN 3.2.6 e código R instalado; versão de desenvolvimento 6.1.1 identificada mas não substituída silenciosamente |
| logicDT | https://doi.org/10.1007/s10994-023-06488-6 | Página do artigo e documentação; preditores binários e recodificação necessária para genótipos |
| GUIDE | https://pages.cs.wisc.edu/~loh/guide.html | Descrição oficial: classificação, árvores e florestas, interação e previsão; contradiz exclusão automática por ser árvore única |
| Additive Groves | https://www.khoury.northeastern.edu/~mirek/papers/2008-ICML-Interactions.pdf | Resumo/metodologia disponível; restrição de funções para interação |
| Additive Groves software | https://dariasor.github.io/TreeExtra/AG_interactions.htm | Fluxo de treino/validação, triagem e modelos restritos; probabilidade binária não auditada |
| siRF | https://arxiv.org/abs/1810.07287 | Resumo e versões; análise secundária, não presumir identidade de duas execuções independentes |
| LSSFind | https://arxiv.org/abs/2102.11800 | Resumo: DWP e recuperação sob hipóteses LSS, não promessa universal |
| RSRF | https://doi.org/10.1016/j.csda.2025.108237 | Resumo localizado; página integral inacessível nesta consulta. Compatibilidade binária não revalidada |

## Divergências corrigidas no uso do inventário

Não se aceita como fato que siRF e iRF do piloto tenham usado sempre a mesma floresta: o código contém ajustes separados. Na nova comparação, extratores só compartilham a régua quando compartilham exatamente o modelo ajustado. Não se aceita que GUIDE deva ser excluído por ser apenas árvore única. RPF atual tem API e padrões distintos dos do piloto e das páginas antigas ainda indexadas. O espelho CRAN de iRF é 2.0.0, enquanto o repositório dos autores auditado é 3.0.0. Essas distinções constam dos registros técnicos.

## Verificações complementares na retomada

- DP-Forests: introdução do texto primário https://arxiv.org/html/1809.08524v1 consultada. A formulação é regressão com ruído normal. Uma possibilidade de extensão não comprova implementação binária disponível. BART e DP-Forests precisam ser desmembrados.
- RIF de Guo e Lin: resumo institucional https://scholar.nycu.edu.tw/en/publications/random-interaction-forest-rif-a-novel-machine-learning-strategy-a/ consultado; código não localizado. Há outro trabalho com sigla RIF sobre priorização de biomarcadores, que não deve ser usado como evidência do mesmo algoritmo.
- GUIDE: links oficiais de manual e binário localizados na página do autor. O manual https://www.stat.wisc.edu/~loh/treeprogs/guide/guideman.pdf apresentou verificação interativa; o binário macOS ARM https://www.stat.wisc.edu/~loh/treeprogs/guide/mac/m1/guide.zip expirou no acesso. Isso limita esta auditoria; não demonstra indisponibilidade permanente do software.
- SNPInterForest: o artigo de Yoshida e Koike (2011), DOI 10.1186/1471-2105-12-469, aponta https://gwas.lifesciencedb.jp/SNPInterForest/index.html. O endereço não ficou acessível nesta consulta; não houve teste de execução.
- Weber et al.: consultadas diretamente as seções “Selection of methods” e “Parameters and software versions”. Elas discutem critérios de inclusão, disponibilidade de software e transparência na estratégia de parâmetros; não prescrevem a lista adotada neste projeto.

Consultas adicionais: `"Dirichlet process forests" classification code`; `"Random Interaction Forest" "code" Guo Lin`; `"SNPInterForest" software download`; `"Guo" "Lin" "Random Interaction Forest" IEEE 2023 software`.
- UFO, seção 4.3: confirmadas 20000 árvores e a configuração harmonizada do RF no artigo. O núcleo aqui compara procedimentos configurados; não isola causalmente o efeito da construção das raízes.
- BART: fonte primária dos autores https://www.rob-mcculloch.org/2026_uml/webpage/BART.pdf e documentação oficial https://search.r-project.org/CRAN/refmans/BART/html/pbart.html localizadas. O suporte binário de BART não foi confundido com o de DP-Forests. BART permanece referência ampliada, sem execução nesta auditoria.
