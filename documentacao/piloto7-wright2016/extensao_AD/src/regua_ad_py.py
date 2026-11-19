"""Extensão A–D do Piloto 7: EBM (referência adicional) em Python, com a régua comum pós-ajuste por permutação.
Mesmos dados (../resultados/dados_etapa1) e MESMOS índices de permutação dos modelos em R (extensao_AD/resultados/permutacoes).
EBM: interpret 0.7.8, ExplainableBoostingClassifier com os padrões do pacote, n_jobs = 1; random_state = (semente_dados +
1000003·s) mod 2^31 (s = 0 reproduz o histórico de src/etapa1_py.py). Nativo: term_importances do termo do par (0 se ausente).
Saídas no mesmo formato de src/regua_ad.R (sufixo _py). No modo validar, também grava a régua SEM lote em 3 conjuntos.
Uso: python extensao_AD/src/regua_ad_py.py tarefa.json   (P7_RAIZ)
"""
import itertools
import json
import os
import platform
import sys
import time
import hashlib

import numpy as np
import pandas as pd
import interpret
import sklearn
from interpret.glassbox import ExplainableBoostingClassifier

T = json.load(open(sys.argv[1]))
RAIZ = os.environ["P7_RAIZ"]
EXT = os.path.join(RAIZ, "extensao_AD")
V7 = ["interactionSNP1", "interactionSNP2"] + [f"effectSNP{i}" for i in range(1, 6)]
PARES = [f"{a}:{b}" for a, b in itertools.combinations(V7, 2)]
CONJ = V7 + PARES
s = int(T["semente_ajuste"]); OFF = 1000003 * s
validar = bool(T.get("validar", False))


def ll_vec(y, p):
    p = np.clip(p, 1e-15, 1 - 1e-15)
    return -(y * np.log(p) + (1 - y) * np.log(1 - p))


def ac_vec(y, p):
    return ((p > 0.5) == (y == 1)).astype(float)


def perdas(prever, Xte, yte, P, conjuntos=CONJ):
    n, Q = P.shape
    b = prever(Xte)
    out = [dict(conjunto="(original)", perm=0, logloss=ll_vec(yte, b).mean(), acuracia=ac_vec(yte, b).mean())]
    Xv = Xte.to_numpy(); idx = P.T.reshape(-1) - 1  # bloco q = linhas q·n .. (q+1)·n − 1, como o empilhamento do R
    Xb = np.tile(Xv, (Q, 1)); yb = np.tile(yte, Q)
    for cj in conjuntos:
        cols = [Xte.columns.get_loc(c) for c in cj.split(":")]
        Xp = Xb.copy(); Xp[:, cols] = Xv[idx][:, cols]
        p = prever(pd.DataFrame(Xp, columns=Xte.columns))
        L = ll_vec(yb, p).reshape(Q, n).mean(1); A = ac_vec(yb, p).reshape(Q, n).mean(1)
        out += [dict(conjunto=cj, perm=q + 1, logloss=L[q], acuracia=A[q]) for q in range(Q)]
    return pd.DataFrame(out), b


def perdas_sem_lote(prever, Xte, yte, P, conjuntos):
    out = []
    for cj in conjuntos:
        cols = cj.split(":")
        for q in range(P.shape[1]):
            Xp = Xte.copy(); Xp[cols] = Xte[cols].to_numpy()[P[:, q] - 1]
            p = prever(Xp)
            out.append(dict(conjunto=cj, perm=q + 1, logloss=ll_vec(yte, p).mean(), acuracia=ac_vec(yte, p).mean()))
    return pd.DataFrame(out)


saida = os.path.join(EXT, T["saida"]); os.makedirs(saida, exist_ok=True)
ddir = os.path.join(RAIZ, "resultados", "dados_etapa1", f"d{T['desenho']:02d}")
pdir = os.path.join(EXT, "resultados", "permutacoes", f"d{T['desenho']:02d}")
for r in T["repeticoes"]:
    pre = os.path.join(saida, f"rep{r:03d}_s{s}")
    if os.path.exists(pre + "_meta_py.json"):
        continue
    sd = T["semente_base"] + 1000 * T["desenho"] + r
    tr = pd.read_csv(os.path.join(ddir, f"rep{r:03d}_treino.csv.gz")); te = pd.read_csv(os.path.join(ddir, f"rep{r:03d}_teste.csv.gz"))
    Xtr, ytr, Xte, yte = tr.drop(columns="pheno"), tr.pheno.to_numpy(), te.drop(columns="pheno"), te.pheno.to_numpy()
    arqP = os.path.join(pdir, f"rep{r:03d}.csv.gz")
    P = pd.read_csv(arqP).to_numpy().astype(np.int64)
    assert P.shape[0] == len(Xte) and all((np.sort(P[:, q]) == np.arange(1, len(Xte) + 1)).all() for q in range(P.shape[1]))
    ii, qq = np.meshgrid(np.arange(1, P.shape[0] + 1), np.arange(1, P.shape[1] + 1), indexing="ij")
    tempos = {}
    t0 = time.time()
    ebm = ExplainableBoostingClassifier(random_state=(sd + OFF) % (2 ** 31), n_jobs=1)
    ebm.fit(Xtr, ytr); tempos["ebm"] = time.time() - t0
    assert list(ebm.classes_) == [0, 1]  # predict_proba[:, 1] = P(caso)
    imp = dict(zip(ebm.term_names_, ebm.term_importances()))
    nat = pd.DataFrame([dict(detector="ebm", par=pr, escore=float(imp.get(f"{pr.split(':')[0]} & {pr.split(':')[1]}",
                                                                          imp.get(f"{pr.split(':')[1]} & {pr.split(':')[0]}", 0.0))))
                        for pr in PARES])
    prever = lambda X: ebm.predict_proba(X)[:, 1]  # noqa: E731
    t0 = time.time(); tab, b = perdas(prever, Xte, yte, P); tempos["regua_ebm"] = time.time() - t0
    tab["modelo"] = "ebm"
    tab.to_csv(pre + "_perdas_py.csv.gz", index=False)
    pd.DataFrame(dict(ebm=b)).to_csv(pre + "_previsoes_py.csv.gz", index=False)
    nat.to_csv(pre + "_nativos_py.csv", index=False)
    if validar:
        t0 = time.time()
        sl = perdas_sem_lote(prever, Xte, yte, P, ["interactionSNP1", "effectSNP1", PARES[0]])
        c = sl.merge(tab, on=["conjunto", "perm"], suffixes=("_sem_lote", "_lote"))
        pd.DataFrame([dict(max_dif_ll=float((c.logloss_sem_lote - c.logloss_lote).abs().max()),
                           max_dif_ac=float((c.acuracia_sem_lote - c.acuracia_lote).abs().max()), n=len(c))]).to_csv(
            pre + "_validar_lote_vs_sem_lote_py.csv", index=False)
        tempos["validar_sem_lote"] = time.time() - t0
    meta = dict(desenho=T["desenho"], repeticao=r, semente_dados=sd, semente_ajuste=s, deslocamento_semente=OFF, mtry=T["mtry"],
                modelos=["ebm"], n_treino=len(Xtr), n_teste=len(Xte), prevalencia_treino=float(ytr.mean()), prevalencia_teste=float(yte.mean()),
                n_pares_ebm_selecionados=int(sum(" & " in t for t in ebm.term_names_)),
                arquivo_perm=os.path.relpath(arqP, EXT), sha256_perm=hashlib.sha256(open(arqP, "rb").read()).hexdigest(),
                digital_perm=int((P * ii * qq).sum()), tempos={k: round(v, 2) for k, v in tempos.items()},
                versoes=dict(python=platform.python_version(), interpret=interpret.__version__, numpy=np.__version__, pandas=pd.__version__,
                             sklearn=sklearn.__version__),
                no=platform.node(), tarefa_slurm=os.environ.get("SLURM_JOB_ID", ""), quando=time.strftime("%Y-%m-%dT%H:%M:%S%z"))
    json.dump(meta, open(pre + "_meta_py.json", "w"), indent=1)
print("ok")
