import csv,json,shutil,sys
from pathlib import Path
root=Path(__file__).resolve().parents[1]
src=Path(sys.argv[1]) if len(sys.argv)>1 else root/'fontes'
if not (src/'MATRIZ_SELECAO.csv').exists():
 src_file=root/'fontes/MATRIZ_ANTERIOR_NAO_REVALIDADA.csv'
else:
 src_file=src/'MATRIZ_SELECAO.csv'
if src_file.resolve()!=(root/'fontes/MATRIZ_ANTERIOR_NAO_REVALIDADA.csv').resolve():
 shutil.copy2(src_file,root/'fontes/MATRIZ_ANTERIOR_NAO_REVALIDADA.csv')
rows=list(csv.DictReader(src_file.open()))
main={'M01':'RF','M02':'IF','M03':'iRF','M07':'RPF','M09':'EBM','M24':'UFO','M26':'RLT'}
extract={'M04','M10','M11','M12','M13','M35','M36','M37','M38','M48','M49'}
general={'M29','M31'}
pending={'M27','M28','M39','M50','M55'}
updates={
'M01':('referencia','RF de Breiman como âncora histórica; não selecionado por resultado do piloto.'),
'M02':('elegivel','Preditor arbóreo com divisões bivariadas; EIM não é pré-requisito da régua.'),
'M03':('elegivel','Comparar a floresta da última iteração; RIT constitui leitura secundária.'),
'M07':('elegivel_software','Classificação logística sustentada pelo software auditado; registrar diferença para o artigo de regressão e para a versão antiga.'),
'M09':('elegivel','EBM é ajuste baseado em árvores com termos individuais e pares; não confundir com floresta de bagging.'),
'M24':('elegivel_preprint','Interações motivam otimização conjunta das raízes; preprint identificado, sem presumir VIM como ranking de pares.'),
'M26':('elegivel_software','Procedimento de reforço explicitamente ativado; suporte de classificação conferido no pacote; artigo e implementação não são versões intercambiáveis.'),
'M08':('controle_pendente','Ablação de ordem um; não representa outro algoritmo; exige teste próprio.'),
'M20':('extensao_recodificacao','Requer preditores binários para a busca lógica; recodificação 0/1/2 deve ser protocolada e permutada por SNP completo.'),
'M25':('pendente_classificacao','Implementação histórica simpleRSRF é de regressão; não converter sua saída em probabilidade por recorte; confirmar implementação binária antes de mudar status.'),
'M27':('pendente_implementacao','Resumo institucional do RIF de Guo e Lin confirmado; código dos autores não localizado nesta busca. Não confundir com outro RIF de biomarcadores.'),
'M28':('desmembrar_objetos','BART geral é referência ampliada; o artigo primário de DP-Forests formula regressão normal. Classificação nativa de DP-Forests não confirmada; não inferir do suporte binário de BART.'),
'M30':('fora_modelo_final','Regras originadas de árvores com ajuste final de coeficientes constituem outra classe operacional; escopo futuro possível.'),
'M39':('pendente_probabilidades','Árvores e detecção por restrição são pertinentes; documentação trabalha com modelo de regressão e critérios RMS/ROC; interface probabilística não verificada.'),
'M50':('pendente_acesso_implementacao','GUIDE é pertinente, inclusive classificação e florestas. Acesso ao manual oficial exigiu verificação interativa e o download oficial do binário expirou nesta consulta. Não auditaram-se probabilidades nem interface automatizada.'),
'M55':('pendente_acesso_implementacao','Artigo primário identifica o software SNPInterForest; endereço oficial indicado não ficou acessível nesta consulta. Não substituir por reimplementação própria.'),
'M51':('controle_pendente','Controle aditivo no logit, fora do estrato de competidores; implementação ainda não auditada nesta rodada.')}
out=[]
for r in rows:
 k=r['id'];status,reason=updates.get(k,('leitura_secundaria','Procedimento de leitura/inferência; não presumir novo preditor.') if k in extract else ('referencia_ampliada','Modelo generalista ou grupo heterogêneo; separar variantes antes de eventual inclusão.') if k in general else ('pendente_evidencia','Fonte original e implementação ainda não revalidadas para este recorte.') if k in pending else ('fora_recorte_primario','Inventário anterior: modelo não arbóreo ou pipeline externo à definição; decisão preliminar de triagem, sem alegação de revisão integral.'))
 tested=main.get(k);res={}
 if tested:
  for n in [120,1000]:
   f=root/'resultados'/f'{tested}_{n}.json'
   res[str(n)]=json.loads(f.read_text()).get('status') if f.exists() else 'PENDENTE'
 out.append(dict(id=k,candidato=r['nome_sigla'],decisao_cientifica=status,motivo=reason,teste_interface=res.get('120','NA'),teste_escala=res.get('1000','NA'),fonte=r['doi_url'],evidencia_atual='fonte/software consultados nesta auditoria' if k in main or k in {'M20','M30','M39','M50','M04'} else 'triagem a partir do inventário anterior; não revalidado integralmente'))
out.extend([
 dict(id='N01',candidato='LSSFind / Depth Weighted Prevalence',decisao_cientifica='leitura_secundaria',motivo='Recuperação de interações em ensemble sob modelo LSS; não contar automaticamente como novo preditor.',teste_interface='NA',teste_escala='NA',fonte='https://arxiv.org/abs/2102.11800',evidencia_atual='resumo primário'),
 dict(id='N02',candidato='Extra Trees',decisao_cientifica='referencia_ampliada',motivo='Referência generalista adicional; não implica mecanismo específico de detecção de pares. Nenhuma execução nesta rodada.',teste_interface='NA',teste_escala='NA',fonte='https://doi.org/10.1007/s10994-006-6226-1',evidencia_atual='candidato conhecido; artigo não revalidado nesta auditoria'),
 dict(id='N03',candidato='lo-siRF',decisao_cientifica='pendente_evidencia',motivo='Pipeline candidato; distinguir triagem, transformação da resposta, ajuste e extração antes de inclusão.',teste_interface='NA',teste_escala='NA',fonte='https://yu-group.github.io/epistasis-cardiac-hypertrophy/',evidencia_atual='candidato registrado; não revalidado nesta rodada')])
with (root/'MATRIZ_DECISOES.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=out[0].keys());w.writeheader();w.writerows(out)
lines=['# Mapa de candidatos e decisões','', 'Registro de 23/11/2026. Os 59 registros são objetos bibliográficos, variantes e controles, não 59 algoritmos independentes. O inventário antigo contém agrupamentos que precisam ser desmembrados. Não se declara revisão sistemática nem exaustividade.','', '| ID | Candidato | Decisão | Justificativa |','|---|---|---|---|']
for r in out:lines.append('|'+ '|'.join(r[x].replace('|','/') for x in ['id','candidato','decisao_cientifica','motivo'])+'|')
lines.extend(['','## Leitura das decisões','','O núcleo técnico examinado tem sete procedimentos, incluindo RF como referência. A auditoria desses sete não elimina automaticamente os demais elegíveis. GUIDE, RIF, variantes bayesianas voltadas a interação e pipelines com mudança de representação permanecem lacunas explícitas. A seleção final para uma nova avaliação depende de fechar essas decisões com a mesma regra; não se atribui inferioridade a métodos não executados.','','Uma escolha apenas entre pacotes prontamente integráveis é uma amostra de conveniência operacional. Ela pode sustentar um estudo delimitado, mas não a afirmação de que se comparou o universo dos métodos arbóreos.'])
(root/'MAPA_CANDIDATOS.md').write_text('\n'.join(lines)+'\n')
