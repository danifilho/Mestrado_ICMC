import sys,json,time,pickle,platform
from pathlib import Path
import numpy as np
from interpret.glassbox import ExplainableBoostingClassifier
import interpret
root=Path(sys.argv[1]);n=int(sys.argv[2]);p=8 if n==120 else 100
rng=np.random.default_rng(907321+n)
X=rng.integers(0,3,size=(n,p)); y=rng.permutation(np.resize([0,1],n));Z=X[:40].copy();before=X.copy()
cfg={'random_state':808031,'n_jobs':1,'interactions':'3x'}
t=time.monotonic()
try:
 m=ExplainableBoostingClassifier(**cfg).fit(X,y);fit_seconds=time.monotonic()-t
 pred=lambda model,z:model.predict_proba(z)[:,list(model.classes_).index(1)]
 if len(sys.argv)>3 and sys.argv[3]=='cost':
  pred(m,X);t0=time.monotonic()
  for j in range(10):
   xx=X.copy();xx[:,:2]=np.roll(X[:,:2],j+1,axis=0);pred(m,xx)
  (root/'resultados/EBM_cost.json').write_text(json.dumps({'method':'EBM','n':n,'p':p,'status':'PROFILED','fit_seconds':fit_seconds,'predict_1000_seconds':(time.monotonic()-t0)/10,'version':interpret.__version__},indent=2))
  sys.exit(0)
 pr=pred(m,Z);m2=ExplainableBoostingClassifier(**cfg).fit(X,y)
 checks={'probabilities':bool(np.isfinite(pr).all() and ((pr>=0)&(pr<=1)).all() and len(pr)==40),
 'same_seed':bool(np.allclose(pr,pred(m2,Z),rtol=0,atol=1e-12)),
 'serialization':bool(np.allclose(pr,pred(pickle.loads(pickle.dumps(m)),Z),rtol=0,atol=1e-12)),
 'row_order':bool(np.allclose(pr,pred(m,Z[::-1])[::-1],rtol=0,atol=1e-12)),
 'input_unchanged':bool(np.array_equal(X,before))}
 for name,cols in [('A',[0]),('B',[1]),('AB',[0,1])]:
  zz=Z.copy();zz[:,cols]=Z[::-1][:,cols];checks['permute_'+name]=bool(np.isfinite(pred(m,zz)).all())
 result={'status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,'fit_seconds':fit_seconds,'config':m.get_params(),'version':interpret.__version__}
except Exception as e:result={'status':'ERROR','error':repr(e)}
result.update(method='EBM',n=n,p=p,total_seconds=time.monotonic()-t,python=platform.python_version())
(root/'resultados'/f'EBM_{n}.json').write_text(json.dumps(result,indent=2))
