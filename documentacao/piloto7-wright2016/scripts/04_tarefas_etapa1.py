"""Tarefas da Etapa 1: os mesmos 20 cenários do subconjunto da Etapa 0 (mtry = 50; 4 combinações das Figuras 3 e 4 x
5 modelos), mesmas sementes de dados. Uma tarefa por (desenho, bloco de repetições).
Uso: python3 scripts/04_tarefas_etapa1.py <etapa1|piloto1> [--bloco 5]
"""
import argparse
import json
import sys
from pathlib import Path

R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R / "scripts"))
from importlib import import_module  # noqa: E402

ap = argparse.ArgumentParser(); ap.add_argument("etapa"); ap.add_argument("--bloco", type=int, default=5)
a = ap.parse_args()
sys.argv = ["x", "subconjunto"]
T0 = import_module("02_tarefas_etapa0")
ds = [d for d in T0.DESENHOS if d["model"] != "modifier_snp2" and (d["beta"], d["beta_effect"], d["maf_interaction"], d["maf_effect"]) in T0.FIG34]
reps = list(range(1, 101)) if a.etapa == "etapa1" else [1]
if a.etapa == "piloto1":
    ds = [d for d in ds if (d["beta"], d["beta_effect"], d["maf_interaction"], d["maf_effect"]) == T0.FIG34[0]]
pasta = R / "resultados" / "logs" / "tarefas" / a.etapa
pasta.mkdir(parents=True, exist_ok=True)
for f in pasta.glob("*.json"):
    f.unlink()
lista = []
for d in ds:
    for i in range(0, len(reps), a.bloco):
        bl = reps[i:i + a.bloco]
        t = dict(d, id=f"d{d['desenho']:02d}_r{bl[0]:03d}", mtry=[50], repeticoes=bl, semente_base=12345,
                 saida=f"resultados/brutos/{a.etapa}/d{d['desenho']:02d}")
        p = pasta / f"{t['id']}.json"
        json.dump(t, open(p, "w"), indent=1)
        lista.append(str(p.relative_to(R)))
(pasta / "lista.txt").write_text("\n".join(lista) + "\n")
print(a.etapa, len(ds), "desenhos,", len(lista), "tarefas")
