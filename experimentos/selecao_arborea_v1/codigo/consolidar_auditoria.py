import json,csv,hashlib,subprocess
from pathlib import Path
root=Path(__file__).resolve().parents[1]
methods=['RF','IF','iRF','RPF','UFO','RLT','EBM']
rows=[];costs=[]
for m in methods:
 for n in [120,1000]:
  p=root/'resultados'/f'{m}_{n}.json'
  d=json.loads(p.read_text()) if p.exists() else {'status':'PENDENTE'}
  rows.append({'metodo':m,'n':n,'p':8 if n==120 else 100,'status':d['status'],'versao':d.get('version',''),'ajuste_s':d.get('fit_seconds',''),'auditoria_s':d.get('total_seconds',''),'checagens_aprovadas':sum(bool(v) for v in d.get('checks',{}).values())})
 p=root/'resultados'/f'{m}_cost.json'
 if p.exists():
  d=json.loads(p.read_text());ft=d['fit_seconds'];pr=d['predict_1000_seconds']
  costs.append({'metodo':m,'ajuste_s':ft,'previsao_1000_s':pr,'chamadas_regua':841,'horas_6000_ajustes':ft*6000/3600,'horas_6000_ajustes_com_regua':(ft+841*pr)*6000/3600})
for file,data in [('AUDITORIA_EXECUTADA.csv',rows),('ESTIMATIVA_CUSTO.csv',costs)]:
 if data:
  with (root/file).open('w') as f:
   w=csv.DictWriter(f,fieldnames=data[0].keys());w.writeheader();w.writerows(data)
lines=['# Auditoria executada e estimativa de custo','', 'Data: 23/11/2026. Testes de engenharia com resposta balanceada independente dos atributos. Não foi comparado desempenho nem recuperação de interações. O resultado PASS indica que passaram oito verificações específicas, não validação integral do algoritmo.','', '| Método | Dimensão | Estado | Primeiro ajuste (s) | Verificações aprovadas |','|---|---|---|---:|---:|']
for r in rows:lines.append(f"|{r['metodo']}|{r['n']}×{r['p']}|{r['status']}|{r['ajuste_s']}|{r['checagens_aprovadas']}|")
lines+=['','As oito verificações são: probabilidades finitas e limitadas, repetição com mesma semente, serialização, equivariância à ordem das linhas, preservação da entrada e previsão após permutar A, B e AB. As dez verificações adicionais da régua estão em `resultados/testes_regua.json`. Não se verificou aqui convergência de toda a distribuição de escores, desempenho em todas as distribuições nem igualdade entre máquinas.','','## Custo condicional do desenho proposto','','O pesquisador escolheu priorizar os padrões dos autores e definir o teto após a estimativa. A conta abaixo usa 20 cenários × 100 realizações × 3 sementes = 6000 ajustes por método. A régua possui 1 + 30×(7+21) = 841 chamadas de previsão de 1000 linhas por ajuste. As sete chamadas de conjuntos individuais permitem calcular o contraste secundário; a medida principal de pares sozinha usaria 631 chamadas.','','| Método | Ajuste (s) | Previsão de 1000 linhas (s) | Só ajustes (h de um núcleo) | Ajustes e régua (h de um núcleo) |','|---|---:|---:|---:|---:|']
for r in costs:lines.append(f"|{r['metodo']}|{r['ajuste_s']:.3f}|{r['previsao_1000_s']:.5f}|{r['horas_6000_ajustes']:.1f}|{r['horas_6000_ajustes_com_regua']:.1f}|")
lines += ['',f"Total dos {len(costs)} métodos com perfil disponível: **{sum(r['horas_6000_ajustes_com_regua'] for r in costs):.1f} horas de um núcleo**, por extrapolação.", '', 'Essa é uma projeção de tempo de parede em uma thread, não uma medição de CPU-h da execução científica. Parte dos perfis ocorreu com outros testes ativos. A distribuição usada tem resposta independente e pode produzir árvores e componentes diferentes dos cenários de Wright; especialmente a poda do RPF pode modificar muito o custo. A medida não inclui controles, extração nativa, bootstrap, transferência e armazenamento, verificações ou tentativas com falha. Também não é estimativa de incerteza: uma linha de perfil por método é insuficiente para um intervalo de custo.', '', 'O perfil faz um ajuste e dez previsões após aquecimento, sem calcular perdas comparativas. Todos os tempos individuais e a configuração estão nos JSON `*_cost.json`. Usar outra máquina, paralelismo ou previsão em lotes exige novo perfil; não prometer aceleração linear. A escolha de um teto menor pode exigir reduzir o desenho ou otimizar a implementação da régua, mas não justifica alterar silenciosamente os algoritmos.', '', 'Nenhuma nova avaliação científica foi iniciada. As sementes futuras foram apenas enumeradas.']
(root/'AUDITORIA_E_CUSTO.md').write_text('\n'.join(lines)+'\n')
subprocess.run(['python3',str(root/'codigo/gerar_mapa.py')],check=True)
