# Etapa 1 (seção 5): mesmo desenho de dados de Wright et al., detectores atuais em R e régua global.
# Para cada repetição: treino = os MESMOS dados da Etapa 0 (semente 12345 + 1000·desenho + rep, problems.R original);
# teste independente do mesmo cenário e da mesma população (semente dos dados + 500000; MAFs de ruído do treino). Os dois conjuntos são gravados para a parte em Python.
# Detectores em R e ranking nativo entre os 21 pares dos 7 SNPs não ruidosos:
#   rf      ranger 0.18.0 (500 árvores, mtry do cenário, probabilidade) — modelo-base de H e Shapley
#   if_quant, if_qual  diversityForest::interactionfor (500 árvores, importance = "both"): EIM por par (máx. entre direções)
#   irf     iRF 3.0.0, signed = FALSE: estabilidade dos conjuntos de tamanho 2 (n.bootstrap = 30, int.return = n.iter)
#   sirf    iRF 3.0.0, signed = TRUE: estabilidade máxima entre as combinações de sinal do par
#   rpf     randomPlantedForest 0.2.1.9000, max_interaction = 2: variância do componente purificado do par no teste
#   h       hstats 1.2.2 sobre o rf: H² por par (normalizado), 7 variáveis
#   shap    treeshap 0.4.0 sobre o rf: média de |interação de Shapley| em 50 observações do teste
# Régua global (5.2) em cada modelo ajustado (rf, if, irf, rpf): no teste, 30 permutações compartilhadas;
#   I(A,B) = queda(A,B) − queda(A) − queda(B), com queda medida em log-loss (aumento) e em acurácia (redução).
#   h e shap herdam a régua do rf; sirf herda a do irf (mesma floresta de previsão).
# Uso: Rscript src/etapa1.R tarefa.json
a <- commandArgs(TRUE); T <- jsonlite::fromJSON(a[1])
suppressPackageStartupMessages({ library(data.table); library(ranger); library(diversityForest); library(iRF)
  library(randomPlantedForest); library(hstats); library(treeshap) })
raiz <- Sys.getenv("P7_RAIZ")
cod <- file.path(raiz, "fontes", "codigo_autores", "replication", "01_main_simulation")
for (f in c("simulate_snps.R", "problems.R")) source(file.path(cod, f))
V7 <- c("interactionSNP1", "interactionSNP2", paste0("effectSNP", 1:5))
PARES <- combn(V7, 2, FUN = paste, collapse = ":")
VERDADE <- "interactionSNP1:interactionSNP2"
agora <- function() proc.time()[["elapsed"]]
par_nome <- function(a, b) { i <- match(c(a, b), V7); paste(V7[sort(i)], collapse = ":") }
vazio <- setNames(rep(NA_real_, length(PARES)), PARES)

logloss <- function(y, p) { p <- pmin(pmax(p, 1e-15), 1 - 1e-15); -mean(y * log(p) + (1 - y) * log(1 - p)) }
acc <- function(y, p) mean((p > 0.5) == (y == 1))
regua <- function(prever, Xte, yte, perms) {
  b <- prever(Xte); base <- c(ll = logloss(yte, b), ac = acc(yte, b))
  queda <- function(cols) {
    m <- sapply(perms, function(o) { Xp <- Xte; Xp[, cols] <- Xte[o, cols]; p <- prever(Xp); c(logloss(yte, p), acc(yte, p)) })
    c(ll = mean(m[1, ]) - base[["ll"]], ac = base[["ac"]] - mean(m[2, ]))
  }
  ind <- sapply(V7, queda)
  out <- t(sapply(PARES, function(pr) { ab <- strsplit(pr, ":")[[1]]; q <- queda(ab); q - ind[, ab[1]] - ind[, ab[2]] }))
  list(base = base, I_ll = out[, "ll"], I_ac = out[, "ac"])
}

dir.create(T$saida, recursive = TRUE, showWarnings = FALSE)
ddir <- file.path(raiz, "resultados", "dados_etapa1", sprintf("d%02d", T$desenho)); dir.create(ddir, recursive = TRUE, showWarnings = FALSE)
# problems.R sorteia as MAFs dos 93 SNPs de ruído (runif) a cada chamada. O teste precisa vir da MESMA população do treino:
# capturamos as MAFs sorteadas no treino (mesmos sorteios de stats::runif, treino idêntico ao da Etapa 0) e o teste as reutiliza.
# (v0 gerava o teste com MAFs novas: deslocamento de distribuição nos SNPs de ruído; ver DECISOES D9.)
cap <- new.env()
sim_treino <- simulate_data; environment(sim_treino) <- list2env(list(runif = function(n, ...) { x <- stats::runif(n, ...); cap$maf <- x; x }),
  parent = environment(simulate_data))
sim_teste <- simulate_data; environment(sim_teste) <- list2env(list(runif = function(n, ...) cap$maf), parent = environment(simulate_data))
gerar <- function(sd, f) { set.seed(sd); f(NULL, n = 1000, prop_cases = 0.5, num_effect_snps = 5, num_noise_snps = 93,
  maf_interaction = T$maf_interaction, maf_effect = T$maf_effect, maf_noise = NA, model = T$model, beta = T$beta, beta_effect = T$beta_effect) }
# grava primeiro os dados de todas as repetições do bloco (a parte em Python depende deles)
for (r in T$repeticoes) {
  sd <- T$semente_base + 1000L * T$desenho + r
  ft <- file.path(ddir, sprintf("rep%03d_treino.csv.gz", r))
  if (!file.exists(ft)) { fwrite(gerar(sd, sim_treino), ft); fwrite(gerar(sd + 500000L, sim_teste), file.path(ddir, sprintf("rep%03d_teste.csv.gz", r))) }
}
for (r in T$repeticoes) {
  arq <- file.path(T$saida, sprintf("rep%03d.csv", r)); if (file.exists(arq)) next
  sd <- T$semente_base + 1000L * T$desenho + r
  tr <- as.data.frame(fread(file.path(ddir, sprintf("rep%03d_treino.csv.gz", r)))); te <- as.data.frame(fread(file.path(ddir, sprintf("rep%03d_teste.csv.gz", r))))
  tr$pheno <- factor(tr$pheno, levels = c(0, 1)); yte <- as.integer(te$pheno); Xtr <- tr[, -1]; Xte <- te[, -1]
  set.seed(sd + 900000L); perms <- lapply(1:30, function(q) sample.int(nrow(Xte)))
  linhas <- list(); tempos <- list(); bases <- list()
  add <- function(det, tipo, sc, modelo_regua) linhas[[length(linhas) + 1]] <<- data.table(detector = det, ranking = tipo, par = PARES,
    escore = as.numeric(sc[PARES]), modelo = modelo_regua)
  regua_add <- function(nome, prever, herdeiros) {
    t0 <- agora(); g <- regua(prever, Xte, yte, perms); tempos[[paste0("regua_", nome)]] <<- agora() - t0
    bases[[nome]] <<- g$base
    for (d in herdeiros) { add(d, "global_logloss", g$I_ll, nome); add(d, "global_acuracia", g$I_ac, nome) }
  }
  m <- T$mtry
  # --- RF (ranger) + H + Shapley
  t0 <- agora(); rf <- ranger(pheno ~ ., tr, num.trees = 500, mtry = m, probability = TRUE, num.threads = 1, seed = sd + 1L); tempos$rf <- agora() - t0
  prev_rf <- function(X) predict(rf, X, num.threads = 1)$predictions[, "1"]
  t0 <- agora(); h <- hstats(rf, X = Xtr, v = V7, pairwise_m = 7, n_max = 500, pred_fun = function(mm, x) predict(mm, x, num.threads = 1)$predictions[, "1"], verbose = FALSE)
  hp <- h2_pairwise(h, normalize = TRUE, squared = TRUE, zero = TRUE, top_m = 21)
  hv <- vazio; for (nm in rownames(hp)) { ab <- strsplit(nm, ":")[[1]]; hv[par_nome(ab[1], ab[2])] <- hp[nm, 1] }; tempos$h <- agora() - t0
  add("h", "nativo", hv, "rf")
  t0 <- agora(); u <- ranger.unify(rf, Xtr); set.seed(sd + 2L); io <- sample.int(nrow(Xte), 50)
  ts <- treeshap(u, Xte[io, ], interactions = TRUE, verbose = FALSE)$interactions
  sv <- vazio; for (pr in PARES) { ab <- strsplit(pr, ":")[[1]]; sv[pr] <- mean(abs(ts[ab[1], ab[2], ])) }; tempos$shap <- agora() - t0
  add("shap", "nativo", sv, "rf")
  regua_add("rf", prev_rf, c("rf", "h", "shap"))
  # --- IF
  t0 <- agora(); fi <- interactionfor(dependent.variable.name = "pheno", data = tr, importance = "both", num.trees = 500, probability = TRUE,
                                      num.threads = 1, seed = sd + 3L, verbose = FALSE); tempos$if_ <- agora() - t0
  eim <- function(v) { s <- vazio; for (nm in names(v)) { ab <- strsplit(gsub(" (large|small)", "", nm), " AND ")[[1]]
    if (all(ab %in% V7) && ab[1] != ab[2]) { k <- par_nome(ab[1], ab[2]); s[k] <- max(s[k], v[[nm]], na.rm = TRUE) } }; s }
  add("if_quant", "nativo", eim(fi$eim.quant), "if"); add("if_qual", "nativo", eim(fi$eim.qual), "if")
  prev_if <- function(X) { p <- predict(fi, data = X, num.threads = 1, verbose = FALSE)$predictions; if (is.null(dim(p))) p else p[, "1"] }
  regua_add("if", prev_if, c("if_quant", "if_qual"))
  # --- iRF e siRF (iRF 3.0.0)
  irf_est <- function(sig) {
    set.seed(sd + 4L)
    f <- iRF(x = as.matrix(Xtr), y = tr$pheno, ntree = 500, mtry = m, n.iter = 5, int.return = 5, n.bootstrap = 30, signed = sig,
             n.core = 1, verbose = FALSE)
    it <- f$interaction; s <- setNames(rep(0, length(PARES)), PARES)  # par não retornado = estabilidade 0 (empate no fim)
    if (!is.null(it) && nrow(it)) for (i in seq_len(nrow(it))) {
      ab <- strsplit(gsub("[+-]", "", it$int[i]), "_")[[1]]
      if (length(ab) == 2 && all(ab %in% V7) && ab[1] != ab[2]) { k <- par_nome(ab[1], ab[2]); s[k] <- max(s[k], it$stability[i], na.rm = TRUE) }
    }
    list(f = f, s = s)
  }
  t0 <- agora(); fr <- irf_est(FALSE); tempos$irf <- agora() - t0; add("irf", "nativo", fr$s, "irf")
  t0 <- agora(); fs <- irf_est(TRUE); tempos$sirf <- agora() - t0; add("sirf", "nativo", fs$s, "irf")
  rfk <- fr$f$rf.list; prev_irf <- function(X) as.numeric(predict(rfk, as.matrix(X), type = "prob")[, "1"])
  regua_add("irf", prev_irf, c("irf", "sirf"))
  # --- RPF
  t0 <- agora(); set.seed(sd + 5L); rp <- rpf(x = Xtr, y = tr$pheno, max_interaction = 2, purify = FALSE, parallel = FALSE); tempos$rpf <- agora() - t0
  prev_rpf <- function(X) as.numeric(predict(rp, new_data = X, type = "prob")$.pred_1)
  regua_add("rpf", prev_rpf, "rpf")
  t0 <- agora(); purify(rp); pc <- predict_components(rp, new_data = Xte, max_interaction = 2)$m
  rv <- vazio; for (pr in PARES) { ab <- strsplit(pr, ":")[[1]]; nm <- intersect(c(paste(ab, collapse = ":"), paste(rev(ab), collapse = ":")), colnames(pc))
    rv[pr] <- if (length(nm)) var(pc[[nm[1]]]) else 0 }; tempos$rpf_componentes <- agora() - t0
  add("rpf", "nativo", rv, "rpf")
  # --- saída
  L <- rbindlist(linhas)
  L[, posto := frank(-escore, ties.method = "average", na.last = "keep"), by = .(detector, ranking)]
  L[, posto_abs := frank(-abs(escore), ties.method = "average", na.last = "keep"), by = .(detector, ranking)]
  L[, posto_neg := frank(escore, ties.method = "average", na.last = "keep"), by = .(detector, ranking)]
  L[, `:=`(desenho = T$desenho, model = T$model, beta = T$beta, beta_effect = T$beta_effect, maf_interaction = T$maf_interaction,
           maf_effect = T$maf_effect, mtry = m, repeticao = r, semente_dados = sd, verdadeiro = par == VERDADE)]
  fwrite(L, arq)
  fwrite(data.table(repeticao = r, modelo = names(bases), logloss = sapply(bases, `[[`, "ll"), acuracia = sapply(bases, `[[`, "ac")),
         file.path(T$saida, sprintf("rep%03d_desempenho.csv", r)))
  writeLines(jsonlite::toJSON(lapply(tempos, round, 2), auto_unbox = TRUE), file.path(T$saida, sprintf("rep%03d_tempos.json", r)))
}
cat("ok\n")
