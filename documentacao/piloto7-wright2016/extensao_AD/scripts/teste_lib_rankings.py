"""Testes com casos artificiais (seção 9): rankings totalmente empatados, idênticos e invertidos, e empates parciais.
Uso: python3 extensao_AD/scripts/teste_lib_rankings.py   (falha com AssertionError; grava auditoria/teste_lib_rankings.txt)"""
import sys
from pathlib import Path

import numpy as np

EXT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EXT / "scripts"))
from lib_rankings import (intersecao_esperada, jaccard_esperado, posto_medio_leq_k, prob_topk, ref_intersecao_aleatoria,  # noqa: E402
                          ref_jaccard_aleatorio, tau_b)

N, k = 21, 3
rng = np.random.default_rng(1)
log = []
emp = np.zeros(N); ident = np.arange(N, 0, -1.0); inv = ident[::-1]
# totalmente empatado: inclusão = k/N para todo item; tau indefinido; Jaccard com qualquer ranking = referência aleatória
assert np.allclose(prob_topk(emp, k), k / N); log.append(f"empatado: P(top-3) = {prob_topk(emp, k)[0]:.4f} (k/N = {k/N:.4f})")
assert np.isnan(tau_b(emp, ident)); log.append("empatado: tau-b indefinido (NaN)")
assert abs(intersecao_esperada(emp, ident, k) - k * k / N) < 1e-12
j, se = jaccard_esperado(emp, emp, k, rng, B=20000)
assert abs(j - ref_jaccard_aleatorio(k, N)) < 4 * se + 1e-3, (j, se, ref_jaccard_aleatorio(k, N))
log.append(f"empatado × empatado: Jaccard MC = {j:.4f} ± {se:.4f}; hipergeométrica = {ref_jaccard_aleatorio(k, N):.4f}")
# idênticos e invertidos
assert tau_b(ident, ident) == 1 and tau_b(ident, inv) == -1
assert jaccard_esperado(ident, ident, k) == (1.0, 0.0) and jaccard_esperado(ident, inv, k) == (0.0, 0.0)
log.append("idênticos: tau-b = 1, Jaccard = 1; invertidos: tau-b = −1, Jaccard = 0")
# empate parcial atravessando o corte: 2 itens empatados nas posições 3–4 → cada um 0,5
s = np.array([10, 9, 8, 8] + [1] * 17, float)
p = prob_topk(s, 3); assert np.allclose(p[:4], [1, 1, .5, .5]) and np.allclose(p[4:], 0) and abs(p.sum() - 3) < 1e-12
assert posto_medio_leq_k(s, 2, 3) == 0.0  # convenção histórica: posto médio 3,5 > 3 → não conta
log.append("empate parcial nas posições 3–4: inclusão fracionária 0,5 cada (convenção histórica: 0)")
# inclusão fracionária = média de desempates aleatórios
M = np.mean([np.argsort(-(s + 1e-9 * rng.random(N)))[:3].tolist().count(2) for _ in range(20000)])
assert abs(M - 0.5) < 0.02; log.append(f"verificação por simulação: {M:.3f}")
assert abs(ref_intersecao_aleatoria(k, N) - 9 / 21) < 1e-12
log.append(f"referências aleatórias (N = 21, k = 3): E|∩| = {9/21:.4f}; E[Jaccard] = {ref_jaccard_aleatorio(3, 21):.4f}")
log.append(f"referências aleatórias (N = 7, k = 3): E|∩| = {9/7:.4f}; E[Jaccard] = {ref_jaccard_aleatorio(3, 7):.4f}")
(EXT / "auditoria" / "teste_lib_rankings.txt").write_text("\n".join(log) + "\nTODOS OS TESTES PASSARAM\n")
print("\n".join(log)); print("TODOS OS TESTES PASSARAM")
