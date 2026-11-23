# Reprodução da auditoria

Esta pasta contém testes técnicos, e não uma nova comparação de desempenho. Os testes não geram tabelas de acurácia, log-loss comparativa ou recuperação do par verdadeiro.

## Arquivos

- `CRITERIOS_ANTES_DOS_TESTES.md`: pergunta, recorte e regras anteriores às execuções técnicas; assinatura em `criterios_pre_teste.sha256`.
- `MATRIZ_DECISOES.csv` e `MAPA_CANDIDATOS.md`: inventário e decisões, incluindo lacunas.
- `FONTES_E_BUSCAS.md`: consultas, fontes e nível de leitura.
- `DECISOES.md`: instalações, correções e tentativas preservadas.
- `PROTOCOLO_NOVA_AVALIACAO.md`: desenho futuro, separado das verificações executadas.
- `codigo/auditar_R.R`: adaptadores e verificações de RF, IF, iRF, UFO, RLT e RPF.
- `codigo/auditar_python.py`: adaptador e verificações de EBM.
- `codigo/executar_auditoria.py`: processos com limite de tempo, preservando resultados existentes.
- `codigo/regua_comum.R`: perda logarítmica, permutação conjunta, contraste e tratamento de empates.
- `codigo/testar_regua.R`: dez verificações da régua e dos conjuntos de topo.
- `codigo/auditar_controles.R`: verificação do controle constante e da logística aditiva.
- `codigo/consolidar_auditoria.py`: produz as tabelas e o relatório de auditoria e custo.
- `resultados/`: JSON de verificações e logs de execução; `progress` registra o término do primeiro ajuste, não aprovação completa.
- `configs/cenarios_origem.json`: cópia do desenho anterior; `mtry=50` é metadado do piloto, não parâmetro imposto a todos os novos métodos.
- `configs/sementes_futuras.csv`: 2000 realizações planejadas, com 14000 sementes distintas. A geração dos dados científicos não foi executada.
- `fontes/wright/`: funções originais copiadas do material de reprodução preservado no projeto, sem alteração; vincular sua licença/proveniência antes de redistribuição externa integral.
- `CONGELAMENTO.json` e `MANIFEST.sha256`: estado de liberação e integridade dos arquivos documentais/código/outputs listados.

## Ambientes

R 4.5.0 local, com biblioteca adicional isolada em `ambiente/R`. A lista completa de versões é preservada em `ambiente/pacotes_R.csv`. Parte das dependências vem da biblioteca já existente do R; o ambiente não é um contêiner hermético. Python 3.10 em ambiente virtual com acesso aos pacotes-base existentes; `requirements_snapshot.txt` registra esse estado. A instalação em outra máquina deve recriar as versões e repetir a auditoria, não apenas confiar no hash dos scripts.

Implementações R: ranger 0.18.0; diversityForest 0.6.0; unityForest 0.2.0; RLT 3.2.6; iRF 3.0.0 no commit `e983ca1627a40cfcf4a147278184db18411f93f6`; randomPlantedForest 0.5.0.9000 no commit `4c9c28e3925f7ad04c161ffc32a85de239bfa86c`. EBM: interpret-core 0.7.8. Conferir versões efetivamente carregadas nos JSON; disponibilidade de pacote não equivale a teste aprovado.

Fontes oficiais: https://github.com/karlkumbier/iRF e https://github.com/PlantedML/randomPlantedForest; demais pacotes R via CRAN/arquivo, e EBM via distribuição oficial PyPI. Cópias de desenvolvimento mantidas localmente não serão incluídas por inteiro na publicação; os commits identificam os fontes.

O iRF exigiu compilação com Fortran instalado isoladamente. `ambiente/Makevars` contém caminhos locais e deve ser ajustado à máquina de destino. O comando de ligação recebeu um caminho de bibliotecas no binário com `install_name_tool`; os fontes permaneceram sem diferenças de Git. Não foi alterado o algoritmo para passar no teste.

## Executar

Com as versões instaladas na biblioteca apropriada e os interpretadores disponíveis:

```sh
Rscript codigo/testar_regua.R .
python codigo/executar_auditoria.py RF IF UFO RLT iRF RPF EBM
```

O executor presume que o ambiente Python foi criado em `ambiente/python`; para outro destino, ajustar o caminho em nova versão registrada. Resultados existentes são preservados e pulados; para repetir, arquivar a tentativa anterior em outro nome, registrando a razão. As tentativas ampliadas de timeout foram executadas separadamente e constam de `DECISOES.md`; o executor padrão permanece com 300 segundos.

As configurações usam uma thread onde a interface oferece essa opção. Não se comprovou igualdade entre execuções de uma e várias threads, nem portabilidade numérica entre sistemas operacionais. A auditoria mede repetibilidade na máquina e versão registradas. O custo foi medido com outros processos técnicos eventualmente ativos, não como benchmark controlado de velocidade.

## Auditoria versus confirmação

Sucesso em dados artificiais de engenharia comprova compatibilidade básica das interfaces e verificações listadas. Não comprova correção de toda a implementação, desempenho em todos os cenários, ausência de viés da medida ou validade biológica. O manifesto deve impedir que pendências sejam confundidas com uma seleção confirmatória finalizada.
