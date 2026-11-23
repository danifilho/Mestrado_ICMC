import subprocess,sys,json,time
from pathlib import Path
root=Path(__file__).resolve().parents[1]
methods=sys.argv[1:] or ['RF','IF','UFO','RLT','iRF','RPF','EBM']
for method in methods:
 for n in [120,1000]:
  out=root/'resultados'/f'{method}_{n}.json'
  if out.exists():continue
  cmd=([str(root/'ambiente/python/bin/python'),str(root/'codigo/auditar_python.py'),str(root),str(n)] if method=='EBM' else ['Rscript',str(root/'codigo/auditar_R.R'),str(root),method,str(n)])
  with (root/'resultados'/f'{method}_{n}.log').open('w') as f:
   try:
    run=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,timeout=300)
    if not out.exists():out.write_text(json.dumps({'method':method,'n':n,'status':'PROCESS_ERROR','returncode':run.returncode}))
   except subprocess.TimeoutExpired:out.write_text(json.dumps({'method':method,'n':n,'status':'TIMEOUT','limit_seconds':300}))
  print(out.name,out.read_text()[:100],flush=True)
