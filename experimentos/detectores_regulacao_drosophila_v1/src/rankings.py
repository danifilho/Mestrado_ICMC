"""Construção dos rankings de pares de fatores (regras congeladas no PROTOCOLO.md, §6)."""
import json
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
FAT = json.loads((RAIZ / "configs" / "fatores.json").read_text())["fatores"]
COL2TF = {c: f["tf"] for f in FAT for c in f["colunas"]}
TFS = sorted(f["tf"] for f in FAT)
PARES = [tuple(p) for p in combinations(TFS, 2)]
VN = pd.read_csv(RAIZ / "data" / "processed" / "varnames.csv")
GRP2TF = {}
for c, g in zip(VN.Predictor, VN.Predictor_collapsed):
    if c in COL2TF:
        GRP2TF[g] = COL2TF[c]
GRUPOS = sorted(set(VN.Predictor_collapsed), key=len, reverse=True)
COLUNAS = set(VN.Predictor)
LISTAS_DET = ["if_quant", "if_qual", "irf"]
LISTAS_CTRL = ["ctrl_importancia", "ctrl_correlacao"]
INDICE_LISTA = {n: i for i, n in enumerate(LISTAS_DET + LISTAS_CTRL + ["irf_projecao"])}


def ordenar(esc, nome, rotulo):
    """esc: dict par -> escore (só pares com escore). Ordena por escore decrescente; empates por sorteio
    com semente fixa (2026, índice da lista, hash estável do rótulo). Devolve DataFrame."""
    if not esc:
        return pd.DataFrame(columns=["tf_1", "tf_2", "escore", "posicao", "grupo_empate", "tamanho_empate"])
    pares = sorted(esc)
    rng = np.random.default_rng([2026, INDICE_LISTA[nome], sum(map(ord, rotulo))])
    chave = rng.permutation(len(pares))
    D = pd.DataFrame({"tf_1": [p[0] for p in pares], "tf_2": [p[1] for p in pares], "escore": [esc[p] for p in pares], "_r": chave})
    D = D.sort_values(["escore", "_r"], ascending=[False, True]).drop(columns="_r").reset_index(drop=True)
    D["posicao"] = np.arange(1, len(D) + 1)
    D["grupo_empate"] = D.escore.rank(method="dense", ascending=False).astype(int)
    D["tamanho_empate"] = D.groupby("grupo_empate").escore.transform("size")
    return D


def _pares_de_colunas(rotulo):
    toks = [t for t in str(rotulo).replace(",", " ").split() if t in COLUNAS]
    return toks if len(toks) == 2 else None


def ranking_if(d, tipo, rotulo):
    p = Path(d) / "nativo" / f"eim_{tipo}.csv"
    if not p.exists():
        return None, None
    T = pd.read_csv(p)
    esc, outros = {}, []
    for r, v in zip(T.rotulo, T.valor):
        cc = _pares_de_colunas(r)
        if cc is None or not np.isfinite(v):
            continue
        a, b = COL2TF.get(cc[0]), COL2TF.get(cc[1])
        if a and b and a != b:
            k = tuple(sorted((a, b)))
            esc[k] = max(esc.get(k, -np.inf), float(v))
        elif not (a and b):
            outros.append((cc[0], cc[1], float(v)))
    O = pd.DataFrame(outros, columns=["coluna_1", "coluna_2", "eim"]).sort_values("eim", ascending=False)
    return ordenar(esc, "if_quant" if tipo == "quant" else "if_qual", rotulo), O


def _grupos_de(nome):
    """Divide 'wt_ZLD_bcd_hb' nos nomes de grupos conhecidos (alguns contêm '_')."""
    toks, out, i = nome.split("_"), [], 0
    while i < len(toks):
        for j in range(len(toks), i, -1):
            cand = "_".join(toks[i:j])
            if cand in set(GRUPOS):
                out.append(cand)
                i = j
                break
        else:
            return None
    return out


def ranking_irf(d, rotulo):
    p = Path(d) / "nativo" / "irf_interacoes.csv"
    if not p.exists():
        return None, None, None
    T = pd.read_csv(p)
    esc, proj, linhas = {}, {}, []
    for nome, v in zip(T.interacao, T.estabilidade):
        g = _grupos_de(nome)
        if g is None:
            continue
        tfs = [GRP2TF.get(x) for x in g]
        linhas.append({"conjunto": nome, "tamanho": len(g), "estabilidade": v, "so_fatores": all(tfs),
                       "fatores": "_".join(sorted({t for t in tfs if t}))})
        if all(tfs):
            st = sorted(set(tfs))
            if len(g) == 2 and len(st) == 2:
                k = tuple(st)
                esc[k] = max(esc.get(k, -np.inf), float(v))
            for a, b in combinations(st, 2):
                proj[(a, b)] = max(proj.get((a, b), -np.inf), float(v))
    return ordenar(esc, "irf", rotulo), ordenar(proj, "irf_projecao", rotulo), pd.DataFrame(linhas)


def ranking_importancia(d, rotulo, semente_postos):
    p = Path(d) / "nativo" / "rf_importancia_permutacao_validacao.csv"
    if not p.exists():
        return None
    T = pd.read_csv(p)
    T["tf"] = T.atributo.map(COL2TF)
    imp = T.dropna(subset=["tf"]).groupby("tf").queda_ap.max()
    rng = np.random.default_rng([semente_postos, sum(map(ord, rotulo))])
    o = pd.DataFrame({"tf": imp.index, "imp": imp.values, "_r": rng.permutation(len(imp))}).sort_values(["imp", "_r"], ascending=[False, True])
    posto = dict(zip(o.tf, np.arange(1, len(o) + 1)))
    return ordenar({(a, b): -(posto[a] + posto[b]) for a, b in PARES}, "ctrl_importancia", rotulo)


def ranking_correlacao(Xtr):
    from scipy.stats import spearmanr
    cols = [c for c in Xtr.columns if c in COL2TF]
    rho = spearmanr(Xtr[cols].to_numpy()).statistic
    esc = {}
    for i, j in combinations(range(len(cols)), 2):
        a, b = COL2TF[cols[i]], COL2TF[cols[j]]
        if a != b:
            k = tuple(sorted((a, b)))
            esc[k] = max(esc.get(k, -np.inf), abs(rho[i, j]))
    return ordenar(esc, "ctrl_correlacao", "treino")


def topk(R, k):
    if R is None or len(R) < k:
        return None
    return [tuple(x) for x in R[["tf_1", "tf_2"]].iloc[:k].to_numpy()]


def resolucoes_empate(R, k, n, semente):
    """n listas top-k alternativas, re-sorteando a ordem dentro dos grupos de empate."""
    if R is None or len(R) < k:
        return []
    rng = np.random.default_rng(semente)
    out = []
    g = R.grupo_empate.to_numpy()
    for _ in range(n):
        o = np.lexsort((rng.random(len(R)), g))
        out.append([tuple(x) for x in R[["tf_1", "tf_2"]].to_numpy()[o][:k]])
    return out


def grau_preservado(lista, n, semente, passos=None):
    """n listas aleatórias com a mesma frequência de participação de cada fator (trocas duplas de arestas
    no grafo completo dos 23 fatores; sem laços nem pares repetidos). Cadeia de Markov a partir da lista
    observada, com 'passos' trocas aceitas entre amostras."""
    rng = np.random.default_rng(semente)
    E = [tuple(sorted(e)) for e in lista]
    S = set(E)
    passos = passos or 10 * len(E)
    out = []
    aceitas_total = 0
    for it in range(n):
        ac = 0
        tent = 0
        while ac < passos and tent < 50 * passos:
            tent += 1
            i, j = rng.choice(len(E), 2, replace=False)
            (a, b), (c, d) = E[i], E[j]
            if rng.random() < 0.5:
                c, d = d, c
            e1, e2 = tuple(sorted((a, d))), tuple(sorted((c, b)))
            if a == d or c == b or e1 == e2 or e1 in S or e2 in S:
                continue
            S -= {E[i], E[j]}
            E[i], E[j] = e1, e2
            S |= {e1, e2}
            ac += 1
        aceitas_total += ac
        out.append(list(E))
        if it == 0 and ac == 0:
            # nenhuma troca possível: a sequência de graus só admite a lista observada (p.ex. uma estrela)
            return [list(E)] * n, 0.0
    return out, aceitas_total / max(1, n)
