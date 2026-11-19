"""Congelamento antes da execução principal: sha256 de dados, partições, configuração, código e testes.
Grava configs/congelamento.json. Uso: python3 scripts/congelar.py "<motivo>"
Para conferir depois: python3 scripts/congelar.py --conferir
"""
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
ALVOS = ["PROTOCOLO.md", "DECISOES.md", "gabarito_wright.csv", "fontes/MOESM*", "fontes/codigo_autores/replication/01_main_simulation/*",
         "src/*.R", "scripts/*.py", "scripts/*.sb"]
SAIDA = RAIZ / "configs" / "congelamento.json"


def hashes():
    h = {}
    for padrao in ALVOS:
        for p in sorted(RAIZ.glob(padrao)):
            if p.is_file() and p.name != "congelar.py":
                h[str(p.relative_to(RAIZ))] = hashlib.sha256(p.read_bytes()).hexdigest()
    return h


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--conferir":
        ref = json.load(open(SAIDA))["sha256"]
        atual = hashes()
        dif = sorted(k for k in set(ref) | set(atual) if ref.get(k) != atual.get(k))
        print("alterados desde o congelamento:", dif if dif else "nenhum")
    else:
        json.dump(dict(data=datetime.now(timezone.utc).isoformat(timespec="seconds"), motivo=" ".join(sys.argv[1:]),
                       sha256=hashes()), open(SAIDA, "w"), indent=1, ensure_ascii=False)
        print("congelado:", SAIDA, len(hashes()), "arquivos")
