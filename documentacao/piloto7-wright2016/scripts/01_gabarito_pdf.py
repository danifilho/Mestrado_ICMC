"""Gabarito numérico da Etapa 0 (seção 4.5): extrai as curvas das Figuras S1–S48 do Arquivo adicional 4 de
Wright et al. (2016) diretamente do PDF vetorial (gráficos ggplot embutidos como XObjects).
- Legenda de cada figura (texto da página): beta_I, beta_M, MAF_I, MAF_M, mtry.
- Em cada XObject: painéis = retângulos de fundo cinza (0,922); curvas = polilinhas (m ... l ... S) com a cor da
  medida (paleta Set1 do script dos autores, 02_plot_main.R). Ordem dos painéis (facet_wrap): Interaction only,
  Modifier SNP, No Interaction, Redundant, Synergistic (níveis do fator, conferidos pelos rótulos das faixas).
- Conversão para dados: ylim(0, 1) com a expansão padrão de 5 % (y = -0,05 no fundo do painel e 1,05 no topo);
  x contínuo de min(k) a max(k) com a mesma expansão. Conferido pelas linhas de grade principais (0; 0,25; ...; 1).
Saída: gabarito_wright.csv (figura, parâmetros, modelo, medida, k, valor) e auditoria/gabarito_extracao.json.
Uso: python3 -I scripts/01_gabarito_pdf.py
"""
import json
import re
import zlib
from pathlib import Path

R = Path(__file__).resolve().parents[1]
b = (R / "fontes" / "MOESM4_ESM.pdf").read_bytes()
objs = {int(n): o for n, o in re.findall(rb"(\d+) 0 obj(.*?)endobj", b, re.S)}


def stream(o):
    m = re.search(rb"stream\r?\n(.*)\r?\nendstream", o, re.S)
    if not m:
        return None
    d = m.group(1)
    return zlib.decompress(d) if b"FlateDecode" in o[:m.start()] else d


CORES = {(0.894, 0.102, 0.110): "Gini", (0.216, 0.494, 0.722): "Permutation", (0.302, 0.686, 0.290): "JVIMP",
         (0.596, 0.306, 0.639): "JMST", (1.000, 0.498, 0.000): "PPI"}
MODELOS = ["Interaction only", "Modifier SNP", "No Interaction", "Redundant", "Synergistic"]


def cor(t):
    best = min(CORES, key=lambda c: sum((a - x) ** 2 for a, x in zip(c, t)))
    return CORES[best] if sum((a - x) ** 2 for a, x in zip(best, t)) < 1e-3 else None


def legenda(txt):
    s = b"".join(re.findall(rb"\((.*?)\)", txt)).decode("latin1")
    return s


def parse_pagina(c, recursos):
    """Pares (nome do XObject, texto da legenda que vem depois)."""
    xo = dict(re.findall(rb"/(Im\d+) (\d+) 0 R", recursos))
    partes = re.split(rb"/(Im\d+) Do", c)
    out = []
    for i in range(1, len(partes), 2):
        nome = partes[i]
        cap = re.search(rb"BT(.*?)ET", partes[i + 1], re.S)
        out.append((int(xo[nome]), legenda(cap.group(1)) if cap else ""))
    return out


def params(cap):
    s = cap.replace(" ", "")
    m = re.match(r"FigureS(\d+):", s)
    if not m:
        return None
    vals = re.findall(r"=0:?(\d)", s)
    mt = re.search(r"mtry=(\d+)", s)
    d = dict(figura=int(m.group(1)))
    nums = re.findall(r"=(0:\d|\d+)", s)
    nums = [float(x.replace(":", ".")) if ":" in x else float(x) for x in nums]
    mt = re.search(r"mtry=(10|50)", s)  # a legenda da S3 traz um "1" colado (nota de rodapé): ler só 10 ou 50
    if len(nums) >= 4 and mt:
        d.update(beta_I=nums[0], beta_M=nums[1], MAF_I=nums[2], MAF_M=nums[3], mtry=int(mt.group(1)))
    d["legenda"] = cap
    return d


def curvas(xob):
    d = stream(objs[xob])
    toks = d.decode("latin1")
    # painéis: retângulos preenchidos com cinza 0,922
    paineis = [tuple(map(float, m)) for m in re.findall(r"0\.922 0\.922 0\.922 scn\n([\d.]+) ([\d.]+) ([\d.]+) ([\d.]+) re f", toks)]
    linhas = []
    cor_atual = None
    for m in re.finditer(r"([\d.]+) ([\d.]+) ([\d.]+) SCN|((?:[\d.]+ [\d.]+ [ml]\n)+)S\n", toks):
        if m.group(1):
            cor_atual = tuple(float(m.group(i)) for i in (1, 2, 3))
        else:
            pts = [tuple(map(float, p)) for p in re.findall(r"([\d.]+) ([\d.]+) [ml]", m.group(4))]
            med = cor(cor_atual) if cor_atual else None
            if med and len(pts) >= 3:
                linhas.append((med, pts))
    # linhas de grade horizontais principais (branco, 1,07 de espessura) para conferência
    return paineis, linhas


linhas_csv, aud = [], dict(figuras=[])
paginas = [n for n, o in objs.items() if re.search(rb"/Type\s*/Page[^s]", o)]
for n in sorted(paginas):
    o = objs[n]
    c = stream(objs[int(re.search(rb"/Contents\s+(\d+) 0 R", o).group(1))])
    rr = re.search(rb"/Resources\s+(\d+) 0 R", o)
    recursos = objs[int(rr.group(1))] if rr else o
    if b"Do" not in c:
        continue
    for xob, cap in parse_pagina(c, recursos):
        p = params(cap)
        if not p or p["figura"] > 48:
            continue
        paineis, linhas = curvas(xob)
        paineis = sorted(paineis, key=lambda r: r[0])
        reg = dict(p, n_paineis=len(paineis), n_curvas=len(linhas))
        for med, pts in linhas:
            xs = [x for x, _ in pts]
            ip = max(i for i, r in enumerate(paineis) if r[0] - 1 <= min(xs))
            x0, y0, w, h = paineis[ip]
            ks = list(range(2, 11)) if med in ("Gini", "Permutation") else list(range(1, 11))
            if len(pts) != len(ks):
                reg.setdefault("avisos", []).append(f"{med} painel {ip}: {len(pts)} pontos")
                continue
            lo, hi = min(ks), max(ks)
            ex = 0.05 * (hi - lo)
            for (x, y), k in zip(pts, ks):
                kx = (lo - ex) + (x - x0) / w * (hi - lo + 2 * ex)
                val = -0.05 + (y - y0) / h * 1.1
                linhas_csv.append(dict(figura=p["figura"], beta_I=p.get("beta_I"), beta_M=p.get("beta_M"), MAF_I=p.get("MAF_I"),
                                       MAF_M=p.get("MAF_M"), mtry=p.get("mtry"), modelo=MODELOS[ip], medida=med, k=k,
                                       k_lido=round(kx, 3), valor=round(val, 4)))
        aud["figuras"].append(reg)

import csv  # noqa: E402
with open(R / "gabarito_wright.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(linhas_csv[0]))
    w.writeheader(); w.writerows(linhas_csv)
dk = max(abs(r["k_lido"] - r["k"]) for r in linhas_csv)
aud.update(n_pontos=len(linhas_csv), desvio_max_k=dk, valor_min=min(r["valor"] for r in linhas_csv),
           valor_max=max(r["valor"] for r in linhas_csv))
json.dump(aud, open(R / "auditoria" / "gabarito_extracao.json", "w"), indent=1, ensure_ascii=False)
print(len(aud["figuras"]), "figuras;", len(linhas_csv), "pontos; desvio máximo de k:", dk,
      "; valores", aud["valor_min"], aud["valor_max"])
for r in aud["figuras"][:6]:
    print({k: r[k] for k in r if k != "legenda"})
