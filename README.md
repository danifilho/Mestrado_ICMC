# Mestrado_ICMC

Documentação e arquivos dos pilotos 3 e 4 discutidos em **Análise crítica de interações**. A pasta `wiki/` é o índice das discussões do projeto; este repositório preserva códigos, protocolos, resultados e figuras.

## Leitura

- [Índice da documentação](wiki/Home.md)
- [Piloto 3 — relatório completo](piloto3/RELATORIO_PILOTO_3.md)
- [Piloto 4 — relatório completo](piloto4/RELATORIO_PILOTO_4.md)
- [Catálogo de testes e evidências](wiki/Catalogo-de-testes.md)
- [Reprodução e rastreabilidade](wiki/Reproducao-e-rastreabilidade.md)

O piloto 3 avalia **classificação de famílias de funções** a partir de assinaturas. O piloto 4 avalia **recuperação de estruturas, previsão de respostas e estabilidade**. A árvore de componentes do piloto 3 e a árvore de expressão do piloto 4 são objetos diferentes.

Os resultados são exploratórios: o perfil sem árvore superou a assinatura da árvore no piloto 3; composições apropriadas ajudaram a prever no piloto 4, mas a topologia da árvore de componentes permaneceu instável. Não houve validação biológica.

## Organização

- `piloto3/`: código, relatório, logs, figuras, tabelas e matrizes originais.
- `piloto4/`: execução principal, auditoria, análise posterior de otimização e figuras.
- `wiki/`: páginas Markdown navegáveis; a Wiki nativa não pôde ser habilitada.
- `MANIFEST.sha256`: integridade dos arquivos deste pacote.

Este pacote consolida artefatos existentes; não representa uma nova execução dos experimentos. Consulte a rastreabilidade para limites de verificação.
