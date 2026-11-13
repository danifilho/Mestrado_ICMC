# Piloto 3: assinaturas de interações

Leia primeiro `RELATORIO_PILOTO_3.md`.

Para reproduzir:

```bash
python -m pip install numpy scipy pandas scikit-learn matplotlib
python experimento.py
```

Sementes fixas. A execução sobrescreve resultados locais. Não precisa de rede após instalar dependências.

- `experimento.py`: geração, verificações, fANOVA, árvores, classificação e figuras.
- `resultados/desempenho.csv`: comparação completa.
- `resultados/diferencas_pareadas.csv`: diferenças com bootstrap.
- `resultados/arvores.png`: árvores de cinco exemplos.
- `resultados/assinatura_3d.png`: projeção visual, não usada para classificar.
- `resultados/protocolo.json`: configuração.
- `resultados/datasets.csv`: identificadores e sementes para regenerar cada função. Parâmetros adicionais são recuperados pela mesma semente no código.
- `resultados/respostas.npz`, `assinaturas.npz`: respostas e representações numéricas.

Resultados exploratórios. Não são uma validação de mecanismos biológicos ou comparação com iRF. A árvore não venceu o perfil de transformações sem árvore.
