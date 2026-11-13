"""Assinaturas de interações por transformações. Piloto exploratório reproduzível.
Não usa GO, rótulos biológicos reais, iRF nem afirma identificabilidade causal.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
from pathlib import Path
import itertools,json,time
import numpy as np
import pandas as pd
from scipy.special import expit,logit,ndtr,ndtri
from scipy.stats import skew,kurtosis
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.metrics import accuracy_score,confusion_matrix
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
O=Path(__file__).parent/'resultados'
CFG=dict(seed=20261112,n_por_familia_treino=60,n_por_familia_teste=40,n_por_familia_shift=40,
         grid=[-1,-.5,0,.5,1],familias=['indice_unico','modulos_exclusivos','tracos_compartilhados','par_especifico','interacoes_distribuidas'],
         curvas_observacao=['logistica','probit'],ruido=['exato','binomial1000'],
         transformacoes=['identidade','log','raiz','quadrado','inverso_negativo','logit','probit'],
         limiar_presenca=1e-4,classificador='ExtraTrees 250 arvores max_depth=8 min_samples_leaf=3 max_features=1.0',
         shift='ganho final 2.0–2.6 versus 0.8–1.5; mecanismos e familias iguais',
         bootstrap=1000,permutacoes_rotulos=20,
         arvore='folhas=11 componentes de ordem >=2; fusao com menor arrependimento de uma transformacao comum; desempate por perfil e indices canonicos')
LEVELS=np.array(CFG['grid']);X=np.array(list(itertools.product(LEVELS,repeat=4)))
SUBS=[s for k in range(1,5) for s in itertools.combinations(range(4),k)]
INTER=[s for s in SUBS if len(s)>=2];ORD=np.array([len(s) for s in INTER]);TN=CFG['transformacoes']

def normalize(z):return (z-z.mean())/z.std()

def generate(family,rng,shift=False):
 # Sinais, magnitudes e nomes de variáveis aleatórios em todas as famílias.
 w=rng.uniform(.6,1.4,4)*rng.choice([-1,1],4);perm=rng.permutation(4);Z=X[:,perm]
 k=rng.uniform(.7,1.7,2);q=rng.uniform(.6,1.4)
 if family==0:z=Z@w
 elif family==1:z=np.tanh(k[0]*(Z[:,:2]@w[:2]))+q*np.tanh(k[1]*(Z[:,2:]@w[2:]))
 elif family==2:
  v=rng.uniform(.6,1.4,4)*rng.choice([-1,1],4)
  # Evita que os dois índices sejam quase a mesma direção.
  for _ in range(100):
   if abs(w@v/np.linalg.norm(w)/np.linalg.norm(v))<.8:break
   v=rng.uniform(.6,1.4,4)*rng.choice([-1,1],4)
  z=np.tanh(k[0]*(Z@w))+q*np.tanh(k[1]*(Z@v))
 elif family==3:z=Z@w+rng.uniform(.8,1.5)*rng.choice([-1,1])*Z[:,0]*Z[:,1]
 else:
  co=rng.uniform(.5,1.3,6)*rng.choice([-1,1],6)
  z=Z@w+sum(c*Z[:,i]*Z[:,j] for c,(i,j) in zip(co,itertools.combinations(range(4),2)))/np.sqrt(2)
 z=normalize(z);offset=rng.uniform(-.4,.4);gain=rng.uniform(2,2.6) if shift else rng.uniform(.8,1.5)
 outer=int(rng.integers(2));eta=offset+gain*z
 # Ajusta escala do probit para amplitude aproximadamente comparável à logística.
 p=expit(eta) if outer==0 else ndtr(eta/1.7)
 return p,dict(ganho=gain,offset=offset,curva=outer,permutacao=perm.tolist(),pesos=w.tolist())

def decompose(y):
 arr=y.reshape((5,)*4);f0=arr.mean();parts={():np.full((1,)*4,f0)};energies=[]
 for S in SUBS:
  axes=tuple(i for i in range(4) if i not in S)
  comp=arr.mean(axis=axes,keepdims=True) if axes else arr.copy()
  for T,v in parts.items():
   if set(T).issubset(S):comp=comp-v
  parts[S]=comp;energies.append(float(np.mean(comp**2)/np.var(arr)))
 return np.array(energies),parts

def transform(y):
 assert y.min()>0 and y.max()<1
 return [y,np.log(y),np.sqrt(y),y*y,-1/y,logit(y),ndtri(y)]

def build_tree(E,orders):
 # E: transformações x componentes, cada energia / variância total da escala.
 # C(S) = mínimo_t soma_s E[t,s]. O custo de fusão é sempre não negativo.
 nodes=[];clusters={};n=E.shape[1]
 for i in range(n):
  t=int(np.argmin(E[:,i]));clusters[i]=[i]
  nodes.append(dict(id=i,leaves=[i],size=1,best=t,cost=float(E[t,i]),before=float(E[0,i]),regret=0.,height=0.,children=[]))
 while len(clusters)>1:
  options=[]
  for i,j in itertools.combinations(clusters,2):
   L=clusters[i]+clusters[j];values=E[:,L].sum(1);t=int(values.argmin());cost=float(values[t]);before=float(values[0])
   regret=max(0.,cost-nodes[i]['cost']-nodes[j]['cost'])/max(before,1e-12)
   prof_i=E[:,clusters[i]].sum(1);prof_j=E[:,clusters[j]].sum(1)
   distance=float(np.linalg.norm(np.log10(prof_i+1e-8)-np.log10(prof_j+1e-8)))
   options.append((round(regret,12),distance,i,j,L,t,cost,before,regret))
  _,_,i,j,L,t,cost,before,regret=min(options,key=lambda z:z[:4]);idx=len(nodes)
  height=max(nodes[i]['height'],nodes[j]['height'])+regret+1e-4
  nodes.append(dict(id=idx,leaves=L,size=len(L),best=t,cost=cost,before=before,regret=regret,height=height,children=[i,j]))
  del clusters[i];del clusters[j];clusters[idx]=L
 return nodes

def signatures(y):
 allE=np.array([decompose(t)[0] for t in transform(y)])
 E=allE[:,4:];assert E.shape==(7,11)
 # Canonicalização sem nomes dos genes; não usa família geradora.
 order=sorted(range(11),key=lambda j:(int(ORD[j]),*np.round(np.log10(E[:,j]+1e-10),10)))
 E=E[:,order];ords=ORD[order];nodes=build_tree(E,ords)
 pairs=allE[0,4:10];base=allE[0];higher=[base[4:10].sum(),base[10:14].sum(),base[14]]
 moments=np.r_[y.mean(),y.std(),skew(y),kurtosis(y),np.quantile(y,[.05,.25,.5,.75,.95])]
 raw=np.r_[np.sort(base[:4]),np.sort(pairs),np.sort(base[10:14]),base[14]]
 # Árvore: características dos nós internos, ordenadas sem rótulos de variáveis.
 features=[]
 for node in sorted(nodes[11:],key=lambda n:(n['size'],n['best'],round(n['cost'],12),round(n['regret'],12))):
  L=node['leaves'];features.extend([node['size']/11,np.mean(ords[L])/4,np.log10(node['before']+1e-10),np.log10(node['cost']+1e-10),
    node['cost']/max(node['before'],1e-10),node['regret'],*np.eye(7)[node['best']]])
 # Perfil sem árvore contém a matriz da qual a árvore é derivada.
 matrix=np.log10(E.T+1e-10).ravel()
 tree=np.array(features)
 out={'momentos':moments,'presenca_pares':np.sort((pairs>CFG['limiar_presenca']).astype(float)),
      'fanova_bruta':raw,'perfil_sem_arvore':matrix,'arvore':tree,'perfil_mais_arvore':np.r_[matrix,tree],
      'controle_mais_arvore':np.r_[moments,raw,tree]}
 return out,nodes,E,order

def checks():
 z=X.sum(1);en,parts=decompose(z)
 assert en[4:].max()<1e-20 and abs(en.sum()-1)<1e-12
 np.testing.assert_allclose(sum(parts.values()).reshape(-1),z,atol=1e-12)
 en,_=decompose(X[:,0]*X[:,1]);assert abs(en[4]-1)<1e-12
 p=expit(X.sum(1));en,_=decompose(logit(p));assert en[4:].sum()<1e-20
 sig,n,E,order=signatures(p)
 assert len(n)==21 and n[-1]['size']==11 and n[-1]['cost']<1e-20
 assert all(t['regret']>=0 for t in n)
 # A transformação comum não pode custar menos que a soma dos mínimos independentes.
 for t in n[11:]:assert t['cost']+1e-12>=sum(n[c]['cost'] for c in t['children'])
 # Invariância a renomear variáveis em uma função não degenerada.
 rng=np.random.default_rng(291);p,_=generate(2,rng);p2=p.reshape((5,)*4).transpose(2,0,3,1).ravel()
 s1,*_=signatures(p);s2,*_=signatures(p2)
 for key in s1:np.testing.assert_allclose(s1[key],s2[key],atol=1e-8)
 print('Verificações: reconstrução fANOVA, aditividade, par puro, curva global, custos, renomeação: OK',flush=True)

def classifier(seed):return ExtraTreesClassifier(n_estimators=250,max_depth=8,min_samples_leaf=3,max_features=1.,random_state=seed,n_jobs=1)

def ci_accuracy(correct,seed):
 rng=np.random.default_rng(seed);v=[np.mean(correct[rng.integers(len(correct),size=len(correct))]) for _ in range(CFG['bootstrap'])]
 return np.quantile(v,[.025,.975])

def run():
 O.mkdir(exist_ok=True);(O/'protocolo.json').write_text(json.dumps(CFG,indent=2,ensure_ascii=False));checks();start=time.time()
 meta=[];store={};trees={};responses=[]
 for regime,n in [('treino',60),('teste',40),('shift',40)]:
  for family in range(5):
   for j in range(n):
    seed=CFG['seed']+100000*['treino','teste','shift'].index(regime)+1000*family+j
    rng=np.random.default_rng(seed);p,param=generate(family,rng,regime=='shift')
    for noise in CFG['ruido']:
     y=p if noise=='exato' else (rng.binomial(1000,p)+.5)/1001
     feats,nodes,E,order=signatures(y)
     idx=len(meta);meta.append(dict(id=idx,familia=family,nome=CFG['familias'][family],regime=regime,ruido=noise,seed=seed,**param))
     for key,val in feats.items():store.setdefault(key,[]).append(val)
     responses.append(y)
     if regime=='teste' and j==0 and noise=='exato':trees[str(family)]=dict(nodes=nodes,energies=E.tolist(),labels=[''.join('ABCD'[k] for k in INTER[i]) for i in order])
   print(f'Gerado {regime}, família {family}, {time.time()-start:.1f}s',flush=True)
 m=pd.DataFrame(meta);m.to_csv(O/'datasets.csv',index=False)
 for key in store:store[key]=np.array(store[key])
 np.savez_compressed(O/'assinaturas.npz',**store);np.savez_compressed(O/'respostas.npz',respostas=np.array(responses))
 (O/'arvores_exemplos.json').write_text(json.dumps(trees,indent=2))
 results=[];predrows=[];predictions={}
 for noise in CFG['ruido']:
  train=(m.regime=='treino')&(m.ruido==noise);target=m.familia.values
  for key,F in store.items():
   model=classifier(312);model.fit(F[train],target[train])
   for regime in ['teste','shift']:
    ix=np.flatnonzero((m.regime==regime)&(m.ruido==noise));pred=model.predict(F[ix]);correct=pred==target[ix];lo,hi=ci_accuracy(correct,713)
    results.append(dict(ruido=noise,regime=regime,assinatura=key,acuracia=correct.mean(),ic_inf=lo,ic_sup=hi,n=len(ix),dimensao=F.shape[1]))
    predictions[(noise,regime,key)]=pred
    predrows.extend(dict(id=int(i),assinatura=key,previsto=int(v),correto=bool(v==target[i])) for i,v in zip(ix,pred))
  print(f'Classificação {noise} concluída {time.time()-start:.1f}s',flush=True)
 pd.DataFrame(results).to_csv(O/'desempenho.csv',index=False);pd.DataFrame(predrows).to_csv(O/'previsoes.csv',index=False)
 # Diferenças pareadas: mesmos conjuntos de teste, sem selecionar pelo resultado.
 diffs=[]
 for noise in CFG['ruido']:
  for regime in ['teste','shift']:
   truth=m[(m.regime==regime)&(m.ruido==noise)].familia.values
   for ka,kb in [('arvore','fanova_bruta'),('arvore','perfil_sem_arvore'),('perfil_mais_arvore','perfil_sem_arvore'),('controle_mais_arvore','momentos')]:
    delta=(predictions[(noise,regime,ka)]==truth).astype(float)-(predictions[(noise,regime,kb)]==truth).astype(float)
    lo,hi=ci_accuracy(delta,843);diffs.append(dict(ruido=noise,regime=regime,A=ka,B=kb,diferenca=delta.mean(),ic_inf=lo,ic_sup=hi))
 pd.DataFrame(diffs).to_csv(O/'diferencas_pareadas.csv',index=False)
 # Controle negativo: permuta rótulos SOMENTE no treino; rótulos de teste permanecem reais.
 neg=[]
 for b in range(CFG['permutacoes_rotulos']):
  mask=(m.regime=='treino')&(m.ruido=='exato');test=(m.regime=='teste')&(m.ruido=='exato');r=np.random.default_rng(9000+b)
  model=classifier(b);model.fit(store['arvore'][mask],r.permutation(m.familia.values[mask]));pred=model.predict(store['arvore'][test]);neg.append(accuracy_score(m.familia.values[test],pred))
 pd.DataFrame({'acuracia':neg}).to_csv(O/'controle_rotulos_permutados.csv',index=False)
 plots(m,store,results,predictions,trees)
 print(pd.DataFrame(results).to_string(index=False));print('Negativo',np.mean(neg),'tempo',time.time()-start,flush=True)

def plots(m,store,results,preds,trees):
 fig,axs=plt.subplots(1,2,figsize=(13,5),constrained_layout=True)
 for ax,noise in zip(axs,CFG['ruido']):
  rows=pd.DataFrame(results);tab=rows[(rows.ruido==noise)&(rows.regime=='teste')];ax.barh(tab.assinatura,tab.acuracia);ax.axvline(.2,color='gray',linestyle='--');ax.set_xlim(0,1);ax.set_title(noise);ax.set_xlabel('Acurácia em 200 mecanismos novos')
 fig.savefig(O/'comparacao.png',dpi=160);plt.close(fig)
 fig,axs=plt.subplots(1,2,figsize=(11,5),constrained_layout=True)
 for ax,reg in zip(axs,['teste','shift']):
  ix=(m.regime==reg)&(m.ruido=='binomial1000');cm=confusion_matrix(m.familia[ix],preds[('binomial1000',reg,'arvore')]);ax.imshow(cm,cmap='Blues',vmin=0,vmax=40)
  for i in range(5):
   for j in range(5):ax.text(j,i,str(cm[i,j]),ha='center',va='center',color='black')
  ax.set_xticks(range(5),range(5));ax.set_yticks(range(5),range(5));ax.set_xlabel('Família prevista');ax.set_ylabel('Família verdadeira');ax.set_title(reg+' — árvore, com ruído')
 fig.savefig(O/'confusao.png',dpi=160);plt.close(fig)
 # PCA apenas ilustração: ajuste no treino, sem rótulos. A classificação usa a assinatura inteira.
 tr=(m.regime=='treino')&(m.ruido=='exato');te=(m.regime=='teste')&(m.ruido=='exato');sc=StandardScaler().fit(store['arvore'][tr]);pc=PCA(3).fit(sc.transform(store['arvore'][tr]));z=pc.transform(sc.transform(store['arvore'][te]))
 fig=plt.figure(figsize=(9,7));ax=fig.add_subplot(projection='3d')
 for family in range(5):
  a=z[m.familia[te].values==family];ax.scatter(*a.T,label=f'{family}: {CFG["familias"][family]}',s=14,alpha=.7)
 ax.set_xlabel('Componente 1');ax.set_ylabel('Componente 2');ax.set_zlabel('Componente 3');ax.set_title(f'Visualização apenas: 3D retém {pc.explained_variance_ratio_.sum():.1%} da variância');ax.legend(fontsize=7);fig.savefig(O/'assinatura_3d.png',dpi=160,bbox_inches='tight');plt.close(fig)
 (O/'pca.json').write_text(json.dumps({'variancia_explicada':pc.explained_variance_ratio_.tolist()}))
 # Árvores anotadas: altura ilustrativa, rótulos de transformação e resíduo.
 fig,axs=plt.subplots(5,1,figsize=(13,17),constrained_layout=True)
 for f,ax in enumerate(axs):
  tree=trees[str(f)];nodes=tree['nodes'];pos={};leaves=[]
  def visit(i):
   node=nodes[i]
   if not node['children']:leaves.append(i);return
   for c in node['children']:visit(c)
  visit(20)
  for x,i in enumerate(leaves):pos[i]=(x,0)
  for node in nodes[11:]:
   i,j=node['children'];xx=(pos[i][0]+pos[j][0])/2;yy=1+max(pos[i][1],pos[j][1]);pos[node['id']]=(xx,yy)
   for child in [i,j]:ax.plot([pos[child][0],pos[child][0],xx],[pos[child][1],yy,yy],color='#64748b',lw=1)
   ratio=node['cost']/max(node['before'],1e-10);ax.text(xx,yy+.05,f'{TN[node["best"]]} | r={ratio:.2f}',ha='center',fontsize=7,bbox=dict(facecolor='white',edgecolor='none',alpha=.8))
  ax.set_xticks(range(11),[tree['labels'][i] for i in leaves]);ax.set_yticks([]);ax.set_ylim(-.2,max(v[1] for v in pos.values())+1);ax.set_title(f'{f}: {CFG["familias"][f]} — nós indicam transformação comum e fração residual r',fontsize=10)
 fig.savefig(O/'arvores.png',dpi=150);plt.close(fig)
if __name__=='__main__':run()
