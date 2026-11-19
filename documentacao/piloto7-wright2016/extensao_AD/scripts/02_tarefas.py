"""Extensão A–D: listas de tarefas (uma por desenho × bloco de realizações × semente de ajuste).
Uso: python3 extensao_AD/scripts/02_tarefas.py <rodada> [--desenhos 25,1] [--reps 1-5 | --reps-arquivo f.json] [--sementes 0,1,2]
     [--bloco 1] [--validar]
--reps-arquivo: JSON {desenho: [realizações]} (subconjunto sorteado e fixado previamente; ver 03_subconjunto_sementes.py).
Saída: resultados/logs/tarefas/<rodada>/*.json e lista.txt (caminhos relativos à raiz do Piloto 7).
"""
import argparse
import json
from pathlib import Path

EXT = Path(__file__).resolve().parents[1]
P7 = EXT.parent
ap = argparse.ArgumentParser()
ap.add_argument("rodada"); ap.add_argument("--desenhos"); ap.add_argument("--reps", default="1-100"); ap.add_argument("--reps-arquivo")
ap.add_argument("--sementes", default="0"); ap.add_argument("--bloco", type=int, default=1); ap.add_argument("--validar", action="store_true")
a = ap.parse_args()
cen = {c["desenho"]: c for c in json.load(open(EXT / "configs" / "cenarios.json"))}
ds = list(cen) if a.desenhos is None else [int(x) for x in a.desenhos.split(",")]
if a.reps_arquivo:
    R = {int(k): v for k, v in json.load(open(a.reps_arquivo)).items()}
else:
    r0, r1 = (int(x) for x in a.reps.split("-")); R = {d: list(range(r0, r1 + 1)) for d in ds}
pasta = EXT / "resultados" / "logs" / "tarefas" / a.rodada
pasta.mkdir(parents=True, exist_ok=True)
for f in pasta.glob("*.json"):
    f.unlink()
lista = []
for s in [int(x) for x in a.sementes.split(",")]:
    for d in ds:
        reps = R[d]
        for i in range(0, len(reps), a.bloco):
            bl = reps[i:i + a.bloco]
            t = dict(cen[d], id=f"d{d:02d}_r{bl[0]:03d}_s{s}", repeticoes=bl, semente_base=12345, semente_ajuste=s, validar=a.validar,
                     saida=f"resultados/brutos/{a.rodada}/d{d:02d}")
            p = pasta / f"{t['id']}.json"; json.dump(t, open(p, "w"), indent=1); lista.append(str(p.relative_to(P7)))
(pasta / "lista.txt").write_text("\n".join(lista) + "\n")
print(a.rodada, len(lista), "tarefas")
