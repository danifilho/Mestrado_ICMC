"""Tarefas da Etapa 0 (seção 4.4): uma tarefa por (desenho de dados, bloco de repetições).
  subconjunto  mtry = 50; as 4 combinações das Figuras 3 e 4 (base; MAF_I = 0,4; beta_M = 0,8; beta_I = 0,8) x 5 modelos
  completo     os 72 desenhos do código (6 modelos x 2 beta_I x 2 beta_M x 3 pares de MAF) x mtry {10, 50}
  piloto       2 repetições de um desenho por modelo (tempo)
Desenho = índice fixo na lista completa (ordem do código: model x beta x beta_effect x pares de MAF).
Uso: python3 scripts/02_tarefas_etapa0.py <subconjunto|completo|piloto> [--bloco 10]
"""
import argparse
import itertools
import json
from pathlib import Path

R = Path(__file__).resolve().parents[1]
MODELOS = ["no_interaction", "synergistic", "interaction_only", "modifier_snp1", "modifier_snp2", "redundant"]
MAF = [(0.2, 0.2), (0.2, 0.4), (0.4, 0.2)]  # (MAF_I, MAF_M), como no código
DESENHOS = [dict(desenho=i + 1, model=m, beta=b, beta_effect=be, maf_interaction=mi, maf_effect=me)
            for i, (m, b, be, (mi, me)) in enumerate(itertools.product(MODELOS, [0.4, 0.8], [0.4, 0.8], MAF))]
FIG34 = [(0.4, 0.4, 0.2, 0.2), (0.4, 0.4, 0.4, 0.2), (0.4, 0.8, 0.2, 0.2), (0.8, 0.4, 0.2, 0.2)]
MEDIDAS = ["impurity", "permutation", "jvimp", "jmst", "pairwise"]

ap = argparse.ArgumentParser(); ap.add_argument("etapa"); ap.add_argument("--bloco", type=int, default=10)
ap.add_argument("--medidas", default=",".join(MEDIDAS)); ap.add_argument("--rotulo", default="")
a = ap.parse_args()
if a.etapa == "subconjunto":
    ds = [d for d in DESENHOS if d["model"] != "modifier_snp2" and (d["beta"], d["beta_effect"], d["maf_interaction"], d["maf_effect"]) in FIG34]
    mtry, reps = [50], range(1, 101)
elif a.etapa == "completo":
    ds, mtry, reps = DESENHOS, [10, 50], range(1, 101)
elif a.etapa in ("piloto",):
    ds = [d for d in DESENHOS if d["model"] != "modifier_snp2" and (d["beta"], d["beta_effect"], d["maf_interaction"], d["maf_effect"]) == FIG34[0]]
    mtry, reps = [10, 50], range(1, 3)
nome = a.etapa + (f"_{a.rotulo}" if a.rotulo else "")
pasta = R / "resultados" / "logs" / "tarefas" / nome
pasta.mkdir(parents=True, exist_ok=True)
for f in pasta.glob("*.json"):
    f.unlink()
lista = []
rl = list(reps)
for d in ds:
    for i in range(0, len(rl), a.bloco):
        bl = rl[i:i + a.bloco]
        t = dict(d, id=f"d{d['desenho']:02d}_r{bl[0]:03d}", n=1000, num_effect_snps=5, num_noise_snps=93, mtry=mtry, medidas=a.medidas.split(","),
                 repeticoes=bl, semente_base=12345, rng_rounding=False, saida=f"resultados/brutos/etapa0{'_' + a.rotulo if a.rotulo else ''}/d{d['desenho']:02d}")
        p = pasta / f"{t['id']}.json"
        json.dump(t, open(p, "w"), indent=1)
        lista.append(str(p.relative_to(R)))
(pasta / "lista.txt").write_text("\n".join(lista) + "\n")
print(nome, len(ds), "desenhos,", len(lista), "tarefas")
