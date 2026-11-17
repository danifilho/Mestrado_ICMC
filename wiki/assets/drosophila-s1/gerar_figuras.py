"""Figuras da análise exploratória S1. Requer Python, numpy, pandas e matplotlib.
Executar: MPLCONFIGDIR=/tmp/mpl_s1 python gerar_figuras.py
Lê apenas snapshots locais; não ajusta modelos. Dados e referências: README.md.
"""
from pathlib import Path
import json, hashlib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from matplotlib.patches import FancyBboxPatch
R=Path(__file__).resolve().parent; D=R/'dados'; F=R/'figuras'; F.mkdir(exist_ok=True)
PAL={'escuro':'#14532D','medio':'#15803D','claro':'#86BF91','suave':'#E7F3E8','texto':'#18352B','neutro':'#E9ECE9','cinza':'#607269'}
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'text.color':PAL['texto'],'axes.labelcolor':PAL['texto'],'xtick.color':PAL['texto'],'ytick.color':PAL['texto'],'axes.spines.top':False,'axes.spines.right':False,'savefig.facecolor':'white'})
methods=['irf','if_quant','if_qual','ctrl_importancia','ctrl_correlacao']
labels=['iRF','IF quantitativo','IF qualitativo','Importância individual','Correlação']
short=['iRF','IF\nquantitativo','IF\nqualitativo','Controle:\nimportância individual','Controle:\ncorrelação']
s1=pd.read_csv(D/'tabela_S1.csv'); key=lambda a,b:tuple(sorted([a.lower(),b.lower()])); pairs=[key(*x.split('–')) for x in s1.par]
assert len(set(pairs))==20
counts=[]; ranks=np.full((20,5),np.nan)
for j,m in enumerate(methods):
 for seed in [2026,2027,2028]:
  df=pd.read_csv(D/'rankings'/f'{m}__completo_s{seed}.csv').sort_values('posicao')
  mp={key(r.tf_1,r.tf_2):r.posicao for r in df.itertuples()}
  if seed==2026:ranks[:,j]=[mp.get(p,np.nan) for p in pairs]
  for k in [5,10,20]:
   count=sum(mp.get(p,100000)<=k for p in pairs)
   counts.append({'lista':m,'semente':seed,'k':k,'recuperados_S1':count,'fracao_candidatos':count/k,'fracao_referencia':count/20})
C=pd.DataFrame(counts);C.to_csv(D/'recuperacao_S1.csv',index=False)
pd.DataFrame(ranks,index=s1.par,columns=methods).to_csv(D/'posicoes_S1_semente2026.csv',index_label='par')

def save(fig,name):
 fig.savefig(F/f'{name}.png',dpi=190,bbox_inches='tight');fig.savefig(F/f'{name}.svg',bbox_inches='tight');plt.close(fig)
def foot(fig,s):fig.text(.04,.015,s,fontsize=9,color=PAL['cinza'])
# 1: esquema sem texto cortado
fig,ax=plt.subplots(figsize=(12,4.5));ax.set_xlim(0,12);ax.set_ylim(0,4);ax.axis('off')
boxes=[('Dados','7.809 regiões de DNA\n80 preditores\nAtiva / não ativa'),('Ajuste','Treino: 4.658 regiões\nValidação: 1.545\nTeste: 1.606'),('Listas','IF quantitativo e qualitativo\niRF: pares retornados\nControles simples'),('Comparação','Dez primeiros candidatos\nversus 20 pares da S1\nTrês sementes')]
for i,(title,body) in enumerate(boxes):
 x=.15+i*3
 ax.add_patch(FancyBboxPatch((x,.9),2.65,2.1,boxstyle='round,pad=0.08',facecolor=PAL['suave'],edgecolor=PAL['medio'],linewidth=1.4))
 ax.text(x+1.325,2.55,title,ha='center',fontsize=14,weight='bold');ax.text(x+1.325,1.75,body,ha='center',va='center',fontsize=10.5,linespacing=1.7)
 if i<3:ax.annotate('',xy=(x+2.95,1.95),xytext=(x+2.72,1.95),arrowprops={'arrowstyle':'->','color':PAL['escuro'],'lw':2})
ax.text(.1,3.55,'Como foi feita a comparação exploratória',fontsize=17,weight='bold')
ax.text(6,.35,'Regiões sobrepostas ficam juntas. A S1 avalia as listas; não é usada no treinamento.',ha='center',fontsize=11)
save(fig,'01_desenho')
# 2: bars
fig,ax=plt.subplots(figsize=(11,5.7));x=np.arange(5)
for i,(seed,col,hatch) in enumerate(zip([2026,2027,2028],[PAL['escuro'],PAL['medio'],PAL['claro']],['','//','..'])):
 vals=[int(C[(C.lista==m)&(C.semente==seed)&(C.k==10)].recuperados_S1.iloc[0]) for m in methods]
 bars=ax.bar(x+(i-1)*.24,vals,.22,label=f'Semente {seed}',color=col,hatch=hatch,edgecolor=PAL['escuro'],linewidth=.5);ax.bar_label(bars,padding=3)
ax.set_xticks(x,short);ax.set_ylim(0,11);ax.set_yticks(range(11));ax.set_ylabel('Pares da S1 entre os 10 primeiros candidatos');ax.set_title('Correspondência com os 20 pares publicados',loc='left',weight='bold',pad=16);ax.legend(ncol=3,loc='upper left');ax.grid(axis='y',alpha=.15);ax.set_axisbelow(True)
foot(fig,'Inclui os quatro pares sem referência indicada na S1. Mesmos dados; três sementes.\nCorrespondência à lista publicada não equivale a acerto biológico.');fig.tight_layout(rect=(0,.1,1,1));save(fig,'02_recuperacao')
#3 matrix
fig,ax=plt.subplots(figsize=(10,10));states=np.where(np.isnan(ranks),0,np.where(ranks<=10,2,1))
ax.imshow(states,cmap=ListedColormap([PAL['neutro'],PAL['suave'],PAL['escuro']]),vmin=0,vmax=2,aspect='auto')
for i in range(20):
 for j in range(5):ax.text(j,i,'—' if np.isnan(ranks[i,j]) else str(int(ranks[i,j])),ha='center',va='center',color='white' if states[i,j]==2 else PAL['texto'])
unknown={'Gt–Med','Kr–Med','D–Gt','D–Twi'}
ax.set_yticks(range(20),[p+(' *' if p in unknown else '') for p in s1.par]);ax.set_xticks(range(5),['iRF','IF\nquantitativo','IF\nqualitativo','Importância\nindividual','Correlação']);ax.xaxis.tick_top();ax.tick_params(length=0)
ax.set_title('Onde aparecem os 20 pares da S1?\nPosições no ranking da semente 2026',loc='left',fontsize=15,pad=25)
for sp in ax.spines.values():sp.set_visible(False)
foot(fig,'Verde escuro: top 10. Verde claro: posição posterior. Cinza / —: par não retornado.\n* Sem referência bibliográfica indicada na S1 original; mantido na comparação.\nPosições empatadas seguem o desempate registrado no experimento.');fig.tight_layout(rect=(0,.10,1,1));save(fig,'03_posicoes')
#4 stability and agreement
E=pd.read_csv(D/'estabilidade.csv');Q=pd.read_csv(D/'concordancia.csv');E=E[E.k==10];Q=Q[Q.k==10]
fig,axs=plt.subplots(1,2,figsize=(14,6),gridspec_kw={'width_ratios':[1.05,1]})
for j,m in enumerate(methods):
 for source,mark,dy,color in [('reamostragens (dados)','o',-.12,PAL['escuro']),('sementes (algoritmo)','s',.12,PAL['claro'])]:
  r=E[(E.lista==m)&(E.fonte==source)].iloc[0]
  axs[0].errorbar(r.jaccard_media,j+dy,xerr=[[r.jaccard_media-r.jaccard_min],[r.jaccard_max-r.jaccard_media]],fmt=mark,color=color,mec=PAL['escuro'],ms=8,capsize=3,label=('Subamostras dos dados' if mark=='o' else 'Sementes') if j==0 else None)
axs[0].set_yticks(range(5),labels);axs[0].invert_yaxis();axs[0].set_xlim(-.02,1.03);axs[0].set_xlabel('Jaccard médio entre listas de dez pares');axs[0].set_title('O método repete suas escolhas?',loc='left',weight='bold');axs[0].legend(loc='lower left',fontsize=9);axs[0].grid(axis='x',alpha=.2)
M=np.full((5,5),np.nan)
for i,a in enumerate(methods):
 for j,b in enumerate(methods):
  if i==j:M[i,j]=E[(E.lista==a)&(E.fonte=='reamostragens (dados)')].jaccard_media.iloc[0]
  else:
   r=Q[((Q.lista_1==a)&(Q.lista_2==b))|((Q.lista_1==b)&(Q.lista_2==a))]
   M[i,j]=r.jaccard_mesma_reamostragem_media.iloc[0]
cm=LinearSegmentedColormap.from_list('verde',[ '#F4FAF4', PAL['claro'],PAL['escuro']])
im=axs[1].imshow(M,cmap=cm,vmin=0,vmax=1)
for i in range(5):
 for j in range(5):axs[1].text(j,i,f'{M[i,j]:.2f}',ha='center',va='center',weight='bold' if i==j else 'normal',color='white' if M[i,j]>.55 else PAL['texto'])
mini=['iRF','IF quant.','IF qual.','Importância','Correlação'];axs[1].set_xticks(range(5),mini,rotation=35,ha='right');axs[1].set_yticks(range(5),mini);axs[1].set_title('Os métodos concordam?',loc='left',weight='bold');fig.colorbar(im,ax=axs[1],fraction=.045,label='Jaccard@10')
foot(fig,'Barras à esquerda: mínimo–máximo, não intervalos de confiança.\nMatriz: diagonal = estabilidade entre subamostras; fora da diagonal = métodos na mesma subamostra.\nEsta figura compara listas entre si; não usa a S1 como gabarito.');fig.tight_layout(rect=(0,.13,1,1));save(fig,'04_estabilidade')
#5 predictive difference
P=pd.read_csv(D/'predicao_diferencas.csv');P=P[P.metrica=='AP'].copy()
fig,ax=plt.subplots(figsize=(9,4.5))
for i,r in enumerate(P.itertuples()):
 ax.errorbar(r.diferenca_media_sementes,i,xerr=[[r.diferenca_media_sementes-r.ic95_inf],[r.ic95_sup-r.diferenca_media_sementes]],fmt='o',color=PAL['escuro'],ms=9,capsize=5)
 ax.text(.016,i,f'{r.diferenca_media_sementes:+.3f}\n[{r.ic95_inf:+.3f}; {r.ic95_sup:+.3f}]',va='center',fontsize=10)
ax.set_yticks([0,1],['IF − RF','iRF − RF']);ax.invert_yaxis();ax.set_ylim(1.6,-.6);ax.axvline(0,color=PAL['cinza'],ls='--');ax.set_xlim(-.035,.032);ax.set_xlabel('Diferença de AP em relação ao Random Forest');ax.set_title('Previsão: nenhuma diferença demonstrada contra RF',loc='left',fontsize=13,weight='bold');ax.grid(axis='x',alpha=.15)
foot(fig,'Pontos: diferença das médias de três sementes. Barras: IC 95%, bootstrap pareado por grupo (2.000).\nAmbos os intervalos incluem zero. Isso não demonstra equivalência.');fig.tight_layout(rect=(0,.14,1,1));save(fig,'05_previsao')
(R/'paleta.json').write_text(json.dumps(PAL,indent=2)+'\n')
manifest={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(R.rglob('*')) if p.is_file() and p.name!='manifesto_sha256.json'}
(R/'manifesto_sha256.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(C[C.k==10].to_string(index=False))
