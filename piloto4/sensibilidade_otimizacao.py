"""Análise adicional após a rodada principal: 10 inícios e 500 avaliações.
Motivo: modelo de índices livres apresentou erro sem ruído mesmo em sua família.
Não sobrescreve a análise principal. Apenas 250 células, réplica 0, ruídos 0 e 0.15.
"""
import json,time
import numpy as np,pandas as pd
from piloto4 import CFG,OUT,FAMILIES,X,generate,fit,eval_free

def run():
 main=pd.read_csv(OUT/'previsao_resumo.csv');CFG['starts']=10;CFG['max_nfev']=500;rows=[];t=time.time()
 (OUT/'protocolo_sensibilidade.json').write_text(json.dumps(dict(post_hoc=True,motivo='erro sem ruido no modelo livre bem especificado; investigar otimizacao',starts=10,max_nfev=500,ntrain=250,noise=[0,.15],observation=0),indent=2))
 for fi,fam in enumerate(FAMILIES):
  for rep in range(CFG['geradores_por_familia']):
   seed=CFG['seed']+fi*1000+rep;f,truth,meta=generate(fam,seed);sd=f.std();r=np.random.default_rng(seed+100000);ix=r.permutation(625);tr=ix[:250];te=ix[500:]
   for noise in [0,.15]:
    rng=np.random.default_rng(seed+10000+int(noise*1000));y=f+rng.normal(0,noise*sd,625);p,success,nfev=fit(None,X[tr],y[tr],seed+17*100);pred=eval_free(p,X)[0]
    old=main[(main.family==fam)&(main.seed==seed)&(main.noise==noise)&(main.observation==0)&(main.ntrain==250)].iloc[0]
    rows.append(dict(family=fam,seed=seed,noise=noise,nmse_free_robust=np.mean((pred[te]-f[te])**2)/sd**2,nmse_free_original=old.nmse_free,nmse_tree=old.nmse_tree,success=success,nfev=nfev,train_mse=np.mean((pred[tr]-y[tr])**2)/sd**2))
  print('Sensibilidade',fam,'concluída',round(time.time()-t,1),flush=True)
 pd.DataFrame(rows).to_csv(OUT/'sensibilidade_otimizacao.csv',index=False)
if __name__=='__main__':run()
