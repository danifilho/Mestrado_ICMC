"""Auditoria posterior: não treina modelos nem altera a análise histórica.
Uso: python auditar_empates.py RAIZ_DO_ESTUDO PASTA_SAIDA
Em cada empate de tamanho e com b escores estritamente maiores, a probabilidade
exata de inclusão no top-k sob desempate uniforme é max(0,min(e,k-b))/e.
"""
import csv,collections,math,statistics,sys
from pathlib import Path
root=Path(sys.argv[1]);dest=Path(sys.argv[2]);dest.mkdir(parents=True,exist_ok=True)
out=collections.defaultdict(list)
for f in sorted((root/'resultados/brutos/etapa1').glob('d*/rep*.csv')):
 if 'desempenho' in f.name:continue
 groups=collections.defaultdict(list)
 for x in csv.DictReader(open(f)):
  if x['ranking']=='nativo':groups[x['detector']].append(x)
 for det,rows in groups.items():
  vals=[float(x['escore']) if x['escore'] not in ('NA','') else math.nan for x in rows]
  if any(not math.isfinite(v) for v in vals):raise ValueError(str(f)+' '+det)
  t=next(x for x in rows if x['verdadeiro'].lower()=='true');v=float(t['escore']);b=sum(w>v for w in vals);e=sum(w==v for w in vals)
  old=sum(float(t['posto'])<=k for k in range(1,11))/10
  new=sum(max(0,min(e,k-b))/e for k in range(1,11))/10
  out[det,t['model']].append((old,new,e>1,len(set(vals))==1,v==0))
with (dest/'sensibilidade_empates.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['detector','model','n','historico','desempate_fracionario','frac_par_empatado','frac_todos_iguais','frac_par_zero'])
 for (det,model),v in sorted(out.items()):w.writerow([det,model,len(v)]+[statistics.mean(x[i] for x in v) for i in range(5)])
print('Grupos auditados:',sum(map(len,out.values())))
