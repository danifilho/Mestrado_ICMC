import json,hashlib,csv
from pathlib import Path
root=Path(__file__).resolve().parents[1]
methods=['RF','IF','iRF','RPF','UFO','RLT','EBM']
registry={}
for m in methods:
 for n in [120,1000]:
  d=json.loads((root/'resultados'/f'{m}_{n}.json').read_text())
  assert d['status']=='PASS',(m,n,d['status'])
  assert all(d['checks'].values())
 registry[m]={k:d[k] for k in ['version','config']}
assert all(json.loads((root/'resultados/testes_regua.json').read_text()).values())
assert json.loads((root/'resultados/CONTROLES.json').read_text())['status']=='PASS'
assert all((root/'resultados'/f'{m}_cost.json').exists() for m in methods)
(root/'configs/modelos_auditados.json').write_text(json.dumps(registry,indent=2,ensure_ascii=False)+'\n')
freeze={'version':'1.0','date':'2026-11-23','status':'DOCUMENTACAO_E_SELECAO_OPERACIONAL_CONGELADAS',
 'scientific_evaluation_authorized':False,'scientific_evaluation_executed':False,
 'selected_models':methods,'scope':'coorte operacional delimitada; mapeamento dirigido não exaustivo',
 'technical_checks':{'method_size_cases':14,'checks_per_case':8,'gauge_checks':10,'control_checks':5},
 'release_conditions':['Definir teto a partir da estimativa e do perfil na infraestrutura escolhida, mantendo a prioridade pelos padrões dos autores.',
 'Integrar e testar o adaptador do gerador, a aplicação completa da régua e o código de análise antes dos dados científicos.',
 'Confirmar que novos ajustes mantêm versões e configurações aqui fixadas; mudanças exigem nova versão anterior à avaliação.'],
 'literature_limitations':['GUIDE, RIF, SNPInterForest e demais candidatos não auditados não foram declarados inferiores nem inexistentes.','Esta seleção não pretende representar estatisticamente todos os métodos arbóreos.'],
 'historical_results_known':True,'note':'Congelamento prospectivo para a versão documental; não é pré-registro retrospectivo do Piloto 7.'}
(root/'CONGELAMENTO.json').write_text(json.dumps(freeze,indent=2,ensure_ascii=False)+'\n')
files=[]
for p in sorted(root.rglob('*')):
 if not p.is_file():continue
 rel=p.relative_to(root)
 if rel.name in ['MANIFEST.sha256'] or '__pycache__' in rel.parts:continue
 if rel.parts[0]=='ambiente':
  if rel.name not in ['pacotes_R_versoes.csv','requirements_snapshot.txt','session_final.txt']:continue
 elif rel.parts[0]=='fontes':
  if rel.parts[1] not in ['wright','MATRIZ_ANTERIOR_NAO_REVALIDADA.csv']:continue
 elif rel.parts[0]=='resultados':
  if p.suffix!='.json':continue
 files.append(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {rel.as_posix()}')
(root/'MANIFEST.sha256').write_text('\n'.join(files)+'\n')
print(f'{len(files)} arquivos congelados; liberação científica = false')
