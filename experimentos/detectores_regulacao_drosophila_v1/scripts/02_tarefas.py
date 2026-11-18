"""Gera as tarefas de uma etapa. Uso: python scripts/02_tarefas.py <etapa> [--metodos if irf rf] [--indices ...]
Etapas: piloto (IF, iRF, RF na reamostragem r01, semente 2026), principal (completo x 3 sementes +
reamostragens r01..rR com semente 2026), permutacao (p01..pP, semente 2026; IF, iRF e RF), oficial
(partição dos autores, semente 2026)."""
import argparse
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
CFG = json.loads((RAIZ / "configs" / "metodos.json").read_text())
EXE = json.loads((RAIZ / "configs" / "execucao.json").read_text())
ORDEM = ["if", "irf", "rf"]


def cfg(m):
    c = {k: v for k, v in CFG[m].items() if not k.startswith("_")}
    return c


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("etapa")
    ap.add_argument("--metodos", nargs="*", default=ORDEM)
    ap.add_argument("--n-reamostragens", type=int, default=EXE["reamostragens"]["n"])
    ap.add_argument("--n-permutacoes", type=int, default=EXE["permutacoes"]["n"])
    a = ap.parse_args()
    T = []
    for m in a.metodos:
        if a.etapa == "piloto":
            T.append(dict(id=f"{m}_r01_s2026", metodo=m, semente=2026, variante="reamostragem", indice="r01"))
        elif a.etapa == "principal":
            for s in EXE["sementes_algoritmo"]:
                T.append(dict(id=f"{m}_completo_s{s}", metodo=m, semente=s, variante="completo", indice="completo"))
            for r in range(1, a.n_reamostragens + 1):
                T.append(dict(id=f"{m}_r{r:02d}_s2026", metodo=m, semente=2026, variante="reamostragem", indice=f"r{r:02d}"))
        elif a.etapa == "permutacao":
            for p in range(1, a.n_permutacoes + 1):
                T.append(dict(id=f"{m}_p{p:02d}_s2026", metodo=m, semente=EXE["permutacoes"]["semente_ajuste"], variante="permutacao", indice=f"p{p:02d}"))
        elif a.etapa == "oficial":
            T.append(dict(id=f"{m}_oficial_s2026", metodo=m, semente=2026, variante="oficial", indice="oficial"))
    d = RAIZ / "resultados" / "logs" / "tarefas" / a.etapa
    d.mkdir(parents=True, exist_ok=True)
    lst = []
    for t in T:
        t.update(cfg=cfg(t["metodo"]), saida=str(Path("resultados") / "brutos" / a.etapa / t["id"]))
        p = d / f"{t['id']}.json"
        p.write_text(json.dumps(t, ensure_ascii=False, indent=1))
        lst.append(str(p.relative_to(RAIZ)))
    (d / "lista.txt").write_text("\n".join(lst) + "\n")
    print(len(T), "tarefas em", d / "lista.txt")


if __name__ == "__main__":
    main()
