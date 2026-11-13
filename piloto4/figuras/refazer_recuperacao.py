from pathlib import Path
import pandas as pd,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
P=Path(__file__).parent;R=P.parent/'resultados'
s=pd.read_csv(R/'resumo_por_condicao.csv');a=pd.read_csv(R/'estabilidade_assinaturas.csv')
names={'aditivo':'Aditivo','curva_global':'Curva global','modulos':'Módulos separados','aninhado':'Módulos aninhados','sobreposto':'Grupos sobrepostos','curva_fora_banco':'Curva fora do banco'}
plt.rcParams.update({'font.size':11,'axes.spines.top':False,'axes.spines.right':False})
fig,axs=plt.subplots(1,2,figsize=(14,5.8),layout='constrained')
for fam in ['modulos','aninhado']:
 for n in [100,250]:
  g=s[(s.family==fam)&(s.ntrain==n)];axs[0].plot(g.noise,g.recovery,marker='o',label=f'{names[fam]}, treino={n}')
axs[0].set(title='A · Recuperação pelas árvores de expressão',ylim=(-.03,1.06),xlabel='Ruído / desvio-padrão da função',ylabel='Proporção de agrupamentos corretos');axs[0].legend(loc='lower left',fontsize=9)
g=a[a.trials>0].groupby(['family','trials']).rf_vs_exact.mean().unstack().reindex(list(names))
x=np.arange(6)
axs[1].bar(x-.18,g[200],width=.36,label='200 ensaios por célula',color='#6b9caf');axs[1].bar(x+.18,g[1000],width=.36,label='1.000 ensaios por célula',color='#dca75b')
axs[1].set(title='B · Instabilidade da árvore de componentes',ylim=(0,1.13),ylabel='Distância à árvore dos dados exatos',xticks=x,xticklabels=list(names.values()))
axs[1].tick_params(axis='x',labelrotation=28)
for label in axs[1].get_xticklabels():label.set_ha('right')
axs[1].legend(loc='upper left',fontsize=9,ncol=1)
fig.supxlabel('Os painéis avaliam árvores diferentes. Em B: 0 = mesmas ramificações; 1 = nenhum agrupamento interno em comum.',fontsize=10)
fig.savefig(P/'recuperacao_estabilidade_explicada.png',dpi=170);plt.close(fig)
