# Reprodução e rastreabilidade

## Origem

Relatórios, scripts, tabelas e figuras foram copiados da pasta local Mestrado_ICMC/experimentos. As matrizes `piloto3/resultados/assinaturas.npz` e `respostas.npz`, ausentes dessa pasta, foram recuperadas do pacote original Piloto_3_assinaturas.zip. O conteúdo experimental foi preservado. As páginas de índice e catálogo são novas.

A leitura da conversa retornou apenas cinco turnos recentes, sem cursor para mensagens anteriores. Os arquivos locais completos complementam esse recorte, especialmente para o piloto 3. Não se afirma que todo o histórico da conversa tenha sido exportado.

## Ambiente e execução

O ambiente original registrado no piloto 4 foi Python 3.12.14, numpy 2.3.5, scipy 1.17.0, pandas 2.2.3, scikit-learn 1.8.0 e matplotlib 3.10.8. Não há arquivo independente de versões do piloto 3; não atribuir automaticamente a ele o ambiente do piloto 4.

Execute a partir de uma cópia de trabalho, pois os scripts sobrescrevem os resultados:

```bash
cd piloto3
python experimento.py
cd ../piloto4
python piloto4.py
python auditar_assinaturas.py
python analisar.py
python sensibilidade_otimizacao.py
python figuras/gerar_metodologia.py
python figuras/refazer_recuperacao.py
```

Instale numpy, scipy, pandas, scikit-learn e matplotlib antes de executar. Consulte os READMEs dos pilotos para detalhes. A opção `--quick` do piloto 4 usa o mesmo destino de resultados: não executar sobre a evidência preservada.

## Verificação desta consolidação

Foram verificados sintaxe dos scripts Python sem executá-los, leitura dos arquivos JSON e contagens dos CSVs: 12.768 ajustes, 672 condições principais, 432 tabelas de estabilidade e 96 ajustes posteriores. Os experimentos não foram reexecutados, e essa conferência não certifica todas as estatísticas relatadas.

O arquivo MANIFEST.sha256 permite verificar integridade dos artefatos. Relatórios e tabelas originais permanecem a referência para resultados.

## Publicação

Destino: [danifilho/Mestrado_ICMC](https://github.com/danifilho/Mestrado_ICMC), privado.

A tentativa de ativar a Wiki nativa retornou `has_wiki=false`. Por isso estas páginas são mantidas na pasta `wiki/`, com navegação Markdown. A [documentação do GitHub](https://docs.github.com/en/communities/documenting-your-project-with-wikis/about-wikis) informa que Wikis privadas dependem de plano compatível. A causa específica da restrição na conta não foi informada pela API.

As páginas podem ser migradas para o repositório separado `.wiki.git` quando a Wiki nativa estiver disponível. Nenhuma alteração de plano ou de privacidade foi feita.
