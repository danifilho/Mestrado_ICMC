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

Destino: [danifilho/Mestrado_ICMC](https://github.com/danifilho/Mestrado_ICMC).

O repositório foi criado privado. O usuário alterou sua visibilidade para público para habilitar a Wiki nativa. Os artefatos experimentais estão no repositório principal; a documentação é mantida também na [Wiki](https://github.com/danifilho/Mestrado_ICMC/wiki).

A pasta `wiki/` preserva uma cópia navegável das páginas. A Wiki nativa usa um repositório Git separado, `.wiki.git`. Futuras alterações devem manter ambas as cópias consistentes.
