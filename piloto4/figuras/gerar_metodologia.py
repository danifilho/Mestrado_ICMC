from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch,FancyArrowPatch
P=Path(__file__).parent
plt.rcParams['font.family']='DejaVu Sans'
fig=plt.figure(figsize=(14,15),facecolor='#f6f8fa');ax=fig.add_axes([0,0,1,1]);ax.set(xlim=(0,100),ylim=(0,108));ax.axis('off')
navy='#163349';muted='#526372';blue='#24698f';teal='#217c73'
def text(x,y,s,size=13,weight='normal',color=navy,ha='left',va='top'):
 return ax.text(x,y,s,fontsize=size,fontweight=weight,color=color,ha=ha,va=va,linespacing=1.45)
def box(x,y,w,h,title,body,color=blue):
 ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.5,rounding_size=1',facecolor='white',edgecolor='#cad4dd',linewidth=1.15))
 ax.plot([x+1,x+1],[y+1.3,y+h-1.3],color=color,lw=3)
 text(x+2.5,y+h-1.25,title,14,'bold',color);text(x+2.5,y+h-4.05,body,12.4,color=muted)
def arrow(x1,y1,x2,y2,color=muted):
 ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle='-|>',mutation_scale=15,color=color,linewidth=1.3,connectionstyle='arc3'))
text(4,105,'PILOTO 4  /  MAPA COMPLETO DA METODOLOGIA',11,'bold',blue)
text(4,102,'O que cada árvore consegue recuperar?',25,'bold')
text(4,98,'Dois testes complementares. Nenhum deles identifica, por si só, um mecanismo biológico.',13,color=muted)
box(4,86,92,9,'BASE COMUM · 48 funções conhecidas, em seis famílias',
 'Aditivo • curva global • módulos separados • módulos aninhados • grupos sobrepostos • curva fora do banco\n8 sorteios de parâmetros por família · 4 variáveis × 5 níveis → 625 combinações por função',navy)
arrow(34,85.5,26,82);arrow(66,85.5,74,82)
text(4,82,'A / ÁRVORES QUE CALCULAM A RESPOSTA',13,'bold',blue)
text(52,82,'B / ÁRVORES QUE RESUMEM INTERAÇÕES',13,'bold',teal)
box(4,68.5,44,11,'1. Criar observações',
 'Ruído gaussiano: 0%, 5% ou 15% do desvio\npadrão da função. Três realizações por nível\nruidoso; uma observação sem ruído.',blue)
box(52,68.5,44,11,'1. Preparar uma resposta entre 0 e 1',
 'Padronizar cada função e aplicar a logística.\nObservar exatamente ou com ruído binomial:\n200 ou 1.000 ensaios por combinação.',teal)
arrow(26,68,26,66);arrow(74,68,74,66)
box(4,54.5,44,11,'2. Reservar combinações inteiras',
 'Treino: 100 ou 250 das 375 células disponíveis.\nValidação: 125 células. Teste: outras 125.\nAs células não se repetem entre conjuntos.',blue)
box(52,54.5,44,11,'2. Medir componentes em sete escalas',
 'Grid completo de 625 células; fANOVA uniforme.\nIdentidade, log, raiz, quadrado, inverso negativo,\nlogit e probit. Energia / variância de cada escala.',teal)
arrow(26,54,26,52);arrow(74,54,74,52)
box(4,40.5,44,11,'3. Ajustar e selecionar modelos',
 '17 candidatos de soma/tanh + índices livres\n+ ExtraTrees. Ajuste somente no treino.\nSeleção na validação: erro e parcimônia.',blue)
box(52,40.5,44,11,'3. Construir a árvore do piloto 3',
 'Folhas: 6 pares, 4 trios e 1 termo de ordem 4.\nUnir grupos pelo custo de compartilhar uma\ntransformação global. Fusão até uma única raiz.',teal)
arrow(26,40,26,38);arrow(74,40,74,38)
box(4,26.5,44,11,'4. Avaliar recuperação e previsão',
 'Grupos escolhidos × grupos do gerador.\nErro nas 125 células de teste × resposta exata.\nComparar estruturas corretas e incorretas\ncom o mesmo número de parâmetros.\nEstabilidade entre réplicas; bootstrap por gerador.',blue)
box(52,26.5,44,11,'4. Avaliar estabilidade dos agrupamentos',
 'Árvore exata × 4 repetições por ruído binomial.\nComparar agrupamentos internos, com os\nmesmos nomes de componentes. Distância:\n0 = iguais; 1 = nenhum grupo em comum.',teal)
text(4,24,'672 condições · 12.768 ajustes de candidatos',12,'bold',blue)
text(52,24,'432 tabelas · não prevê novas respostas',12,'bold',teal)
box(4,10,44,11,'CONTROLE ADICIONAL · otimização',
 'Após detectar limitações do ajuste livre:\n10 inícios e 500 avaliações, em 96 ajustes.\nResultados separados da rodada principal.\nConvergência não garante ótimo global.',blue)
box(52,10,44,11,'CONTROLE DE AMBIGUIDADE',
 '15 árvores binárias de somas + curva global.\nTodas produzem a mesma resposta.\nUm agrupamento interno exclusivo não pode\nser identificado nesse caso.',teal)
text(4,7.5,'LEITURA CONJUNTA',11,'bold',navy)
text(4,5.5,'A composição explícita pode ajudar a prever. A assinatura de componentes ainda é instável.',14,'bold')
text(4,2.8,'O elo pendente: uma árvore das interações que recupere explicações compartilhadas com estabilidade.',12,color=muted)
fig.savefig(P/'metodologia_piloto4.png',dpi=170,facecolor=fig.get_facecolor());fig.savefig(P/'metodologia_piloto4.svg',facecolor=fig.get_facecolor());plt.close(fig)
