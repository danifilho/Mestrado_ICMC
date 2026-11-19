"""Figuras da Etapa 1 (PNG e SVG, paleta verde do projeto) e dados de cada figura em figuras/dados/.
Entradas: resultados/tabelas/etapa1_*.csv (de 05_analisar_etapa1.py).
Gini e permutação (Wright) não entram nas figuras de pares: medem SNPs isolados (posto = máximo dos 2 SNPs entre 100), não o
posto do par entre 21, e não são comparáveis com os detectores de pares.
Uso: python3 scripts/06_figuras_etapa1.py
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

R = Path(__file__).resolve().parents[1]
TAB, FIG = R / "resultados" / "tabelas", R / "figuras"
DF = FIG / "dados"
DF.mkdir(parents=True, exist_ok=True)
ESC, MED, CLA, FUN, TXT, NEU, CIN = "#14532D", "#15803D", "#86BF91", "#E7F3E8", "#18352B", "#E9ECE9", "#6B7280"
plt.rcParams.update({"font.size": 9, "text.color": TXT, "axes.labelcolor": TXT, "xtick.color": TXT, "ytick.color": TXT,
                     "axes.edgecolor": TXT, "font.family": "DejaVu Sans", "savefig.dpi": 200,
                     "axes.spines.top": False, "axes.spines.right": False})
CMAP = matplotlib.colors.LinearSegmentedColormap.from_list("v", ["#FFFFFF", FUN, CLA, MED, ESC])
MODELOS = ["Só interação", "SNP modificador", "Sinérgico", "Redundante", "Sem interação"]
COM_INT = MODELOS[:4]
ACASO = np.mean([k / 21 for k in range(1, 11)])
NATIVOS = {"ebm": "EBM", "h": "H de Friedman (RF)", "rpf": "RPF (componente)", "shap": "SHAP interação (RF)", "sirf": "siRF",
           "irf": "iRF", "nid": "NID", "if_quant": "IF (EIM quantitativa)", "if_qual": "IF (EIM qualitativa)"}
WRIGHT = {"jvimp_W": "JVIMP (Wright, rfsrc 1.6.1)", "jmst_W": "JMST (Wright)", "ppi_W": "PPI (Wright)"}
# régua: um representante por modelo ajustado (h e shap herdam a do rf; sirf a do irf; if_qual a do if)
REGUA = {"rf": "RF", "if_quant": "IF", "irf": "iRF", "rpf": "RPF", "nid": "NID", "ebm": "EBM"}


def salvar(fig, nome, dados=None):
    for ext in ("png", "svg"):
        fig.savefig(FIG / f"{nome}.{ext}", bbox_inches="tight", facecolor="white")
    plt.close(fig)
    if dados is not None:
        dados.to_csv(DF / f"{nome}.csv", index=False)


G = pd.read_csv(TAB / "etapa1_resumo_por_modelo.csv")
G["com_int"] = G[COM_INT].mean(axis=1)


def linhas_tabela(direcao_regua):
    out = []
    for d, n in WRIGHT.items():
        r = G[(G.detector == d)].iloc[0]; out.append(dict(grupo="Wright (Etapa 0)", rotulo=n, **{m: r[m] for m in MODELOS}, com_int=r.com_int))
    for d, n in NATIVOS.items():
        r = G[(G.detector == d) & (G.ranking == "nativo")].iloc[0]; out.append(dict(grupo="Escore nativo", rotulo=n, **{m: r[m] for m in MODELOS}, com_int=r.com_int))
    for d, n in REGUA.items():
        r = G[(G.detector == d) & (G.ranking == "global_logloss") & (G.direcao == direcao_regua)].iloc[0]
        out.append(dict(grupo=f"Régua global ({direcao_regua}, log-loss)", rotulo=f"Régua · {n}", **{m: r[m] for m in MODELOS}, com_int=r.com_int))
    return pd.DataFrame(out)


def fig_mapa():
    T = linhas_tabela("|I|")
    T = pd.concat([g.sort_values("com_int", ascending=False) for _, g in T.groupby("grupo", sort=False)])
    M = T[MODELOS].to_numpy()
    fig, ax = plt.subplots(figsize=(8.2, 7.6))
    im = ax.imshow(M, cmap=CMAP, vmin=0, vmax=0.8, aspect="auto")
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            v = M[i, j]
            ax.text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=8, color="white" if v > 0.5 else TXT,
                    weight="bold" if (j < 4 and v >= 0.5) else "normal")
    ax.set_xticks(range(5), [m.replace(" ", "\n", 1) if m != "Sem interação" else "Sem interação\n(sem par a achar)" for m in MODELOS])
    ax.set_yticks(range(len(T)), T.rotulo)
    ax.xaxis.tick_top(); ax.tick_params(length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    # separadores entre grupos
    n = 0
    for _, g in T.groupby("grupo", sort=False):
        n += len(g)
        if n < len(T):
            ax.axhline(n - 0.5, color="white", lw=4)
    ax.axvline(3.5, color="white", lw=4)
    pos = 0
    for gnome, g in T.groupby("grupo", sort=False):
        ax.text(5.05, pos + (len(g) - 1) / 2, gnome, rotation=-90, va="center", ha="left", fontsize=8, color=CIN)
        pos += len(g)
    cb = fig.colorbar(im, ax=ax, fraction=0.03, pad=0.12); cb.set_label("Detecção média do par verdadeiro (k = 1…10)")
    cb.ax.axhline(ACASO, color=TXT, lw=1.5)
    cb.set_ticks([0, 0.2, ACASO, 0.4, 0.6, 0.8], labels=["0", "0,2", f"acaso {ACASO:.2f}".replace(".", ","), "0,4", "0,6", "0,8"])
    ax.set_title("Etapa 1: com que frequência cada detector põe o par verdadeiro no topo\n"
                 "(média de P(posto ≤ k), k = 1…10, entre os 21 pares; 4 cenários por modelo × 100 repetições)", fontsize=9.5, pad=40)
    fig.text(0.02, -0.02, "Em \"Sem interação\" os dois SNPs só têm efeitos marginais: valores acima do acaso ali indicam que o detector\n"
             "ranqueia o par pela força marginal, não pela interação. Régua com |I| (convenção principal, pré-fixada).", fontsize=7.5, color=CIN)
    salvar(fig, "e1_fig1_mapa_deteccao", T)


def fig_sinal_ruido():
    T = linhas_tabela("|I|")
    est = {"Wright (Etapa 0)": dict(marker="s", fc="white", ec=ESC), "Escore nativo": dict(marker="o", fc=MED, ec=MED),
           "Régua global (|I|, log-loss)": dict(marker="^", fc=CLA, ec=ESC)}
    fig, ax = plt.subplots(figsize=(8.4, 6.4))
    ax.axvline(ACASO, color=CIN, lw=0.8, ls=":"); ax.axhline(ACASO, color=CIN, lw=0.8, ls=":")
    ax.plot([0, 0.8], [0, 0.8], color=NEU, lw=1.2, zorder=0)
    ax.text(0.66, 0.635, "diagonal: mesma taxa\ncom e sem interação", fontsize=7, color=CIN, rotation=0, ha="left")
    ax.text(ACASO + 0.004, 0.205, "acaso", fontsize=7, color=CIN); ax.text(0.765, ACASO + 0.006, "acaso", fontsize=7, color=CIN)
    for g, s in est.items():
        d = T[T.grupo == g]
        ax.scatter(d["Sem interação"], d.com_int, s=46, lw=1.3, label=g, zorder=3, **{"marker": s["marker"], "facecolors": s["fc"], "edgecolors": s["ec"]})
    rot = T[T.grupo.isin(["Wright (Etapa 0)", "Escore nativo"]) | T.rotulo.isin(["Régua · NID", "Régua · RPF"])]
    desloc = {"EBM": (6, 2), "H de Friedman (RF)": (6, 4), "RPF (componente)": (6, 4), "SHAP interação (RF)": (6, -4),
              "siRF": (6, 3), "iRF": (6, -8), "NID": (6, -4), "IF (EIM quantitativa)": (-6, 6), "IF (EIM qualitativa)": (6, -8),
              "JVIMP (Wright, rfsrc 1.6.1)": (6, 2), "JMST (Wright)": (6, 4), "PPI (Wright)": (6, -6),
              "Régua · NID": (6, 2), "Régua · RPF": (6, -3)}
    for _, r in rot.iterrows():
        dx, dy = desloc.get(r.rotulo, (6, 0))
        ax.annotate(r.rotulo, (r["Sem interação"], r.com_int), xytext=(dx, dy), textcoords="offset points", fontsize=7,
                    ha="right" if dx < 0 else "left", va="center", color=TXT)
    grp = T[T.rotulo.isin(["Régua · RF", "Régua · IF", "Régua · iRF", "Régua · EBM"])]
    ax.annotate("Régua em RF, IF, iRF e EBM", (grp["Sem interação"].mean(), grp.com_int.max() + 0.008), xytext=(0.35, 0.585),
                fontsize=7, color=TXT, ha="center", arrowprops=dict(arrowstyle="-", color=CIN, lw=0.8))
    ax.set_xlim(0.2, 0.8); ax.set_ylim(0.2, 0.8)
    ax.set_xlabel("Detecção do par em \"Sem interação\" (só efeitos marginais; quanto menor, melhor)")
    ax.set_ylabel("Detecção média nos 4 modelos com interação (quanto maior, melhor)")
    ax.set_title("Sinal (eixo y) contra detecção espúria pela força marginal (eixo x)", fontsize=10)
    ax.legend(frameon=False, fontsize=7.5, loc="lower right")
    ax.grid(color=NEU, lw=0.6); ax.set_axisbelow(True)
    salvar(fig, "e1_fig2_sinal_vs_espurio", T[["grupo", "rotulo", "Sem interação", "com_int"]])


def fig_curvas():
    C = pd.read_csv(TAB / "etapa1_curvas_deteccao.csv")
    sel = [("ebm", "nativo", "nativo", "EBM (nativo)", ESC, "-", "o"),
           ("h", "nativo", "nativo", "H de Friedman (nativo)", MED, "-", "s"),
           ("rf", "global_logloss", "|I|", "Régua · RF (|I|)", CLA, "-", "^"),
           ("jvimp_W", "nativo (Etapa 0)", "Wright", "JVIMP (Wright)", TXT, "--", "D"),
           ("ppi_W", "nativo (Etapa 0)", "Wright", "PPI (Wright)", CIN, ":", "v")]
    fig, axs = plt.subplots(1, 5, figsize=(14, 3.6), sharey=True)
    dados = []
    for ax, m in zip(axs, MODELOS):
        ks = np.arange(1, 11)
        ax.plot(ks, ks / 21, color=CIN, lw=1, ls=(0, (1, 2)), label="acaso (k/21)")
        for det, rk, dr, nome, cor, ls, mk in sel:
            c = C[(C.detector == det) & (C.ranking == rk) & (C.direcao == dr) & (C.modelo == m)].groupby("k").deteccao.mean()
            ax.plot(c.index, c.values, color=cor, ls=ls, lw=2, marker=mk, ms=4, label=nome, mfc="white" if ls != "-" else cor)
            dados.append(pd.DataFrame(dict(modelo=m, detector=nome, k=c.index, deteccao=c.values)))
        ax.set_title(m, fontsize=9.5); ax.set_xticks([1, 5, 10]); ax.set_ylim(0, 1); ax.set_xlabel("k (top-k entre 21 pares)")
        ax.grid(color=NEU, lw=0.6); ax.set_axisbelow(True)
    axs[0].set_ylabel("P(par verdadeiro no top-k)")
    axs[-1].text(0.5, 0.97, "aqui, detecção = espúria", transform=axs[-1].transAxes, ha="center", va="top", fontsize=7, color=CIN)
    h, lab = axs[0].get_legend_handles_labels()
    fig.legend(h, lab, ncol=6, frameon=False, loc="upper center", bbox_to_anchor=(0.5, 1.08), fontsize=8)
    fig.suptitle("Curvas de detecção por modelo (média dos 4 cenários, 100 repetições cada)", y=1.14, fontsize=10)
    salvar(fig, "e1_fig3_curvas", pd.concat(dados))


def fig_concordancia():
    K = pd.read_csv(TAB / "etapa1_concordancia_resumo.csv")
    K = K[K.a.str.contains("nativo") & K.b.str.contains("nativo")]
    nomes = {f"{d} (nativo)": NATIVOS[d] for d in NATIVOS}
    ordem = [f"{d} (nativo)" for d in ["ebm", "h", "shap", "rpf", "irf", "sirf", "nid", "if_quant", "if_qual"]]
    M = pd.DataFrame(np.nan, index=ordem, columns=ordem)
    for _, r in K.iterrows():
        M.loc[r.a, r.b] = M.loc[r.b, r.a] = r.kendall_tau
    fig, ax = plt.subplots(figsize=(6.6, 5.6))
    Mv = M.to_numpy(); mask = np.triu(np.ones_like(Mv, bool))
    im = ax.imshow(np.where(mask, np.nan, Mv), cmap=CMAP, vmin=0, vmax=0.8)
    for i in range(len(ordem)):
        for j in range(i):
            v = Mv[i, j]; ax.text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=7.5, color="white" if v > 0.5 else TXT)
    ax.set_xticks(range(len(ordem)), [nomes[o] for o in ordem], rotation=40, ha="right"); ax.set_yticks(range(len(ordem)), [nomes[o] for o in ordem])
    ax.tick_params(length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    cb = fig.colorbar(im, ax=ax, fraction=0.04); cb.set_label("τ de Kendall médio (21 pares, mesma repetição)")
    ax.set_title("Concordância entre os rankings nativos (2.000 repetições)", fontsize=10)
    salvar(fig, "e1_fig4_concordancia", M.reset_index().rename(columns={"index": "detector"}))


fig_mapa(); fig_sinal_ruido(); fig_curvas(); fig_concordancia()
print("ok", sorted(p.name for p in FIG.glob("e1_*.png")))
