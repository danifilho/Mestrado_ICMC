"""Etapa 1 (seção 5.3): curvas de detecção top-k, resumo, taxa no modelo "Sem interação" e concordância.
Entradas: resultados/brutos/<etapa>/d*/rep*.csv (R) e rep*_py.csv (Python); referências da Etapa 0 com os mesmos dados de
treino (resultados/brutos/etapa0: Gini, permutação, PPI, JMST; JVIMP de etapa0_rfsrc161, a versão que reproduz Wright).
Rankings: nativo (escore decrescente); régua global com |I| decrescente (principal, convenção da JVIMP), −I decrescente
e I decrescente (sensibilidades). Acaso: P(posto <= k) = k/21 para o par verdadeiro entre 21 pares.
Uso: python3 scripts/05_analisar_etapa1.py [etapa1|piloto1]
"""
import itertools
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import kendalltau

R = Path(__file__).resolve().parents[1]
etapa = sys.argv[1] if len(sys.argv) > 1 else "etapa1"
TAB = R / "resultados" / "tabelas"
TAB.mkdir(parents=True, exist_ok=True)
MOD = {"interaction_only": "Só interação", "modifier_snp1": "SNP modificador", "no_interaction": "Sem interação",
       "redundant": "Redundante", "synergistic": "Sinérgico"}
CEN = ["beta", "beta_effect", "maf_interaction", "maf_effect"]
KS = range(1, 11)

br = R / "resultados" / "brutos" / etapa
D = pd.concat([pd.read_csv(f) for f in br.glob("d*/rep[0-9][0-9][0-9].csv")] +
              [pd.read_csv(f) for f in br.glob("d*/rep[0-9][0-9][0-9]_py.csv")], ignore_index=True)
D["model"] = D.model.astype(str)
reps = D[["desenho", "repeticao"]].drop_duplicates()

# postos do par verdadeiro por (detector, tipo de ranking)
linhas = []
for (det, rk), g in D[D.verdadeiro].groupby(["detector", "ranking"]):
    variantes = [("posto", "nativo")] if rk == "nativo" else [("posto_abs", "|I|"), ("posto_neg", "−I"), ("posto", "I")]
    for col, nome in variantes:
        h = g[CEN + ["model", "desenho", "repeticao"]].copy()
        h["detector"], h["ranking"], h["direcao"], h["posto_verdadeiro"] = det, rk, nome, g[col].values
        linhas.append(h)
# referências da Etapa 0 (mesmos dados de treino; postos já calculados em Wright)
ALG = {"impurity": "gini_W", "permutation": "permutacao_W", "pairwise": "ppi_W", "jmst": "jmst_W"}
e0 = pd.concat([pd.read_csv(f) for f in (R / "resultados" / "brutos" / "etapa0").glob("d*/rep*.csv")])
e0j = pd.concat([pd.read_csv(f) for f in (R / "resultados" / "brutos" / "etapa0_rfsrc161").glob("d*/rep*.csv")])
e0 = pd.concat([e0[(e0.algo != "jvimp") & (e0.mtry == 50)], e0j.assign(algo="jvimp161")])
e0 = e0.merge(reps, left_on=["desenho", "repeticao"], right_on=["desenho", "repeticao"])
for alg, g in e0.groupby("algo"):
    h = g[CEN + ["model", "desenho", "repeticao"]].rename(columns={"maf_interaction": "maf_interaction"}).copy()
    h["detector"] = ALG.get(alg, "jvimp_W"); h["ranking"] = "nativo (Etapa 0)"; h["direcao"] = "Wright"
    h["posto_verdadeiro"] = g["rank"].values
    linhas.append(h)
P = pd.concat(linhas, ignore_index=True)
P["modelo"] = P.model.map(MOD)
P.to_csv(TAB / f"{etapa}_postos_par_verdadeiro.csv.gz", index=False)

curvas = []
for k in KS:
    c = P.assign(top=(P.posto_verdadeiro <= k)).groupby(CEN + ["modelo", "detector", "ranking", "direcao"]).agg(
        deteccao=("top", "mean"), n=("top", "size"), na=("posto_verdadeiro", lambda s: s.isna().sum())).reset_index()
    curvas.append(c.assign(k=k))
C = pd.concat(curvas)
C.to_csv(TAB / f"{etapa}_curvas_deteccao.csv", index=False)
res = C.groupby(CEN + ["modelo", "detector", "ranking", "direcao"]).deteccao.mean().rename("media_curva_k1_10").reset_index()
res["acaso"] = np.mean([k / 21 for k in KS])
res.to_csv(TAB / f"{etapa}_resumo_deteccao.csv", index=False)
geral = res.groupby(["detector", "ranking", "direcao", "modelo"]).media_curva_k1_10.mean().unstack("modelo").round(3)
geral.to_csv(TAB / f"{etapa}_resumo_por_modelo.csv")

# concordância entre detectores na mesma repetição (rankings nativos e régua global por |I|)
conc = []
Dn = D[(D.ranking == "nativo")].assign(chave=lambda d: d.detector + " (nativo)", s=lambda d: d.escore)
Dg = D[(D.ranking == "global_logloss")].assign(chave=lambda d: d.modelo + " (régua, |I|)", s=lambda d: d.escore.abs())
Dg = Dg.drop_duplicates(["desenho", "repeticao", "modelo", "par"])
DD = pd.concat([Dn, Dg])
for (des, rep), g in DD.groupby(["desenho", "repeticao"]):
    M = g.pivot_table(index="par", columns="chave", values="s")
    top3 = {c: set(M[c].sort_values(ascending=False).head(3).index) for c in M.columns}
    for a, b in itertools.combinations(M.columns, 2):
        x, y = M[a], M[b]
        ok = x.notna() & y.notna()
        tau = kendalltau(x[ok], y[ok]).statistic if ok.sum() > 2 and x[ok].nunique() > 1 and y[ok].nunique() > 1 else np.nan
        conc.append(dict(desenho=des, repeticao=rep, a=a, b=b, intersecao_top3=len(top3[a] & top3[b]), kendall_tau=tau))
K = pd.DataFrame(conc)
K.to_csv(TAB / f"{etapa}_concordancia_por_repeticao.csv.gz", index=False)
K.groupby(["a", "b"]).agg(intersecao_top3=("intersecao_top3", "mean"), kendall_tau=("kendall_tau", "mean"), n=("kendall_tau", "size")).round(3).to_csv(
    TAB / f"{etapa}_concordancia_resumo.csv")

# desempenho preditivo dos modelos (contexto)
perf = pd.concat([pd.read_csv(f).assign(desenho=int(f.parent.name[1:])) for f in br.glob("d*/rep*_desempenho*.csv")])
perf.groupby("modelo")[["logloss", "acuracia"]].mean().round(4).to_csv(TAB / f"{etapa}_desempenho_modelos.csv")
print(geral.to_string())
print(perf.groupby("modelo")[["logloss", "acuracia"]].mean().round(4))
