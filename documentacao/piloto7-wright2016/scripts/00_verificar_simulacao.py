"""Seção 3.5 do protocolo: verificação da simulação antes de qualquer floresta.
(1) Penetrâncias da Tabela 3 de Wright et al. (2016): Só interação, beta_I = beta_M = 0,4, MAF_I = 0,4, MAF_M = 0,2,
    com o beta0 da fórmula do código (seção 3.1), média sobre a soma dos 5 SNPs marginais ~ Binomial(10; MAF_M).
(2) Proporção esperada de casos em cada desenho de dados do código (6 modelos x 2 beta_I x 2 beta_M x 3 pares de MAF),
    calculada exatamente pela soma sobre os genótipos (Hardy-Weinberg).
Não usa os arquivos dos autores: as fórmulas vêm do protocolo; a conferência contra problems.R fica para quando o
Arquivo adicional 3 estiver disponível. Uso: python3 scripts/00_verificar_simulacao.py
"""
import itertools
import json
from math import comb, exp, log
from pathlib import Path

R = Path(__file__).resolve().parents[1]
s = lambda z: 1 / (1 + exp(-z))  # noqa: E731
logit = lambda p: log(p / (1 - p))  # noqa: E731


def beta0(bI, bM, mi, me):
    return -logit(0.5) - 2 * bI * (2 * mi) - 5 * bM * (2 * me)


def hw(p):
    return [(1 - p) ** 2, 2 * p * (1 - p), p ** 2]


# Tabela 1 do artigo (seção 3.2 do protocolo): (c1, c2, c12) em unidades de beta_I.
# O código tem 6 modelos (problems.R, conferido em D3): modifier_snp1 = (0, beta, beta), o "Modifier SNP" das figuras;
# modifier_snp2 = (beta, 0, beta), não plotado.
MODELOS = {"so_interacao": (0, 0, 1), "modificador_snp1": (0, 1, 1), "modificador_snp2": (1, 0, 1),
           "sem_interacao": (1, 1, 0), "redundante": (1, 1, -1), "sinergico": (1, 1, 1)}

# (1) Tabela 3
bI = bM = 0.4; mi, me = 0.4, 0.2
b0 = beta0(bI, bM, mi, me)
pE = [comb(10, k) * me ** k * (1 - me) ** (10 - k) for k in range(11)]
artigo = {(0, 0): 0.35, (1, 1): 0.44, (2, 1): 0.54, (2, 2): 0.72}
tab3 = []
for (x1, x2), pub in artigo.items():
    pen = sum(pE[k] * s(b0 + bM * k + bI * x1 * x2) for k in range(11))
    tab3.append(dict(x1=x1, x2=x2, nossa=round(pen, 4), artigo=pub, diferenca=round(pen - pub, 4)))

# (2) proporção esperada de casos por desenho
props = []
for (nome, (c1, c2, c12)), bI_, bM_, (mi_, me_) in itertools.product(MODELOS.items(), [0.4, 0.8], [0.4, 0.8],
                                                                      [(0.2, 0.2), (0.2, 0.4), (0.4, 0.2)]):
    b0_ = beta0(bI_, bM_, mi_, me_)
    pE_ = [comb(10, k) * me_ ** k * (1 - me_) ** (10 - k) for k in range(11)]
    g = hw(mi_)
    p = sum(g[x1] * g[x2] * pE_[k] * s(b0_ + bM_ * k + bI_ * (c1 * x1 + c2 * x2 + c12 * x1 * x2))
            for x1 in range(3) for x2 in range(3) for k in range(11))
    props.append(dict(modelo=nome, beta_I=bI_, beta_M=bM_, MAF_I=mi_, MAF_M=me_, beta0=round(b0_, 4), prop_casos=round(p, 4)))
out = dict(beta0_tabela3=round(b0, 4), tabela3=tab3, proporcao_casos=props,
           prop_min=min(x["prop_casos"] for x in props), prop_max=max(x["prop_casos"] for x in props))
json.dump(out, open(R / "auditoria" / "verificacao_simulacao.json", "w"), indent=1, ensure_ascii=False)
print("beta0 =", out["beta0_tabela3"])
for t in tab3:
    print(t)
print("proporção de casos: mín", out["prop_min"], "máx", out["prop_max"])
