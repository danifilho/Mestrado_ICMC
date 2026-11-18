"""Auditoria dos dados do caso de enhancers do iRF e preparo das partições, reamostragens e permutações.

Entradas: data/raw/ (cópias de iRF_analyses.zip, Zenodo 10.5281/zenodo.1401347, md5 do zip
651290c665d2a3dc4583ea9b026a647f): enhancer.Rdata, irfSuppData1.csv, enhancer.R, README.md.
Compara com os arquivos da comparação anterior (experimentos/comparacao_preditores_v1/data).

Regras (PROTOCOLO.md, seções 2-3 e 7; fixadas antes de qualquer ranking):
- grupos = componentes conexos de sobreposição genômica (mesmo cromossomo, intervalos r6 que se
  tocam), mesmo id e atributos idênticos (mesma regra da comparação anterior);
- partição agrupada e aproximadamente estratificada: StratifiedGroupKFold(5, shuffle, 2026);
  folds 0-2 = treino (~60%), 3 = validação (~20%), 4 = teste (~20%);
- reamostragens de estabilidade: R = 20 subamostras de 80% dos GRUPOS do treino, sem reposição
  (semente 2026 + r); o mesmo conjunto vale para todos os métodos;
- permutações do desfecho no treino: permuta-se o VETOR de rótulos entre grupos de mesmo tamanho
  (preserva a dependência de rótulos dentro de grupos sobrepostos); semente 3026 + p.
"""
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedGroupKFold

RAIZ = Path(__file__).resolve().parents[1]
RAW = RAIZ / "data" / "raw"
OUT = RAIZ / "data" / "processed"
ANT = RAIZ.parent / "comparacao_preditores_v1" / "data"
EXE = json.loads((RAIZ / "configs" / "execucao.json").read_text())


def sha256(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def ler_rdata():
    with tempfile.TemporaryDirectory() as d:
        r = f'''load("{RAW / "enhancer.Rdata"}"); cat(class(X), dim(X), "\\n")
write.csv(data.frame(X, check.names = FALSE), "{d}/X.csv", row.names = FALSE)
write.csv(data.frame(y = Y), "{d}/Y.csv", row.names = FALSE)
write.csv(data.frame(i = train.id), "{d}/tr.csv", row.names = FALSE)
write.csv(data.frame(i = test.id), "{d}/te.csv", row.names = FALSE)
write.csv(varnames.all, "{d}/v.csv", row.names = FALSE)
cat(ls(), "\\n")'''
        o = subprocess.run(["Rscript", "-e", r], capture_output=True, text=True, check=True).stdout
        X = pd.read_csv(f"{d}/X.csv")
        return (X, pd.read_csv(f"{d}/Y.csv").y.to_numpy(), pd.read_csv(f"{d}/tr.csv").i.to_numpy(),
                pd.read_csv(f"{d}/te.csv").i.to_numpy(), pd.read_csv(f"{d}/v.csv"), o)


def grupos(meta, X):
    n = len(meta)
    pai = list(range(n))

    def achar(i):
        while pai[i] != i:
            pai[i] = pai[pai[i]]
            i = pai[i]
        return i

    def unir(i, j):
        a, b = achar(i), achar(j)
        if a != b:
            pai[max(a, b)] = min(a, b)

    mot = {"sobreposicao": 0, "mesmo_id": 0, "atributos_identicos": 0}
    for _, sub in meta.sort_values(["chr", "r6start"]).groupby("chr"):
        fim, ant = -1, None
        for i in sub.index:
            if ant is not None and meta.at[i, "r6start"] <= fim:
                unir(i, ant)
                mot["sobreposicao"] += 1
            fim = max(fim, meta.at[i, "r6stop"])
            ant = i
    for _, sub in meta.groupby("id"):
        for i in sub.index[1:]:
            unir(sub.index[0], i)
            mot["mesmo_id"] += 1
    chave = pd.util.hash_pandas_object(X, index=False)
    for _, sub in pd.Series(range(n)).groupby(chave.values):
        for i in sub.values[1:]:
            unir(sub.values[0], i)
            mot["atributos_identicos"] += 1
    _, g = np.unique([achar(i) for i in range(n)], return_inverse=True)
    return g, mot


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    sup = pd.read_csv(RAW / "irfSuppData1.csv")
    Xr, yr, tr, te, vn, saida_r = ler_rdata()
    feats = list(sup.columns[5:])
    aud = {"objetos_no_Rdata": saida_r.strip().splitlines()[-1]}
    aud["X_Rdata_igual_CSV"] = bool(list(Xr.columns) == feats and np.array_equal(Xr.to_numpy(), sup[feats].to_numpy()))
    aud["Y_Rdata_igual_CSV"] = bool(np.array_equal(yr, sup.positive.to_numpy()))
    Xa = pd.read_csv(ANT / "X.csv.gz")
    aud["X_igual_comparacao_anterior"] = bool(np.array_equal(Xa.to_numpy(), Xr.to_numpy()) and list(Xa.columns) == feats)
    aud["Y_igual_comparacao_anterior"] = bool(np.array_equal(pd.read_csv(ANT / "Y.csv").y.to_numpy(), yr))
    aud["treino_oficial_igual"] = bool(np.array_equal(np.sort(tr), pd.read_csv(ANT / "train_id_oficial.csv").linha.to_numpy()))
    aud["teste_oficial_igual"] = bool(np.array_equal(np.sort(te), pd.read_csv(ANT / "test_id_oficial.csv").linha.to_numpy()))
    aud["varnames_igual"] = bool(vn.equals(pd.read_csv(ANT / "varnames_all.csv")))
    aud["varnames_ordem_igual_colunas"] = bool(list(vn.Predictor) == feats)
    n = len(yr)
    meta = sup[["id", "chr", "r6start", "r6stop"]].copy()
    aud.update({"n": int(n), "p": len(feats), "positivos": int(yr.sum()), "ausentes": int(Xr.isna().sum().sum()),
                "treino_oficial": int(len(tr)), "teste_oficial": int(len(te)),
                "positivos_treino_oficial": int(yr[tr - 1].sum()), "positivos_teste_oficial": int(yr[te - 1].sum()),
                "cromossomos": sorted(meta.chr.unique().tolist()),
                "comprimento_regioes": {k: float(v) for k, v in (meta.r6stop - meta.r6start + 1).describe().items()},
                "prefixos_id": meta.id.str.extract(r"^([A-Za-z]+)")[0].value_counts().to_dict()})
    X = Xr
    g, mot = grupos(meta, X)
    lado_of = np.where(np.isin(np.arange(1, n + 1), tr), "treino", "teste")
    gs = pd.Series(lado_of).groupby(g).nunique()
    aud["grupos"] = {"n": int(g.max() + 1), "unioes": mot, "tamanho_max": int(np.bincount(g).max()),
                     "grupos_divididos_na_particao_oficial": int((gs > 1).sum()),
                     "linhas_em_grupos_divididos_oficial": int(np.isin(g, gs[gs > 1].index).sum())}

    # partição agrupada 60/20/20
    sgk = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=EXE["semente_particao"])
    fold = np.empty(n, int)
    for k, (_, idx) in enumerate(sgk.split(np.zeros(n), yr, g)):
        fold[idx] = k
    lado = np.where(fold <= 2, "treino", np.where(fold == 3, "validacao", "teste"))
    part = pd.DataFrame({"linha": np.arange(1, n + 1), "id": meta.id, "chr": meta.chr, "r6start": meta.r6start,
                         "r6stop": meta.r6stop, "y": yr, "grupo": g, "lado": lado, "lado_oficial": lado_of})
    assert part.groupby("grupo").lado.nunique().max() == 1
    aud["particao_agrupada"] = {s: {"n": int((lado == s).sum()), "positivos": int(yr[lado == s].sum()),
                                    "prop": float(yr[lado == s].mean()), "grupos": int(part[lado == s].grupo.nunique())}
                                for s in ("treino", "validacao", "teste")}
    part.to_csv(OUT / "particao.csv", index=False)

    # reamostragens (subamostras de grupos do treino)
    it = np.flatnonzero(lado == "treino")
    gtr = np.unique(g[it])
    R = EXE["reamostragens"]["n"]
    sub = {}
    for r in range(1, R + 1):
        rng = np.random.default_rng(EXE["reamostragens"]["semente_base"] + r)
        esc = rng.choice(gtr, size=int(round(EXE["reamostragens"]["fracao_grupos"] * len(gtr))), replace=False)
        sub[f"r{r:02d}"] = np.isin(g[it], esc).astype(int)
    S = pd.DataFrame(sub)
    S.insert(0, "linha", it + 1)
    S.to_csv(OUT / "reamostragens_treino.csv", index=False)

    # permutações por grupo (vetores de rótulos trocados entre grupos de mesmo tamanho)
    ytr, gt = yr[it], g[it]
    perm = {}
    for p in range(1, EXE["permutacoes"]["n"] + 1):
        rng = np.random.default_rng(EXE["permutacoes"]["semente_base"] + p)
        ynew = ytr.copy()
        grp = pd.Series(np.arange(len(it))).groupby(gt).apply(list)
        tam = grp.map(len)
        for t, gg in grp.groupby(tam):
            lst = list(gg.values)
            ordem = rng.permutation(len(lst))
            for a, b in zip(lst, [lst[j] for j in ordem]):
                ynew[a] = ytr[b]  # a e b têm o mesmo tamanho; linhas na ordem genômica de cada grupo
        perm[f"p{p:02d}"] = ynew
    P = pd.DataFrame(perm)
    P.insert(0, "linha", it + 1)
    P.to_csv(OUT / "permutacoes_treino.csv", index=False)
    aud["permutacoes"] = {"n": EXE["permutacoes"]["n"], "positivos_preservados": bool((P.iloc[:, 1:].sum() == ytr.sum()).all()),
                          "grupos_por_tamanho": {int(k): int(v) for k, v in pd.Series(np.bincount(gt)[np.unique(gt)]).value_counts().sort_index().items()}}

    # matrizes por lado
    for s in ("treino", "validacao", "teste"):
        m = lado == s
        X[m].to_csv(OUT / f"X_{s}.csv", index=False)
        pd.DataFrame({"y": yr[m]}).to_csv(OUT / f"y_{s}.csv", index=False)
        part[m][["linha", "id", "grupo"]].to_csv(OUT / f"ids_{s}.csv", index=False)
    # partição oficial (análise secundária de reprodução)
    for s in ("treino", "teste"):
        m = lado_of == s
        pd.DataFrame({"linha": np.flatnonzero(m) + 1}).to_csv(OUT / f"oficial_{s}_linhas.csv", index=False)

    vn.to_csv(OUT / "varnames.csv", index=False)
    aud["hashes"] = {**{f"raw/{p.name}": sha256(p) for p in sorted(RAW.glob("*"))},
                     **{f"processed/{p.name}": sha256(p) for p in sorted(OUT.glob("*"))}}
    (RAIZ / "resultados" / "auditoria" / "auditoria_dados.json").write_text(json.dumps(aud, indent=1, ensure_ascii=False))
    print(json.dumps({k: v for k, v in aud.items() if k != "hashes"}, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    sys.exit(main())
