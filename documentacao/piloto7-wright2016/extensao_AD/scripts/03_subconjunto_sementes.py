"""Extensão A–D, Ensaio C: subconjunto balanceado de realizações para as sementes de ajuste adicionais, sorteado e fixado ANTES
de qualquer ranking da extensão (não usa resultados, só o número da realização). Para cada um dos 20 cenários, sorteia n_por_cenario
realizações entre 1..100 sem reposição, com numpy default_rng(20261119 + desenho). Também fixa o subconjunto da verificação de
estabilidade das 30 permutações (as 10 primeiras do sorteio de cada cenário).
Uso: python3 extensao_AD/scripts/03_subconjunto_sementes.py [--n 20]
Saída: configs/subconjunto_sementes.json e configs/subconjunto_estabilidade_perm.json
"""
import argparse
import json
from pathlib import Path

import numpy as np

EXT = Path(__file__).resolve().parents[1]
ap = argparse.ArgumentParser(); ap.add_argument("--n", type=int, default=20); a = ap.parse_args()
cen = json.load(open(EXT / "configs" / "cenarios.json"))
sub, est = {}, {}
for c in cen:
    d = c["desenho"]
    sorteio = (np.random.default_rng(20261119 + d).permutation(100) + 1)[: a.n].tolist()
    sub[d] = sorted(sorteio); est[d] = sorted(sorteio[:10])
json.dump(sub, open(EXT / "configs" / "subconjunto_sementes.json", "w"), indent=1)
json.dump(est, open(EXT / "configs" / "subconjunto_estabilidade_perm.json", "w"), indent=1)
print({k: v[:5] for k, v in list(sub.items())[:3]}, "...")
