"""Estabilidade da árvore de componentes do piloto 3, separada da árvore de expressão."""
import itertools,json,time
import numpy as np,pandas as pd
from scipy.special import expit
from piloto4 import generate,FAMILIES,CFG,OUT,X
from piloto3_legado import signatures,INTER

def clades(nodes,labels):
 return {frozenset(labels[k] for k in n['leaves']) for n in nodes if 1<n['size']<11}
def rf(a,b):return len(a.symmetric_difference(b))/(len(a)+len(b))
def analyze():
 rows=[];pairs=[];start=time.time()
 for fi,fam in enumerate(FAMILIES):
  for rep in range(CFG['geradores_por_familia']):
   seed=CFG['seed']+fi*1000+rep;f,truth,meta=generate(fam,seed);p=expit((f-f.mean())/f.std());base=None;sets={}
   for trials in [0,1000,200]:
    for obs in range(1 if trials==0 else 4):
     rng=np.random.default_rng(seed+trials+obs*1000000);y=p if trials==0 else (rng.binomial(trials,p)+.5)/(trials+1)
     sig,nodes,E,order=signatures(y);labels=[''.join('ABCD'[k] for k in INTER[i]) for i in order];s=clades(nodes,labels)
     if trials==0:base=s;baseE={labels[j]:E[:,j] for j in range(11)}
     sets.setdefault(trials,[]).append(s)
     # Grupo de três variáveis corresponde a quatro componentes internos (3 pares + trio).
     expected=None
     if fam=='aninhado':
      g=next(g for g in meta['groups'] if len(g)==3);expected=frozenset(''.join('ABCD'[k] for k in c) for size in [2,3] for c in itertools.combinations(g,size))
     profile=np.array([E[:,labels.index(l)] for l in sorted(labels)]);ref=np.array([baseE[l] for l in sorted(labels)])
     rows.append(dict(family=fam,seed=seed,trials=trials,observation=obs,rf_vs_exact=rf(s,base),root_transform=nodes[-1]['best'],root_residual=nodes[-1]['cost']/max(nodes[-1]['before'],1e-10),zero_regret_nodes=sum(n['regret']<1e-9 for n in nodes[11:]),profile_absolute_rmse=np.sqrt(np.mean((profile-ref)**2)),triple_clade_hit=(int(expected in s) if expected else np.nan)))
   for trials,ss in sets.items():
    for a,b in itertools.combinations(ss,2):pairs.append(dict(family=fam,seed=seed,trials=trials,rf=rf(a,b)))
  print('Assinaturas',fam,'concluído',round(time.time()-start,1),flush=True)
 pd.DataFrame(rows).to_csv(OUT/'estabilidade_assinaturas.csv',index=False);pd.DataFrame(pairs).to_csv(OUT/'estabilidade_assinaturas_pares.csv',index=False)
 # Controle analítico-numérico: 3 árvores equilibradas e 12 aninhadas usando apenas somas.
 # Todas calculam exatamente a mesma função, independentemente de topologia.
 z=X@np.array([.8,1.1,-.9,.7]);a=expit(z);errors=[]
 for i,j in itertools.combinations(range(4),2):
  others=[k for k in range(4) if k not in [i,j]]
  for k in others:
   last=next(l for l in others if l!=k);w=np.array([.8,1.1,-.9,.7]);b=expit(((X[:,i]*w[i]+X[:,j]*w[j])+X[:,k]*w[k])+X[:,last]*w[last]);errors.append(float(np.max(abs(a-b))))
 for pair in [(0,1),(0,2),(0,3)]:
  other=[k for k in range(4) if k not in pair];w=np.array([.8,1.1,-.9,.7]);b=expit((X[:,pair]@w[list(pair)])+(X[:,other]@w[other]));errors.append(float(np.max(abs(a-b))))
 assert max(errors)<1e-14
 (OUT/'controle_ambiguidade.json').write_text(json.dumps(dict(arvores_equivalentes=len(errors),erro_maximo=max(errors),explicacao='Uma curva global de uma soma admite 15 árvores binárias de somas com a mesma resposta. Isso não prova equivalência de mecanismos celulares, mas impede identificar agrupamentos latentes dessas descrições pela resposta.'),indent=2,ensure_ascii=False))
if __name__=='__main__':analyze()
