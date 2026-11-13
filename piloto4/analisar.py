"""Tabelas e figuras. Não altera dados, modelos ou critérios de seleção."""
import itertools,json
import numpy as np,pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from piloto4 import OUT,MODELS,FAMILIES
NAMES={'aditivo':'Aditivo','curva_global':'Curva global','modulos':'Módulos separados','aninhado':'Módulos aninhados','sobreposto':'Grupos sobrepostos','curva_fora_banco':'Curva fora do banco'}
COLS=['nmse_tree','nmse_flat','nmse_free','nmse_extra','nmse_oracle','nmse_wrong']
LABELS=['Árvore selecionada','Sem níveis aninhados','Dois índices livres','ExtraTrees','Estrutura verdadeira','Estrutura incorreta']
def run():
 s=pd.read_csv(OUT/'previsao_resumo.csv');a=pd.read_csv(OUT/'ajustes.csv');rows=[]
 for keys,g in s.groupby(['family','noise','ntrain']):
  r=dict(zip(['family','noise','ntrain'],keys));r.update(n=len(g),seeds=g.seed.nunique(),recovery=g.group_hit.mean(),non_tree_selected=g.non_tree_selected.mean(),ambiguous=g.ambiguous_topologies.mean())
  for col in COLS:r[col+'_mean']=g[col].mean();r[col+'_median']=g[col].median()
  rows.append(r)
 agg=pd.DataFrame(rows);agg.to_csv(OUT/'resumo_por_condicao.csv',index=False)
 # Reamostragem da unidade independente: parâmetros geradores (seed); não células ou réplicas.
 diff=[];rng=np.random.default_rng(119)
 for keys,g in s.groupby(['family','noise','ntrain']):
  for c1,c2 in [('nmse_flat','nmse_tree'),('nmse_free','nmse_tree'),('nmse_wrong','nmse_oracle')]:
   d=g.assign(delta=g[c1]-g[c2]).groupby('seed').delta.mean().dropna().values
   if len(d):
    b=np.array([rng.choice(d,len(d),replace=True).mean() for _ in range(2000)]);lo,hi=np.quantile(b,[.025,.975]);diff.append(dict(zip(['family','noise','ntrain'],keys))|dict(comparacao=c1+' - '+c2,mean=d.mean(),low=lo,high=hi,n=len(d)))
 pd.DataFrame(diff).to_csv(OUT/'diferencas_bootstrap_geradores.csv',index=False)
 groups={m['name']:{tuple(sorted(v)) for v in m['groups']} for m in MODELS};st=[]
 for keys,g in s[s.noise>0].groupby(['family','seed','noise','ntrain']):
  agreement=[];jac=[]
  for i,j in itertools.combinations(g.selected_tree,2):
   agreement.append(i==j);x,y=groups[i],groups[j];jac.append(len(x&y)/len(x|y) if x|y else 1.)
  st.append(dict(zip(['family','seed','noise','ntrain'],keys))|dict(agreement=np.mean(agreement),jaccard=np.mean(jac)))
 pd.DataFrame(st).to_csv(OUT/'estabilidade_expressoes.csv',index=False)
 # Falhas de convergência são mantidas e contabilizadas.
 conv=a.groupby(['family','model']).agg(fraction_converged=('success','mean'),n=('success','size'),median_nfev=('nfev','median')).reset_index();conv.to_csv(OUT/'convergencia.csv',index=False)
 sel=s.merge(a[['condition','model','success']],left_on=['condition','selected_tree'],right_on=['condition','model']);sel[['condition','success']].to_csv(OUT/'convergencia_selecionados.csv',index=False)
 plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
 fig,axs=plt.subplots(2,3,figsize=(14,8),constrained_layout=True)
 for fam,ax in zip(FAMILIES,axs.ravel()):
  g=agg[(agg.family==fam)&(agg.ntrain==250)];xx=np.arange(len(g));
  for c,l in zip(COLS[:4],LABELS[:4]):ax.plot(xx,np.maximum(g[c+'_mean'],1e-8),marker='o',label=l)
  ax.set_xticks(xx,[str(v) for v in g.noise]);ax.set_yscale('log');ax.set_title(NAMES[fam]);ax.set_xlabel('Ruído / desvio-padrão da função');ax.set_ylabel('Erro / variância da resposta')
 axs[0,0].legend(fontsize=8);fig.suptitle('Previsão de 125 combinações retidas • 250 células de treino\nMédia sobre 8 geradores; piso gráfico 10⁻⁸ (não um piso nos resultados)');fig.savefig(OUT/'previsao.png',dpi=160);plt.close(fig)
 fig,axs=plt.subplots(1,2,figsize=(11,4),constrained_layout=True)
 for fam in ['modulos','aninhado']:
  for n in [100,250]:
   g=agg[(agg.family==fam)&(agg.ntrain==n)];axs[0].plot(g.noise,g.recovery,marker='o',label=f'{NAMES[fam]}, n={n}')
 axs[0].set_ylim(-.03,1.05);axs[0].set_ylabel('Proporção de estruturas\nexatas recuperadas');axs[0].set_xlabel('Ruído relativo');axs[0].legend(fontsize=8)
 audit=pd.read_csv(OUT/'estabilidade_assinaturas.csv');h=audit[audit.trials>0].groupby(['family','trials']).rf_vs_exact.mean().unstack();h=h.reindex(FAMILIES);h.plot.bar(ax=axs[1],rot=30);axs[1].set_xticklabels([NAMES[v] for v in h.index],ha='right');axs[1].set_ylim(0,1);axs[1].set_title('Árvore de componentes do piloto 3');axs[1].set_ylabel('Distância topológica à versão exata\n0 = iguais; 1 = nenhum grupo interno em comum');axs[1].legend(title='Ensaios binomiais');fig.savefig(OUT/'recuperacao_estabilidade.png',dpi=160);plt.close(fig)
 print('PRINCIPAL, 250 células\n'+agg[agg.ntrain==250].to_string(index=False))
 print('Convergência todos:',a.success.mean(),'selecionados:',sel.success.mean())
 print('ESTABILIDADE EXPRESSÕES\n',pd.DataFrame(st).groupby(['family','noise','ntrain'])[['agreement','jaccard']].mean().to_string())
 print('AUDITORIA\n',audit.groupby(['family','trials'])[['rf_vs_exact','zero_regret_nodes','triple_clade_hit']].mean().to_string())
if __name__=='__main__':run()
