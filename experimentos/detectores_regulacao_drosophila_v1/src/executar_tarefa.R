# Executa UMA tarefa (um ajuste). Uso: Rscript src/executar_tarefa.R tarefa.json
# Campos: id, metodo (if | irf | rf), semente, variante ("completo" | "reamostragem" | "permutacao" |
# "oficial"), indice (r01.., p01..), cfg, saida.
# - completo: treino agrupado inteiro; prevê validação e teste.
# - reamostragem: subamostra de grupos do treino (coluna de reamostragens_treino.csv); prevê validação e teste.
# - permutacao: treino inteiro com rótulos permutados por grupo (permutacoes_treino.csv).
# - oficial: partição oficial dos autores (análise secundária de reprodução); prevê o teste oficial.
# Nunca lê evidências biológicas.
a <- commandArgs(TRUE)
T <- jsonlite::fromJSON(a[1], simplifyVector = TRUE)
raiz <- Sys.getenv("ESTUDO_RAIZ")
source(file.path(raiz, "src", "metodos.R"))
setDTthreads(1)
D <- file.path(raiz, "data", "processed")
lerX <- function(p) { m <- as.matrix(fread(p)); storage.mode(m) <- "double"; m }
dir.create(T$saida, recursive = TRUE, showWarnings = FALSE)
info <- list(id = T$id, metodo = T$metodo, variante = T$variante, indice = T$indice, semente = T$semente, cfg = T$cfg,
             inicio = format(Sys.time(), "%Y-%m-%dT%H:%M:%S%z"), no = Sys.info()[["nodename"]], versao_R = R.version.string)
if (T$variante == "oficial") {
  sup <- fread(file.path(raiz, "data", "raw", "irfSuppData1.csv"))
  Xall <- as.matrix(sup[, -(1:5)]); storage.mode(Xall) <- "double"; yall <- sup$positive
  tr <- fread(file.path(D, "oficial_treino_linhas.csv"))$linha; te <- fread(file.path(D, "oficial_teste_linhas.csv"))$linha
  X <- Xall[tr, ]; y <- yall[tr]; prev <- list(teste_oficial = Xall[te, ])
  Xval <- NULL; yval <- NULL
} else {
  X <- lerX(file.path(D, "X_treino.csv")); y <- fread(file.path(D, "y_treino.csv"))$y
  Xval <- lerX(file.path(D, "X_validacao.csv")); yval <- fread(file.path(D, "y_validacao.csv"))$y
  if (T$variante == "reamostragem") {
    m <- fread(file.path(D, "reamostragens_treino.csv"))[[T$indice]] == 1
    X <- X[m, , drop = FALSE]; y <- y[m]
  } else if (T$variante == "permutacao") {
    y <- fread(file.path(D, "permutacoes_treino.csv"))[[T$indice]]
  }
  prev <- list(validacao = Xval, teste = lerX(file.path(D, "X_teste.csv")))
}
info$n_ajuste <- nrow(X); info$positivos_ajuste <- sum(y)
m <- T$metodo
t0 <- agora()
fit <- get(paste0("ajustar_", m))(X, y, T$cfg, T$semente)
info$segundos_treino <- agora() - t0
info$ajuste <- fit$info
info$segundos_previsao <- list()
for (nm in names(prev)) {
  t1 <- agora()
  p <- get(paste0("prever_", m))(fit, prev[[nm]])
  stopifnot(length(p) == nrow(prev[[nm]]), all(is.finite(p)))
  fwrite(data.table(previsao = p), file.path(T$saida, paste0("pred_", nm, ".csv")))
  info$segundos_previsao[[nm]] <- agora() - t1
}
dn <- file.path(T$saida, "nativo"); dir.create(dn, showWarnings = FALSE)
t2 <- agora()
if (!(m == "rf" && is.null(Xval)))
  info$extracao <- get(paste0("extrair_", m))(fit, X, y, T$cfg, T$semente, dn, Xval, yval)
info$segundos_extracao <- agora() - t2
info$memoria_R_mb <- sum(gc()[, 6])
info$status <- "ok"
info$fim <- format(Sys.time(), "%Y-%m-%dT%H:%M:%S%z")
writeLines(jsonlite::toJSON(info, auto_unbox = TRUE, null = "null", digits = NA, pretty = TRUE), file.path(T$saida, "info.json"))
