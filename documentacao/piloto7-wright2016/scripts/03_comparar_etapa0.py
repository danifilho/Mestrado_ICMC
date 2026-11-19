"""Etapa 0: compara as curvas de captura/detecção com o gabarito (gabarito_wright.csv), seção 4.5 do protocolo.
- Curva: proporção das repetições com posto <= k (individuais: k = 2..10; pares: k = 1..10), como em 02_plot_main.R.
- Critério 1: |nosso − publicado| <= 0,10 em >= 90 % dos pontos (cenário × modelo × medida × k).
- Critério 2: nenhuma inversão das ordens descritas no texto. Operacionalização (fixada aqui, antes de ver resultados):
  (a) Gini × Permutação: em cada cenário × modelo em que a média da curva publicada de Gini difere da de Permutação
      por mais de 0,10, o nosso sinal da diferença deve ser o mesmo;
  (b) "Sem interação" × "Só interação", para cada medida de pares: idem, comparando as médias das curvas dos dois modelos.
- Verificação da simulação (3.5): proporção média de casos por desenho dentro de ±0,02 da esperada.
Saídas: resultados/tabelas/etapa0_*.csv e etapa0_veredito.json. Uso: python3 scripts/03_comparar_etapa0.py [subconjunto|completo] [--de <pasta>] [--jvimp-de <pasta>]
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

R = Path(__file__).resolve().parents[1]
etapa = sys.argv[1] if len(sys.argv) > 1 else "subconjunto"
# Diagnóstico (D7): --jvimp-de <pasta> substitui as linhas de JVIMP pelas de outra rodada (ex.: etapa0_rfsrc161)
jvimp_de = sys.argv[sys.argv.index("--jvimp-de") + 1] if "--jvimp-de" in sys.argv else None
# D10: --de <pasta> lê outra rodada como base (ex.: etapa0_comp_rfsrc341); o rótulo da pasta entra no nome das saídas
base = sys.argv[sys.argv.index("--de") + 1] if "--de" in sys.argv else "etapa0"
sufixo = (f"_{base}" if base != "etapa0" else "") + (f"_jvimp_{jvimp_de}" if jvimp_de else "")
TAB = R / "resultados" / "tabelas"
TAB.mkdir(parents=True, exist_ok=True)
MOD = {"interaction_only": "Interaction only", "modifier_snp1": "Modifier SNP", "no_interaction": "No Interaction",
       "redundant": "Redundant", "synergistic": "Synergistic"}
ALG = {"impurity": "Gini", "permutation": "Permutation", "jvimp": "JVIMP", "jmst": "JMST", "pairwise": "PPI"}

d = pd.concat([pd.read_csv(f) for f in (R / "resultados" / "brutos" / base).glob("d*/rep*.csv")])
if jvimp_de:
    alt = pd.concat([pd.read_csv(f) for f in (R / "resultados" / "brutos" / jvimp_de).glob("d*/rep*.csv")])
    d = pd.concat([d[d.algo != "jvimp"], alt[alt.algo == "jvimp"]])
d = d[d.model.isin(MOD)]
if etapa == "subconjunto":  # os arquivos do piloto de tempo também têm mtry = 10 (2 repetições); o subconjunto é só mtry = 50
    d = d[d.mtry == 50]
d["modelo"], d["medida"] = d.model.map(MOD), d.algo.map(ALG)
chave = ["beta", "beta_effect", "maf_interaction", "maf_effect", "mtry", "modelo", "medida"]
curvas = []
for k in range(1, 11):
    g = d.assign(top=(d["rank"] <= k)).groupby(chave).agg(nosso=("top", "mean"), n_rep=("top", "size"), n_na=("rank", lambda s: s.isna().sum()))
    curvas.append(g.reset_index().assign(k=k))
C = pd.concat(curvas)
C = C[~((C.medida.isin(["Gini", "Permutation"])) & (C.k == 1))]
G = pd.read_csv(R / "gabarito_wright.csv").rename(columns={"beta_I": "beta", "beta_M": "beta_effect", "MAF_I": "maf_interaction",
                                                         "MAF_M": "maf_effect", "valor": "publicado"})
M = C.merge(G[chave + ["k", "publicado", "figura"]], on=chave + ["k"], how="left")
M["dif"] = M.nosso - M.publicado
M.to_csv(TAB / f"etapa0_{etapa}{sufixo}_pontos.csv", index=False)
crit1 = float((M.dif.abs() <= 0.10).mean())

med = M.groupby(chave).agg(nosso=("nosso", "mean"), publicado=("publicado", "mean")).reset_index()
inv = []
cen = ["beta", "beta_effect", "maf_interaction", "maf_effect", "mtry"]
for keys, g in med.groupby(cen + ["modelo"]):
    a, b = g[g.medida == "Gini"], g[g.medida == "Permutation"]
    if len(a) and len(b):
        dp, dn = a.publicado.iloc[0] - b.publicado.iloc[0], a.nosso.iloc[0] - b.nosso.iloc[0]
        if abs(dp) > 0.10:
            inv.append(dict(regra="Gini × Permutação", cenario=str(keys), dif_publicada=dp, dif_nossa=dn, invertida=np.sign(dp) != np.sign(dn)))
for keys, g in med.groupby(cen + ["medida"]):
    if keys[-1] in ("Gini", "Permutation"):
        continue
    a, b = g[g.modelo == "No Interaction"], g[g.modelo == "Interaction only"]
    if len(a) and len(b):
        dp, dn = a.publicado.iloc[0] - b.publicado.iloc[0], a.nosso.iloc[0] - b.nosso.iloc[0]
        if abs(dp) > 0.10:
            inv.append(dict(regra="Sem interação × Só interação", cenario=str(keys), dif_publicada=dp, dif_nossa=dn, invertida=np.sign(dp) != np.sign(dn)))
I = pd.DataFrame(inv)
I.to_csv(TAB / f"etapa0_{etapa}{sufixo}_ordens.csv", index=False)

prop = d.groupby(["desenho", "model", "beta", "beta_effect", "maf_interaction", "maf_effect"]).prop_casos.mean().reset_index()
esp = {(r["modelo"], r["beta_I"], r["beta_M"], r["MAF_I"], r["MAF_M"]): r["prop_casos"]
       for r in json.load(open(R / "auditoria" / "verificacao_simulacao.json"))["proporcao_casos"]}
NOME = {"interaction_only": "so_interacao", "modifier_snp1": "modificador_snp1", "modifier_snp2": "modificador_snp2",
        "no_interaction": "sem_interacao", "redundant": "redundante", "synergistic": "sinergico"}
prop["esperada"] = [esp.get((NOME[r.model], r.beta, r.beta_effect, r.maf_interaction, r.maf_effect)) for r in prop.itertuples()]
prop["dentro_0_02"] = (prop.prop_casos - prop.esperada).abs() <= 0.02
prop.to_csv(TAB / f"etapa0_{etapa}{sufixo}_proporcao_casos.csv", index=False)

ver = dict(etapa=etapa, n_pontos=int(len(M)), pontos_sem_gabarito=int(M.publicado.isna().sum()),
           frac_pontos_ate_0_10=crit1, criterio1=crit1 >= 0.90, dif_abs_media=float(M.dif.abs().mean()),
           ordens_avaliadas=int(len(I)), ordens_invertidas=int(I.invertida.sum()) if len(I) else 0,
           criterio2=bool(len(I) == 0 or not I.invertida.any()), rank_na=int(d["rank"].isna().sum()),
           proporcao_casos_ok=f"{int(prop.dentro_0_02.sum())}/{len(prop)}",
           por_medida=M.assign(ok=M.dif.abs() <= 0.10).groupby("medida").ok.mean().round(3).to_dict())
ver["P0_passa"] = bool(ver["criterio1"] and ver["criterio2"])
json.dump(ver, open(TAB / f"etapa0_{etapa}{sufixo}_veredito.json", "w"), indent=1, ensure_ascii=False)
print(json.dumps(ver, indent=1, ensure_ascii=False))
