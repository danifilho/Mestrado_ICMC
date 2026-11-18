# Adaptadores (classificação binária) para IF, iRF e RF. Derivados dos adaptadores auditados do
# benchmark e do piloto anterior; configurações em configs/metodos.json.
suppressPackageStartupMessages({ library(jsonlite); library(data.table) })
df_xy <- function(X, y = NULL) { d <- as.data.frame(X); if (!is.null(y)) d$y <- y; d }
agora <- function() proc.time()[["elapsed"]]
escrever <- function(df, p) fwrite(as.data.frame(df), p)

# ---------------- Random Forest (ranger): referência preditiva e controle de importância individual
ajustar_rf <- function(X, y, cfg, semente) {
  suppressPackageStartupMessages(library(ranger))
  fit <- ranger(dependent.variable.name = "y", data = df_xy(X, factor(y, levels = c(0, 1))), num.trees = cfg$num_trees,
                probability = TRUE, num.threads = 1, seed = semente, verbose = FALSE)
  list(fit = fit, info = list(num_trees = fit$num.trees, mtry = fit$mtry, min_node_size = fit$min.node.size,
                              versao = as.character(packageVersion("ranger"))))
}
prever_rf <- function(fit, Xn) as.numeric(predict(fit$fit, data = df_xy(Xn), num.threads = 1)$predictions[, "1"])

# AP sem dependências (empates tratados como no sklearn: por limiar distinto)
ap <- function(y, s) {
  o <- order(-s); y <- y[o]; s <- s[o]
  fim <- c(which(diff(s) != 0), length(s))
  tp <- cumsum(y)[fim]; fp <- fim - tp
  prec <- tp / (tp + fp); rec <- tp / sum(y)
  sum(diff(c(0, rec)) * prec)
}
# Importância por permutação na VALIDAÇÃO (queda de AP), R repetições
extrair_rf <- function(fit, X, y, cfg, semente, saida, Xval, yval) {
  set.seed(semente)
  base <- ap(yval, prever_rf(fit, Xval))
  R <- cfg$repeticoes_permutacao
  imp <- vapply(colnames(Xval), function(v) {
    base - mean(vapply(seq_len(R), function(r) { Xp <- Xval; Xp[, v] <- Xp[sample.int(nrow(Xp)), v]; ap(yval, prever_rf(fit, Xp)) }, 0.0))
  }, 0.0)
  escrever(data.frame(atributo = colnames(Xval), queda_ap = imp), file.path(saida, "rf_importancia_permutacao_validacao.csv"))
  list(status = "ok", ap_base_validacao = base, repeticoes = R)
}

# ---------------- Interaction Forests (diversityForest 0.6.0)
ajustar_if <- function(X, y, cfg, semente) {
  suppressPackageStartupMessages(library(diversityForest))
  args <- list(dependent.variable.name = "y", data = df_xy(X, factor(y, levels = c(0, 1))), importance = cfg$importance,
               probability = TRUE, num.threads = 1, seed = semente, verbose = FALSE)
  if (!is.null(cfg$num_trees)) args$num.trees <- cfg$num_trees
  fit <- do.call(interactionfor, args)
  list(fit = fit, info = list(num_trees = fit$num.trees, npairs = fit$npairs, min_node_size = fit$min.node.size,
                              importance_mode = fit$importance.mode, n_amostra = nrow(X),
                              floresta_previsao_separada = nrow(X) > 1000,
                              versao = as.character(packageVersion("diversityForest"))))
}
prever_if <- function(fit, Xn) {
  p <- predict(fit$fit, data = df_xy(Xn), num.threads = 1, verbose = FALSE)$predictions
  as.numeric(if (is.null(dim(p))) p else p[, "1"])
}
extrair_if <- function(fit, X, y, cfg, semente, saida, ...) {
  f <- fit$fit
  par <- function(v) if (is.null(v)) NULL else data.frame(rotulo = names(v), valor = as.numeric(v))
  for (nm in c("quant", "qual", "univ")) {
    d <- par(f[[paste0("eim.", nm)]])
    if (!is.null(d)) escrever(d, file.path(saida, paste0("eim_", nm, ".csv")))
  }
  list(status = if (is.null(f$eim.quant)) "sem EIM" else "ok", n_quant = length(f$eim.quant), n_qual = length(f$eim.qual),
       nota = "n > 1000: EIM numa floresta de profundidade restrita (simplify.large.n) e previsão numa segunda floresta (padrão do pacote)")
}

# ---------------- iRF 2.0.0 (configuração de enhancer.R dos autores)
ajustar_irf <- function(X, y, cfg, semente) {
  lib <- Sys.getenv("IRF2_LIB", "/CAMINHO/HPCC/bench_Rlib_irf2")
  suppressPackageStartupMessages(library(iRF, lib.loc = lib))
  stopifnot(as.character(packageVersion("iRF", lib.loc = lib)) == "2.0.0")
  set.seed(semente)
  gp <- cfg$varnames_grp_json; if (!startsWith(gp, "/")) gp <- file.path(Sys.getenv("ESTUDO_RAIZ"), gp)
  grp <- fromJSON(gp)
  stopifnot(identical(names(grp), colnames(X)))
  t0 <- agora()
  fit <- NULL
  invisible(capture.output(fit <- suppressWarnings(iRF(x = X, y = factor(y, levels = c(0, 1)), n.iter = as.integer(cfg$n_iter),
    ntree = as.integer(cfg$ntree), n.core = 1L, interactions.return = as.integer(cfg$n_iter),
    n.bootstrap = as.integer(cfg$n_bootstrap), varnames.grp = unname(unlist(grp)),
    rit.param = list(depth = cfg$rit_depth, ntree = cfg$rit_ntree, nchild = cfg$rit_nchild, class.id = 1, class.cut = NULL),
    verbose = FALSE))))
  list(fit = fit, info = list(n_iter = cfg$n_iter, ntree = cfg$ntree, n_bootstrap = cfg$n_bootstrap,
                              mtry = fit$rf.list[[1]]$mtry, rit = cfg[grep("^rit_", names(cfg))], versao = "2.0.0",
                              nota = "o tempo de ajuste inclui a descoberta (30 bootstraps + RIT na iteração 5)"))
}
prever_irf <- function(fit, Xn) as.numeric(predict(fit$fit$rf.list[[length(fit$fit$rf.list)]], Xn, type = "prob")[, "1"])
extrair_irf <- function(fit, X, y, cfg, semente, saida, ...) {
  k <- as.integer(cfg$n_iter)
  st <- fit$fit$interaction[[k]]
  df <- if (length(st)) data.frame(interacao = names(st), estabilidade = as.numeric(st)) else data.frame(interacao = character(0), estabilidade = numeric(0))
  df$tamanho <- lengths(strsplit(df$interacao, "_"))
  escrever(df, file.path(saida, "irf_interacoes.csv"))
  w <- fit$fit$rf.list[[k]]$importance
  escrever(data.frame(atributo = rownames(w), mean_decrease_gini = as.numeric(w[, 1])), file.path(saida, "irf_importancia_iteracao_final.csv"))
  list(status = if (nrow(df)) "ok" else "lista vazia", n_conjuntos = nrow(df), n_pares = sum(df$tamanho == 2),
       n_ordem_superior = sum(df$tamanho > 2))
}
