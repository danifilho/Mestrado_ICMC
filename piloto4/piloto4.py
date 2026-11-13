"""Piloto 4: testes complementares de assinaturas e modelos compostos.
As árvores de expressão não são as árvores de componentes do piloto 3.
"""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
from pathlib import Path
import itertools,json,time,sys
import numpy as np,pandas as pd
from scipy.optimize import least_squares
from scipy.special import expit
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.metrics import adjusted_rand_score
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
OUT=Path(__file__).parent/'resultados';OUT.mkdir(exist_ok=True)
X=np.array(list(itertools.product(np.linspace(-1,1,5),repeat=4)))
FAMILIES=['aditivo','curva_global','modulos','aninhado','sobreposto','curva_fora_banco']
CFG=dict(seed=20261113,geradores_por_familia=8,niveis=5,treinos=[100,250],validacao=125,teste=125,
 ruido=[0,.05,.15],replicas_ruidosas=3,starts=2,max_nfev=100,
 criterio='menor numero parametros dentro de 1 erro padrao da melhor MSE de validacao; empates por MSE',
 familia_curvas='identidade e tanh; arctan somente nos geradores fora do banco',
 dominio='fatorial completo 4 variaveis; teste retido por celulas inteiras',
 tipos_arvore='17 modelos de expressao: aditivo, curva global, 3 particoes equilibradas, 12 hierarquias aninhadas',
 adicionais='modelo de 2 indices compartilhados; ExtraTrees; oraculos estruturais e topologia incorreta')
# Convenção: u = x_i*w_i nas folhas; nó não linear = a*tanh(soma(filhos)+b).
# O nó raiz recebe também intercepto livre. Nós de soma não têm parâmetros.
def nonlinear(children):return ('t',children)
def add(children):return ('s',children)
MODELS=[dict(name='aditivo',expr=add([0,1,2,3]),groups=[]),dict(name='global',expr=nonlinear([0,1,2,3]),groups=[])]
for pair in [(0,1),(0,2),(0,3)]:
 other=tuple(i for i in range(4) if i not in pair)
 MODELS.append(dict(name='mod_' + ''.join(map(str,pair)),expr=add([nonlinear(list(pair)),nonlinear(list(other))]),groups=[tuple(pair),other]))
for pair in itertools.combinations(range(4),2):
 for third in (i for i in range(4) if i not in pair):
  fourth=next(i for i in range(4) if i not in pair and i!=third)
  MODELS.append(dict(name='nest_'+''.join(map(str,pair))+str(third),expr=add([nonlinear([nonlinear(list(pair)),third]),fourth]),groups=[tuple(pair),tuple(sorted((*pair,third)))]))

def compile_expr(expr):
 count=[5]
 def go(e):
  if isinstance(e,int):return e
  kind,children=e;cc=[go(c) for c in children]
  if kind=='t':idx=count[0];count[0]+=2;return(kind,cc,idx)
  return(kind,cc,None)
 tree=go(expr);return tree,count[0]
for m in MODELS:m['compiled'],m['npar']=compile_expr(m['expr'])

def eval_tree(m,p,x,curve='tanh'):
 n=len(x);k=len(p)
 def go(t):
  if isinstance(t,int):
   jac=np.zeros((n,k));jac[:,t]=x[:,t];return p[t]*x[:,t],jac
  kind,children,idx=t;vals=[go(c) for c in children];z=sum(v[0] for v in vals);j=sum(v[1] for v in vals)
  if kind=='s':return z,j
  a,b=p[idx:idx+2];u=z+b
  if curve=='tanh':h=np.tanh(u);dh=1-h*h
  else:h=np.arctan(u);dh=1/(1+u*u)
  out=a*h;j=a*dh[:,None]*j;j[:,idx]=h;j[:,idx+1]=a*dh
  return out,j
 out,jac=go(m['compiled']);out=out+p[4];jac[:,4]=1;return out,jac

def eval_free(p,x):
 # Dois índices com variáveis compartilhadas + soma linear: não impõe grupos exclusivos.
 W=p[:8].reshape(2,4);b=p[8:10];a=p[10:12];z=x@W.T+b;t=np.tanh(z);d=1-t*t
 out=t@a+x@p[12:16]+p[16];j=np.zeros((len(x),17))
 for i in range(2):j[:,4*i:4*i+4]=(a[i]*d[:,i])[:,None]*x;j[:,8+i]=a[i]*d[:,i];j[:,10+i]=t[:,i]
 j[:,12:16]=x;j[:,16]=1;return out,j

def fit(m,x,y,seed):
 rng=np.random.default_rng(seed);free=m is None;k=17 if free else m['npar'];fun=eval_free if free else lambda p,x:eval_tree(m,p,x)
 if not free and m['name']=='aditivo':
  p=np.linalg.lstsq(np.c_[x,np.ones(len(x))],y,rcond=None)[0];return p,True,1
 best=None
 for start in range(CFG['starts']):
  p=rng.uniform(.4,1.2,k)*rng.choice([-1,1],k)
  if free:p[8:10]=0;p[12:16]=0;p[16]=np.mean(y)
  else:
   p[4]=np.mean(y)
   for j in range(5,k,2):p[j]=1.;p[j+1]=0.
  cache={}
  def both(p):
   if 'p' not in cache or not np.array_equal(cache['p'],p):cache['p']=p.copy();cache['v'],cache['j']=fun(p,x)
   return cache['v'],cache['j']
  r=least_squares(lambda p:both(p)[0]-y,p,jac=lambda p:both(p)[1],bounds=(-6,6),max_nfev=CFG['max_nfev'],ftol=1e-7,xtol=1e-7,gtol=1e-7)
  if best is None or r.cost<best.cost:best=r
 return best.x,bool(best.success),int(best.nfev)

def generate(family,seed):
 rng=np.random.default_rng(seed);perm=rng.permutation(4)
 if family=='aditivo':m=MODELS[0]
 elif family=='curva_global':m=MODELS[1]
 elif family in ['modulos','curva_fora_banco']:m=MODELS[2+rng.integers(3)]
 elif family=='aninhado':m=MODELS[5+rng.integers(12)]
 else:
  w=rng.uniform(.5,1.4,(2,4))*rng.choice([-1,1],(2,4));w[0,perm[3]]=0;w[1,perm[0]]=0
  # Dois intermediários com sobreposição de duas variáveis; sem árvore exclusiva imposta.
  p=np.r_[w.ravel(),rng.uniform(-.2,.2,2),rng.uniform(.7,1.3,2),np.zeros(4),rng.uniform(-.2,.2)]
  f,_=eval_free(p,X);return f,None,dict(params=p.tolist(),groups=[sorted(perm[:3].tolist()),sorted(perm[1:].tolist())],model='indices_sobrepostos')
 p=np.empty(m['npar']);p[:4]=rng.uniform(.6,1.5,4)*rng.choice([-1,1],4);p[4]=rng.uniform(-.2,.2)
 for j in range(5,len(p),2):p[j]=rng.uniform(.7,1.5);p[j+1]=rng.uniform(-.3,.3)
 f,_=eval_tree(m,p,X,'arctan' if family=='curva_fora_banco' else 'tanh')
 return f,m,dict(params=p.tolist(),groups=m['groups'],model=m['name'])

def select(rows):
 best=min(rows,key=lambda r:r['mse_val']);limit=best['mse_val']+best['se_val']
 cand=[r for r in rows if r['mse_val']<=limit+1e-12]
 return min(cand,key=lambda r:(r['npar'],r['mse_val'])),cand

def checks():
 from scipy.optimize._numdiff import approx_derivative
 rng=np.random.default_rng(10)
 for m in MODELS:
  p=rng.normal(size=m['npar']);v,j=eval_tree(m,p,X[:10]);np.testing.assert_allclose(j,approx_derivative(lambda q:eval_tree(m,q,X[:10])[0],p),atol=1e-6)
 p=rng.normal(size=17);np.testing.assert_allclose(eval_free(p,X[:10])[1],approx_derivative(lambda q:eval_free(q,X[:10])[0],p),atol=1e-6)
 assert len(MODELS)==17
 print('Jacobianos analíticos e catálogo: OK',flush=True)

def run_predict(quick=False):
 (OUT/'protocolo.json').write_text(json.dumps(CFG,ensure_ascii=False,indent=2));checks();start=time.time();rows=[];summary=[];gens=[]
 nseeds=1 if quick else CFG['geradores_por_familia']
 for fi,fam in enumerate(FAMILIES):
  for rep in range(nseeds):
   seed=CFG['seed']+fi*1000+rep;f,truth,meta=generate(fam,seed);sd=f.std();gens.append(dict(family=fam,seed=seed,**meta));r=np.random.default_rng(seed+100000);ix=r.permutation(625);pool=ix[:375];val=ix[375:500];test=ix[500:]
   for noise in ([.05] if quick else CFG['ruido']):
    for obs in range(1 if quick or noise==0 else CFG['replicas_ruidosas']):
     rng=np.random.default_rng(seed+10000+obs*100+int(noise*1000));y=f+rng.normal(0,noise*sd,625)
     for ntrain in ([100] if quick else CFG['treinos']):
      train=pool[:ntrain];key=f'{fam}_{rep}_{noise}_{obs}_{ntrain}';fits=[];preds={}
      for mi,m in enumerate(MODELS+[None]):
       name=m['name'] if m else 'indices_livres';p,success,nfev=fit(m,X[train],y[train],seed+mi*100+obs)
       pred=eval_tree(m,p,X)[0] if m else eval_free(p,X)[0];ev=(pred[val]-y[val])**2/sd**2
       row=dict(condition=key,family=fam,seed=seed,noise=noise,observation=obs,ntrain=ntrain,model=name,npar=m['npar'] if m else 17,mse_val=float(ev.mean()),se_val=float(ev.std(ddof=1)/np.sqrt(len(ev))),nmse=float(np.mean((pred[test]-f[test])**2)/sd**2),success=success,nfev=nfev)
       fits.append(row);preds[name]=pred;rows.append(row)
      et=ExtraTreesRegressor(n_estimators=150,min_samples_leaf=2,random_state=seed,n_jobs=1).fit(X[train],y[train]);pred=et.predict(X);ev=(pred[val]-y[val])**2/sd**2
      row=dict(condition=key,family=fam,seed=seed,noise=noise,observation=obs,ntrain=ntrain,model='ExtraTrees',npar=np.nan,mse_val=float(ev.mean()),se_val=float(ev.std(ddof=1)/np.sqrt(len(ev))),nmse=float(np.mean((pred[test]-f[test])**2)/sd**2),success=True,nfev=0);rows.append(row)
      tree,candidates=select(fits[:17]);flat,_=select(fits[:5]);allfit,candall=select(fits);best=min(fits[:17],key=lambda q:q['mse_val']);wrong=None
      if truth is not None and fam in ['modulos','aninhado']:
       ids=range(2,5) if fam=='modulos' else range(5,17);wrong=min([fits[i] for i in ids if MODELS[i]['name']!=truth['name']],key=lambda q:q['mse_val'])
      group_hit=np.nan if fam not in ['modulos','aninhado'] else int(tree['model']==truth['name'])
      oracle=next((q for q in fits if truth and q['model']==truth['name']),None)
      summary.append(dict(condition=key,family=fam,seed=seed,noise=noise,observation=obs,ntrain=ntrain,selected_tree=tree['model'],selected_all=allfit['model'],compatible=';'.join(q['model'] for q in candidates),num_compatible=len(candidates),nmse_tree=tree['nmse'],nmse_flat=flat['nmse'],nmse_free=fits[-1]['nmse'],nmse_extra=row['nmse'],nmse_oracle=oracle['nmse'] if oracle else np.nan,nmse_wrong=wrong['nmse'] if wrong else np.nan,group_hit=group_hit,non_tree_selected=allfit['model']=='indices_livres',ambiguous_topologies=len(candidates)>1,truth=meta['model']))
      pd.DataFrame(summary).to_csv(OUT/'previsao_resumo.csv',index=False)
   print(f'{fam} gerador {rep+1}/{nseeds} concluído; {time.time()-start:.1f}s',flush=True)
 pd.DataFrame(rows).to_csv(OUT/'ajustes.csv',index=False);pd.DataFrame(summary).to_csv(OUT/'previsao_resumo.csv',index=False);(OUT/'geradores.json').write_text(json.dumps(gens,indent=2));return pd.DataFrame(summary)

if __name__=='__main__':run_predict('--quick' in sys.argv)
