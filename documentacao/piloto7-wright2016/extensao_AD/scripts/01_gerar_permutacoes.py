"""Extensão A–D: índices de permutação COMPARTILHADOS entre todos os modelos, sementes de ajuste e linguagens (R e Python).
Para cada (desenho, realização): 30 permutações das 1.000 linhas do teste, geradas uma única vez e gravadas em arquivo.
Gerador: numpy default_rng(semente_dados + 900000), a MESMA construção da parte Python histórica (src/etapa1_py.py), de modo
que a régua histórica do EBM e do NID usou exatamente estas permutações (verificável). A parte R histórica usou outras
(sample.int do R), por isso a régua histórica dos modelos em R não é comparável valor a valor (ver DECISOES_EXTENSAO E3).
Formato: CSV gzip, 1.000 linhas × 30 colunas p01..p30, índices 1-based (linha do teste que entra na posição i).
Saída: resultados/permutacoes/dXX/repRRR.csv.gz e resultados/permutacoes/manifesto_permutacoes.csv (sha256 do arquivo gzip,
  gravado com mtime = 0, e uma impressão digital Σ P[i,q]·i·q que os executores R e Python recalculam e gravam em cada saída).
Uso: python3 extensao_AD/scripts/01_gerar_permutacoes.py [--desenhos 1,25] [--reps 1-5]
"""
import argparse
import gzip
import hashlib
import io
import json
from pathlib import Path

import numpy as np

EXT = Path(__file__).resolve().parents[1]
P7 = EXT.parent
ap = argparse.ArgumentParser()
ap.add_argument("--desenhos", default=None)
ap.add_argument("--reps", default="1-100")
ap.add_argument("--n_perm", type=int, default=30)
ap.add_argument("--n_teste", type=int, default=1000)
a = ap.parse_args()
cen = json.load(open(EXT / "configs" / "cenarios.json"))
ds = [c["desenho"] for c in cen] if a.desenhos is None else [int(x) for x in a.desenhos.split(",")]
r0, r1 = (int(x) for x in a.reps.split("-"))
linhas = []
for d in ds:
    pasta = EXT / "resultados" / "permutacoes" / f"d{d:02d}"
    pasta.mkdir(parents=True, exist_ok=True)
    for r in range(r0, r1 + 1):
        sd = 12345 + 1000 * d + r
        rng = np.random.default_rng(sd + 900000)
        P = np.column_stack([rng.permutation(a.n_teste) + 1 for _ in range(a.n_perm)])
        buf = io.StringIO()
        buf.write(",".join(f"p{q + 1:02d}" for q in range(a.n_perm)) + "\n")
        np.savetxt(buf, P, fmt="%d", delimiter=",")
        dados = buf.getvalue().encode()
        arq = pasta / f"rep{r:03d}.csv.gz"
        with gzip.GzipFile(arq, "wb", mtime=0) as g:  # mtime = 0: arquivo byte a byte reprodutível
            g.write(dados)
        # impressão digital independente de formato, calculada igual em R e Python: soma de P[i,q]·i·q (inteiros exatos em double)
        ii, qq = np.meshgrid(np.arange(1, a.n_teste + 1), np.arange(1, a.n_perm + 1), indexing="ij")
        digital = int((P.astype(np.int64) * ii * qq).sum())
        linhas.append(f"{d},{r},{sd},{sd + 900000},{hashlib.sha256(arq.read_bytes()).hexdigest()},{digital}")
man = EXT / "resultados" / "permutacoes" / "manifesto_permutacoes.csv"
antigas = man.read_text().splitlines()[1:] if man.exists() else []
chave = {tuple(l.split(",")[:2]) for l in linhas}
todas = [l for l in antigas if tuple(l.split(",")[:2]) not in chave] + linhas
man.write_text("desenho,repeticao,semente_dados,semente_perm,sha256_arquivo,digital\n" + "\n".join(sorted(todas, key=lambda s: tuple(map(int, s.split(",")[:2])))) + "\n")
print(len(linhas), "arquivos de permutação;", man)
