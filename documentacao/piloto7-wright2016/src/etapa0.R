# Etapa 0: executa as funções ORIGINAIS de Wright et al. (Arquivo adicional 3, 01_main_simulation: problems.R,
# simulate_snps.R e algorithms.R, sem modificação) para um bloco de repetições de um desenho de dados.
# O BatchExperiments é substituído por um array SLURM; cada repetição gera UM conjunto de dados, usado por todas as
# medidas e valores de mtry (como no BatchExperiments, em que a instância do problema depende só do desenho e da
# repetição). Sementes: dados = semente_base + 1000 * desenho + repetição; cada medida reinicia o gerador com
# semente dos dados + 100 * índice da medida + mtry.
# Uso: Rscript src/etapa0.R tarefa.json  (variáveis: PPI_LIB = biblioteca com o ranger 0.1.6.33 do Arquivo adicional 1)
a <- commandArgs(TRUE); T <- jsonlite::fromJSON(a[1])
.libPaths(c(Sys.getenv("PPI_LIB"), Sys.getenv("RFSRC_LIB"), .libPaths()))  # ranger 0.1.6.33 (PPI) e randomForestSRC 3.4.1
# Compatibilidade (D6): no ranger 0.1.6.33 o método importance.ranger é exportado mas não registrado como S3; desde o
# R 3.6 ele não é achado pelo caminho de busca. Registrá-lo não altera nenhum cálculo.
suppressPackageStartupMessages(library(ranger))
registerS3method("importance", "ranger", ranger::importance.ranger, envir = asNamespace("ranger"))
cod <- file.path(Sys.getenv("P7_RAIZ"), "fontes", "codigo_autores", "replication", "01_main_simulation")
for (f in c("simulate_snps.R", "problems.R", "algorithms.R")) source(file.path(cod, f))
# Compatibilidade (D6): no randomForestSRC 3.4.1, find.interaction ordena as variáveis por importância (sorted = TRUE),
# e o jmst_wrapper dos autores monta o nome do par na ordem da matriz; se interactionSNP2 vier antes de interactionSNP1,
# o nome "interactionSNP1:interactionSNP2" não existe e o posto vira NA. Com sorted = FALSE a matriz segue xvar.names.
# A JMST usa a média das duas direções e a JVIMP usa |Difference| por par: nenhum valor muda, só a ordem das linhas.
find.interaction <- function(...) randomForestSRC::find.interaction(..., sorted = FALSE)
if (isTRUE(T$rng_rounding)) suppressWarnings(RNGkind(sample.kind = "Rounding"))
info_ranger <- as.character(packageVersion("ranger")); info_rfsrc <- as.character(packageVersion("randomForestSRC"))
alg <- c(impurity = "impurity_wrapper", permutation = "permutation_wrapper", jvimp = "jvimp_wrapper",
         jmst = "jmst_wrapper", pairwise = "pairwise_wrapper")
dir.create(T$saida, recursive = TRUE, showWarnings = FALSE)
out <- list()
for (r in T$repeticoes) {
  arq <- file.path(T$saida, sprintf("rep%03d.csv", r))
  if (file.exists(arq)) next
  sd <- T$semente_base + 1000L * T$desenho + r
  set.seed(sd)
  dat <- simulate_data(NULL, n = T$n, prop_cases = 0.5, num_effect_snps = T$num_effect_snps, num_noise_snps = T$num_noise_snps,
                       maf_interaction = T$maf_interaction, maf_effect = T$maf_effect, maf_noise = NA, model = T$model,
                       beta = T$beta, beta_effect = T$beta_effect)
  linhas <- list()
  for (m in T$mtry) for (i in seq_along(T$medidas)) {
    med <- T$medidas[i]
    set.seed(sd + 100L * i + m)
    t0 <- proc.time()[["elapsed"]]
    erro <- ""
    rk <- tryCatch(as.numeric(get(alg[[med]])(NULL, dat, num_trees = 500, num_threads = 1, mtry = m)),
                   error = function(e) { erro <<- conditionMessage(e); NA_real_ })
    linhas[[length(linhas) + 1]] <- data.frame(desenho = T$desenho, model = T$model, beta = T$beta, beta_effect = T$beta_effect,
      maf_interaction = T$maf_interaction, maf_effect = T$maf_effect, repeticao = r, semente_dados = sd, mtry = m, algo = med,
      rank = rk, segundos = proc.time()[["elapsed"]] - t0, prop_casos = mean(dat$pheno == "1"),
      ranger = info_ranger, randomForestSRC = info_rfsrc, erro = erro)
  }
  data.table::fwrite(do.call(rbind, linhas), arq)
}
cat("ok\n")
