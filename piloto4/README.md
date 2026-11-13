# Piloto 4 — Recuperação, estabilidade e previsão

Este pacote testa duas coisas diferentes:

1. **Árvore de componentes do piloto 3:** agrupa componentes da fANOVA segundo transformações globais compartilhadas. Avaliamos estabilidade da topologia.
2. **Árvores de expressão:** calculam uma resposta combinando variáveis por somas e curvas locais. Avaliamos recuperação e previsão. São um teste complementar da hipótese, não a implementação definitiva de uma árvore cujas folhas são interações.

Leia `RELATORIO_PILOTO_4.md` para resultados e limitações.

## Reproduzir

Python 3, numpy, scipy, pandas, scikit-learn e matplotlib. Após instalar dependências, a execução não usa internet.

```bash
python piloto4.py
python auditar_assinaturas.py
python analisar.py
python sensibilidade_otimizacao.py
```

`python piloto4.py --quick` faz uma execução curta para verificar funcionamento, mas **sobrescreve** os mesmos resultados. Rode em uma cópia do pacote se quiser preservar a execução completa.

- `piloto4.py`: catálogo, fórmulas, gradientes, ajuste, seleção por validação e teste.
- `piloto3_legado.py`: implementação anterior preservada como módulo; não é necessário executá-la.
- `auditar_assinaturas.py`: usa as assinaturas anteriores e verifica estabilidade e equivalência entre árvores de somas.
- `analisar.py`: agrega e cria figuras sem alterar critérios.
- `resultados/protocolo.json`: escolhas numéricas fixadas antes da execução principal.
- `resultados/geradores.json`: parâmetros exatos das funções geradoras.
- `resultados/ajustes.csv`: resultado de cada candidato, incluindo convergência.
- `resultados/previsao_resumo.csv`: seleções por condição e erros nas células retidas.
- `resultados/diferencas_bootstrap_geradores.csv`: diferenças pareadas, reamostrando geradores independentes.
- `resultados/estabilidade_expressoes.csv`: repetibilidade das estruturas de expressão selecionadas.
- `resultados/estabilidade_assinaturas.csv`: estabilidade das árvores de componentes.

Nenhuma estrutura é identificada como um mecanismo biológico real. A seleção de modelo é restrita ao catálogo e não constitui prova de inexistência de outra explicação. A regra de um erro padrão é uma heurística, não um intervalo de confiança sobre estruturas.

## Figuras explicativas (`figuras/`)

Vieram de um pacote separado (`Figuras_piloto4.zip`):

- `figuras/metodologia_piloto4.png` / `.svg`: mapa da metodologia dos dois testes. Gerado por `figuras/gerar_metodologia.py`.
- `figuras/recuperacao_estabilidade_explicada.png`: versão comentada de `resultados/recuperacao_estabilidade.png`. Gerado por `figuras/refazer_recuperacao.py`, que lê `resultados/` (caminho ajustado para esta estrutura de pastas).

```bash
python figuras/gerar_metodologia.py
python figuras/refazer_recuperacao.py
```
