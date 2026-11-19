"""Etapa 1, detectores em Python (seção 5.1): NID e EBM, sobre os mesmos dados gravados por src/etapa1.R.
- NID (Tsang, Cheng & Liu 2018), código original (GitHub mtsang/neural-interaction-detection, commit ae974e1):
  MLP [256, 128, 64] (arquitetura padrão de detect_interactions), L1 = 1e-4, Adam lr 0,01, até 100 épocas com parada
  antecipada (paciência 5) em 20 % do treino. ADAPTAÇÃO registrada: perda BCE com logit (desfecho binário; o original usa
  MSE) e X padronizado com média e desvio do treino. Escore nativo: interpret_pairwise_interactions (pesos), 21 pares.
- EBM (GA²M): interpret 0.7.8, ExplainableBoostingClassifier com os padrões do pacote; escore nativo = importância
  (term_importances) do termo do par, 0 se o par não foi selecionado.
- Régua global: a mesma de src/etapa1.R (30 permutações compartilhadas, mesma semente; log-loss e acurácia).
Uso: python src/etapa1_py.py tarefa.json   (P7_RAIZ; NID_DIR = pasta do código do NID)
"""
import itertools
import json
import os
import sys
import time

import numpy as np
import pandas as pd

sys.path.insert(0, os.environ["NID_DIR"])
import torch  # noqa: E402
from torch import nn  # noqa: E402
from multilayer_perceptron import MLP, get_weights, train  # noqa: E402
from neural_interaction_detection import interpret_pairwise_interactions, preprocess_weights  # noqa: E402
from interpret.glassbox import ExplainableBoostingClassifier  # noqa: E402

T = json.load(open(sys.argv[1]))
RAIZ = os.environ["P7_RAIZ"]
V7 = ["interactionSNP1", "interactionSNP2"] + [f"effectSNP{i}" for i in range(1, 6)]
PARES = [f"{a}:{b}" for a, b in itertools.combinations(V7, 2)]
VERDADE = "interactionSNP1:interactionSNP2"
torch.set_num_threads(1)


def logloss(y, p):
    p = np.clip(p, 1e-15, 1 - 1e-15)
    return float(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)))


def acc(y, p):
    return float(np.mean((p > 0.5) == (y == 1)))


def regua(prever, Xte, yte, perms):
    b = prever(Xte)
    base = dict(ll=logloss(yte, b), ac=acc(yte, b))

    def queda(cols):
        ll, ac = [], []
        for o in perms:
            Xp = Xte.copy()
            Xp[cols] = Xte[cols].to_numpy()[o]
            p = prever(Xp)
            ll.append(logloss(yte, p)); ac.append(acc(yte, p))
        return np.mean(ll) - base["ll"], base["ac"] - np.mean(ac)
    ind = {v: queda([v]) for v in V7}
    I_ll, I_ac = {}, {}
    for pr in PARES:
        a, b2 = pr.split(":")
        q = queda([a, b2])
        I_ll[pr] = q[0] - ind[a][0] - ind[b2][0]
        I_ac[pr] = q[1] - ind[a][1] - ind[b2][1]
    return base, I_ll, I_ac


def postos(s, sinal):
    v = pd.Series(s, dtype=float)
    return (sinal * v).rank(ascending=False, method="average")


ddir = os.path.join(RAIZ, "resultados", "dados_etapa1", f"d{T['desenho']:02d}")
os.makedirs(T["saida"], exist_ok=True)
for r in T["repeticoes"]:
    arq = os.path.join(T["saida"], f"rep{r:03d}_py.csv")
    if os.path.exists(arq):
        continue
    sd = T["semente_base"] + 1000 * T["desenho"] + r
    tr = pd.read_csv(os.path.join(ddir, f"rep{r:03d}_treino.csv.gz"))
    te = pd.read_csv(os.path.join(ddir, f"rep{r:03d}_teste.csv.gz"))
    Xtr, ytr, Xte, yte = tr.drop(columns="pheno"), tr.pheno.to_numpy(), te.drop(columns="pheno"), te.pheno.to_numpy()
    cols = list(Xtr.columns)
    rng = np.random.default_rng(sd + 900000)
    perms = [rng.permutation(len(Xte)) for _ in range(30)]
    linhas, tempos, bases = [], {}, {}

    def add(det, tipo, sc, modelo):
        for pr in PARES:
            linhas.append(dict(detector=det, ranking=tipo, par=pr, escore=sc.get(pr, np.nan), modelo=modelo))

    # --- NID
    t0 = time.time()
    torch.manual_seed(sd); np.random.seed(sd % (2 ** 32))
    mu, sdv = Xtr.mean(), Xtr.std().replace(0, 1)
    Z = ((Xtr - mu) / sdv).to_numpy(np.float32)
    idx = np.random.permutation(len(Z)); nv = len(Z) // 5
    va, trn = idx[:nv], idx[nv:]
    mk = lambda X, y: torch.utils.data.DataLoader(torch.utils.data.TensorDataset(torch.tensor(X), torch.tensor(y, dtype=torch.float32)[:, None]),  # noqa: E731
                                                  batch_size=100, shuffle=True)
    loaders = {"train": mk(Z[trn], ytr[trn]), "val": mk(Z[va], ytr[va]), "test": mk(Z[va], ytr[va])}
    # classe MLP do repositório (como no demo.ipynb): get_weights lê as camadas 'interaction_mlp'; o detect_interactions
    # do próprio repositório usa create_mlp, cujas camadas não têm esse nome (inconsistência do código original)
    net = MLP(Z.shape[1], [256, 128, 64], use_main_effect_nets=False)
    net, _ = train(net, loaders, criterion=nn.BCEWithLogitsLoss(reduction="mean"), nepochs=100, early_stopping=True, patience=5,
                   l1_const=1e-4, learning_rate=0.01)
    w_in, w_later = preprocess_weights(get_weights(net))
    rk = interpret_pairwise_interactions(w_in, w_later)
    nid = {}
    for (i, j), s in rk:
        a, b = cols[i], cols[j]
        if a in V7 and b in V7:
            ab = sorted([a, b], key=V7.index)
            nid[f"{ab[0]}:{ab[1]}"] = float(s)
    tempos["nid"] = time.time() - t0
    add("nid", "nativo", nid, "nid")

    def prev_nid(X):
        with torch.no_grad():
            z = torch.tensor(((X - mu) / sdv).to_numpy(np.float32))
            return torch.sigmoid(net(z)).numpy().ravel()
    t0 = time.time(); b, ll, ac = regua(prev_nid, Xte, yte, perms); tempos["regua_nid"] = time.time() - t0
    bases["nid"] = b; add("nid", "global_logloss", ll, "nid"); add("nid", "global_acuracia", ac, "nid")

    # --- EBM
    t0 = time.time()
    ebm = ExplainableBoostingClassifier(random_state=sd % (2 ** 31), n_jobs=1)
    ebm.fit(Xtr, ytr)
    imp = dict(zip(ebm.term_names_, ebm.term_importances()))
    eb = {}
    for pr in PARES:
        a, b2 = pr.split(":")
        eb[pr] = float(imp.get(f"{a} & {b2}", imp.get(f"{b2} & {a}", 0.0)))
    tempos["ebm"] = time.time() - t0
    add("ebm", "nativo", eb, "ebm")
    t0 = time.time(); b, ll, ac = regua(lambda X: ebm.predict_proba(X)[:, 1], Xte, yte, perms); tempos["regua_ebm"] = time.time() - t0
    bases["ebm"] = b; add("ebm", "global_logloss", ll, "ebm"); add("ebm", "global_acuracia", ac, "ebm")

    L = pd.DataFrame(linhas)
    for nome, sinal, absol in [("posto", 1, False), ("posto_abs", 1, True), ("posto_neg", -1, False)]:
        L[nome] = L.groupby(["detector", "ranking"]).escore.transform(
            lambda s: (s.abs() if absol else sinal * s).rank(ascending=False, method="average"))
    L = L.assign(desenho=T["desenho"], model=T["model"], beta=T["beta"], beta_effect=T["beta_effect"], maf_interaction=T["maf_interaction"],
                 maf_effect=T["maf_effect"], mtry=T["mtry"][0] if isinstance(T["mtry"], list) else T["mtry"], repeticao=r, semente_dados=sd,
                 verdadeiro=L.par == VERDADE, n_pares_ebm_selecionados=sum(" & " in t for t in ebm.term_names_))
    L.to_csv(arq, index=False)
    pd.DataFrame([dict(repeticao=r, modelo=k, logloss=v["ll"], acuracia=v["ac"]) for k, v in bases.items()]).to_csv(
        os.path.join(T["saida"], f"rep{r:03d}_desempenho_py.csv"), index=False)
    json.dump({k: round(v, 2) for k, v in tempos.items()}, open(os.path.join(T["saida"], f"rep{r:03d}_tempos_py.json"), "w"))
print("ok")
