"""Auditoria reproduzível da análise S1, publicada em 18/11/2026.
Recalcula rankings, Jaccard e AP/IC dos arquivos dos ajustes. Não treina modelos,
não consulta literatura nem altera snapshots. Executar da pasta do estudo.
"""
from pathlib import Path
from itertools import combinations
import sys
import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score
R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R / 'src'))
import rankings as rk
B = R / 'resultados/brutos/principal'
D = R / 'data/processed'
M = R / 'resultados/metricas'
X = pd.read_csv(D / 'X_treino.csv')
SUB = pd.read_csv(D / 'reamostragens_treino.csv')
seeds = [f'completo_s{s}' for s in [2026, 2027, 2028]]
subs = [f'r{i:02d}_s2026' for i in range(1, 21)]
names = ['if_quant', 'if_qual', 'irf', 'ctrl_importancia', 'ctrl_correlacao']
rankings = {}
for rot in seeds + subs:
    rankings['if_quant', rot] = rk.ranking_if(B / f'if_{rot}', 'quant', rot)[0]
    rankings['if_qual', rot] = rk.ranking_if(B / f'if_{rot}', 'qual', rot)[0]
    rankings['irf', rot] = rk.ranking_irf(B / f'irf_{rot}', rot)[0]
    rankings['ctrl_importancia', rot] = rk.ranking_importancia(B / f'rf_{rot}', rot, 2026)
    x = X if rot in seeds else X[SUB[rot[:3]].to_numpy() == 1].reset_index(drop=True)
    rankings['ctrl_correlacao', rot] = rk.ranking_correlacao(x)
    for name in names:
        old = pd.read_csv(R / 'resultados/rankings' / f'{name}__{rot}.csv')
        new = rankings[name, rot]
        pd.testing.assert_frame_equal(new.reset_index(drop=True), old[new.columns], check_dtype=False, rtol=1e-10, atol=1e-12)
print('115 rankings conferidos com as saídas nativas dos ajustes.')
def top(name, rot):
    return set(map(tuple, rankings[name, rot][['tf_1', 'tf_2']].head(10).to_numpy()))
def jaccard(a, b):
    assert len(a) == len(b) == 10
    return len(a & b) / len(a | b)
E = pd.read_csv(M / 'estabilidade.csv').query('k == 10')
C = pd.read_csv(M / 'concordancia.csv').query('k == 10')
for name in names:
    for fonte, rots in [('reamostragens (dados)', subs), ('sementes (algoritmo)', seeds)]:
        vals = [jaccard(top(name, a), top(name, b)) for a, b in combinations(rots, 2)]
        row = E[(E.lista == name) & (E.fonte == fonte)].iloc[0]
        np.testing.assert_allclose([np.mean(vals), min(vals), max(vals)], row[['jaccard_media', 'jaccard_min', 'jaccard_max']].to_numpy(dtype=float), atol=1e-12)
for a, b in combinations(names, 2):
    row = C[((C.lista_1 == a) & (C.lista_2 == b)) | ((C.lista_1 == b) & (C.lista_2 == a))].iloc[0]
    value = np.mean([jaccard(top(a, rot), top(b, rot)) for rot in subs])
    np.testing.assert_allclose(value, row.jaccard_mesma_reamostragem_media, atol=1e-12)
print('Jaccard@10: médias, extremos e concordâncias conferidos.')
y = pd.read_csv(D / 'y_teste.csv').y.to_numpy()
g = pd.read_csv(D / 'ids_teste.csv').grupo.to_numpy()
P = {(m, s): pd.read_csv(B / f'{m}_completo_s{s}' / 'pred_teste.csv').previsao.to_numpy() for m in ['if', 'irf', 'rf'] for s in [2026, 2027, 2028]}
PV = pd.read_csv(M / 'predicao.csv')
for (m, s), p in P.items():
    old = PV[(PV.metodo == m) & (PV.semente.astype(str) == str(s))].AP.iloc[0]
    np.testing.assert_allclose(average_precision_score(y, p), old, atol=1e-12)
rng = np.random.default_rng(2026)
ug = np.unique(g)
idx = {v: np.flatnonzero(g == v) for v in ug}
boots = [np.concatenate([idx[v] for v in rng.choice(ug, len(ug))]) for _ in range(2000)]
DI = pd.read_csv(M / 'predicao_diferencas.csv').query('metrica == "AP"')
for m in ['if', 'irf']:
    def diff(b):
        return np.mean([average_precision_score(y[b], P[m, s][b]) - average_precision_score(y[b], P['rf', s][b]) for s in [2026, 2027, 2028]])
    vals = [diff(b) for b in boots if y[b].sum() > 0]
    result = [diff(np.arange(len(y))), *np.quantile(vals, [0.025, 0.975])]
    old = DI[DI.comparacao == f'{m} − rf'].iloc[0]
    np.testing.assert_allclose(result, old[['diferenca_media_sementes', 'ic95_inf', 'ic95_sup']].to_numpy(dtype=float), atol=1e-12)
print('AP por semente e os dois IC95% pareados (2.000 grupos bootstrap) conferidos.')
