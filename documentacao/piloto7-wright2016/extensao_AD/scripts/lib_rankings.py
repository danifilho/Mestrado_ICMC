"""Funções de ranking com tratamento explícito de empates (extensão A–D). Convenção: escore MAIOR = mais importante.

Empates são tratados como desempate aleatório uniforme e independente entre rankings:
- prob_topk: probabilidade de cada item estar no top-k = clip((k − nº estritamente melhores) / nº empatados com ele, 0, 1).
  É a "inclusão fracionária": para o item-alvo, equivale à recuperação esperada sob desempate aleatório.
- intersecao_esperada: E|T1 ∩ T2| = Σ_i p1_i · p2_i (exata, pois os desempates são independentes entre os rankings).
- jaccard_esperado: E[|∩| / |∪|] (não linear): exata quando não há empate atravessando o corte; senão, Monte Carlo com
  B desempates por ranking (gerador registrado), devolvendo média e erro-padrão de Monte Carlo.
- tau_b: Kendall tau-b (scipy); NaN (indefinido) se um dos rankings for constante.
- referências de listas aleatórias do mesmo tamanho: E|∩| = k²/N; E[Jaccard] pela hipergeométrica.
- posto_medio_leq_k: convenção histórica (posto médio ≤ k), mantida só para comparação.
"""
from math import comb

import numpy as np
from scipy.stats import kendalltau


def prob_topk(s, k):
    s = np.asarray(s, float)
    melhores = (s[None, :] > s[:, None]).sum(1)
    empatados = (s[None, :] == s[:, None]).sum(1)
    return np.clip((k - melhores) / empatados, 0.0, 1.0)


def intersecao_esperada(s1, s2, k):
    return float((prob_topk(s1, k) * prob_topk(s2, k)).sum())


def _topk_desempate(s, k, rng, B):
    s = np.asarray(s, float)
    u = rng.random((B, len(s)))
    ordem = np.lexsort((u, -np.broadcast_to(s, (B, len(s)))), axis=1)  # chave principal: −s; desempate: u
    M = np.zeros((B, len(s)), bool)
    np.put_along_axis(M, ordem[:, :k], True, axis=1)
    return M


def jaccard_esperado(s1, s2, k, rng=None, B=400):
    p1, p2 = prob_topk(s1, k), prob_topk(s2, k)
    if np.all((p1 == 0) | (p1 == 1)) and np.all((p2 == 0) | (p2 == 1)):
        i = float((p1 * p2).sum())
        return i / (2 * k - i), 0.0
    rng = rng if rng is not None else np.random.default_rng(0)
    A, C = _topk_desempate(s1, k, rng, B), _topk_desempate(s2, k, rng, B)
    i = (A & C).sum(1)
    J = i / (2 * k - i)
    return float(J.mean()), float(J.std(ddof=1) / np.sqrt(B))


def tau_b(s1, s2):
    s1, s2 = np.asarray(s1, float), np.asarray(s2, float)
    if np.all(s1 == s1[0]) or np.all(s2 == s2[0]):
        return np.nan
    return float(kendalltau(s1, s2, variant="b").statistic)


def ref_intersecao_aleatoria(k, N):
    return k * k / N


def ref_jaccard_aleatorio(k, N):
    # |∩| ~ Hipergeométrica(N, k, k)
    return float(sum(comb(k, j) * comb(N - k, k - j) / comb(N, k) * j / (2 * k - j) for j in range(0, k + 1)))


def posto_medio_leq_k(s, alvo, k):
    s = np.asarray(s, float)
    posto = (s > s[alvo]).sum() + ((s == s[alvo]).sum() + 1) / 2
    return float(posto <= k)


def n_empates(s):
    s = np.asarray(s, float)
    return int(len(s) - len(np.unique(s)))
