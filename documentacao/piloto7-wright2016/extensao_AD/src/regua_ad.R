# Extensão A–D do Piloto 7: modelos do núcleo em R (RF, IF, iRF, RPF) e régua comum pós-ajuste com valores POR PERMUTAÇÃO.
# Dados: os mesmos treino/teste da Etapa 1 corrigida (D9), lidos de ../resultados/dados_etapa1 (nada é regenerado).
# Permutações: lidas de extensao_AD/resultados/permutacoes (as mesmas para todos os modelos, sementes de ajuste, R e Python).
# Para cada modelo ajustado e cada conjunto C (7 SNPs isolados e 21 pares), grava a perda no teste original e após cada uma
# das 30 permutações: Δ_C = L(permutado) − L(original) (log-loss: aumento; acurácia: queda). Na permutação conjunta, a MESMA
# permutação de linhas vai às duas colunas. ΔA, ΔAB e I_AB = ΔAB − ΔA − ΔB são derivados na análise, não aqui.
# Semente de ajuste s (0 = histórica da Etapa 1; s > 0 = novas): semente do modelo = semente histórica + 1000003·s.
#   RF   ranger 0.18.0, 500 árvores, mtry 50, probabilidade, seed = sd + 1        nativo: H² (hstats, sobre o RF; secundário)
#   IF   diversityForest 0.6.0 interactionfor, 500 árvores, importance = "both", seed = sd + 3   nativo: EIM quant. e qual.
#   iRF  iRF 3.0.0, signed = FALSE, n.iter 5, n.bootstrap 30, set.seed(sd + 4)   nativo: estabilidade dos pares
#   RPF  randomPlantedForest 0.2.1.9000, max_interaction 2, set.seed(sd + 5)      nativo: variância do componente purificado (teste)
# Configurações idênticas às de src/etapa1.R (histórico). Previsão em lote: as 30 cópias permutadas do teste são empilhadas e
# previstas numa única chamada por conjunto (as previsões são linha a linha; a equivalência é conferida no modo validar).
# Modo validar (smoke test): (a) régua sem lote para 3 conjuntos do RF; (b) I com as permutações R históricas (sample.int após
# set.seed(sd + 900000)), comparável ao I gravado na Etapa 1.
# Uso: Rscript extensao_AD/src/regua_ad.R tarefa.json      (P7_RAIZ = raiz do Piloto 7)
a <- commandArgs(TRUE); T <- jsonlite::fromJSON(a[1])
suppressPackageStartupMessages({ library(data.table); library(ranger); library(diversityForest); library(iRF)
  library(randomPlantedForest); library(hstats) })
raiz <- Sys.getenv("P7_RAIZ"); EXT <- file.path(raiz, "extensao_AD")
V7 <- c("interactionSNP1", "interactionSNP2", paste0("effectSNP", 1:5))
PARES <- combn(V7, 2, FUN = paste, collapse = ":")
CONJ <- c(V7, PARES)
agora <- function() proc.time()[["elapsed"]]
par_nome <- function(a, b) { i <- match(c(a, b), V7); paste(V7[sort(i)], collapse = ":") }
vazio <- setNames(rep(NA_real_, length(PARES)), PARES)
s <- as.integer(T$semente_ajuste); OFF <- 1000003L * s
validar <- isTRUE(T$validar)
modelos <- if (is.null(T$modelos)) c("rf", "if", "irf", "rpf") else T$modelos

ll_vec <- function(y, p) { p <- pmin(pmax(p, 1e-15), 1 - 1e-15); -(y * log(p) + (1 - y) * log(1 - p)) }
ac_vec <- function(y, p) as.numeric((p > 0.5) == (y == 1))   # classe positiva = caso (pheno = 1); p = 0,5 conta como controle
digital <- function(P) sum(as.numeric(P) * as.numeric(row(P)) * as.numeric(col(P)))

perdas <- function(prever, Xte, yte, P, conjuntos = CONJ) {
  n <- nrow(Xte); Q <- ncol(P); b <- prever(Xte)
  out <- list(data.table(conjunto = "(original)", perm = 0L, logloss = mean(ll_vec(yte, b)), acuracia = mean(ac_vec(yte, b))))
  Xb <- Xte[rep(seq_len(n), Q), , drop = FALSE]; yb <- rep(yte, Q); bl <- rep(seq_len(Q), each = n); idx <- as.vector(P)
  for (cj in conjuntos) {
    cols <- strsplit(cj, ":")[[1]]; Xp <- Xb; Xp[, cols] <- Xte[idx, cols, drop = FALSE]; p <- prever(Xp)
    out[[length(out) + 1]] <- data.table(conjunto = cj, perm = seq_len(Q), logloss = as.numeric(tapply(ll_vec(yb, p), bl, mean)),
                                         acuracia = as.numeric(tapply(ac_vec(yb, p), bl, mean)))
  }
  list(tab = rbindlist(out), prev = b)
}
perdas_sem_lote <- function(prever, Xte, yte, P, conjuntos) {
  rbindlist(lapply(conjuntos, function(cj) { cols <- strsplit(cj, ":")[[1]]
    rbindlist(lapply(seq_len(ncol(P)), function(q) { Xp <- Xte; Xp[, cols] <- Xte[P[, q], cols, drop = FALSE]; p <- prever(Xp)
      data.table(conjunto = cj, perm = q, logloss = mean(ll_vec(yte, p)), acuracia = mean(ac_vec(yte, p))) })) }))
}
contraste <- function(tab) {  # I = queda(A,B) − queda(A) − queda(B), com quedas médias nas permutações (definição histórica)
  b <- tab[perm == 0]; m <- tab[perm > 0, .(ll = mean(logloss) - b$logloss, ac = b$acuracia - mean(acuracia)), by = conjunto]
  q <- setNames(m$ll, m$conjunto); qa <- setNames(m$ac, m$conjunto)
  rbindlist(lapply(PARES, function(pr) { ab <- strsplit(pr, ":")[[1]]
    data.table(par = pr, I_ll = q[[pr]] - q[[ab[1]]] - q[[ab[2]]], I_ac = qa[[pr]] - qa[[ab[1]]] - qa[[ab[2]]]) }))
}

saida <- file.path(EXT, T$saida); dir.create(saida, recursive = TRUE, showWarnings = FALSE)
ddir <- file.path(raiz, "resultados", "dados_etapa1", sprintf("d%02d", T$desenho))
pdir <- file.path(EXT, "resultados", "permutacoes", sprintf("d%02d", T$desenho))
for (r in T$repeticoes) {
  pre <- file.path(saida, sprintf("rep%03d_s%d", r, s)); if (file.exists(paste0(pre, "_meta.json"))) next
  sd <- T$semente_base + 1000L * T$desenho + r
  tr <- as.data.frame(fread(file.path(ddir, sprintf("rep%03d_treino.csv.gz", r)))); te <- as.data.frame(fread(file.path(ddir, sprintf("rep%03d_teste.csv.gz", r))))
  tr$pheno <- factor(tr$pheno, levels = c(0, 1)); yte <- as.integer(te$pheno); Xtr <- tr[, -1]; Xte <- te[, -1]
  stopifnot(identical(names(Xtr), names(Xte)), nrow(Xte) == 1000L, all(yte %in% 0:1))
  arqP <- file.path(pdir, sprintf("rep%03d.csv.gz", r)); P <- as.matrix(fread(arqP)); storage.mode(P) <- "integer"
  stopifnot(nrow(P) == nrow(Xte), all(apply(P, 2, function(v) identical(sort(v), seq_len(nrow(Xte))))))
  # estado do gerador do R idêntico ao histórico (src/etapa1.R): as permutações R históricas também alimentam o hstats
  set.seed(sd + 900000L); permsR <- lapply(1:30, function(q) sample.int(nrow(Xte))); PR <- do.call(cbind, permsR)
  tabs <- list(); prevs <- list(); nat <- list(); tempos <- list(); val <- list(); m <- T$mtry
  reg <- function(nome, prever) {
    t0 <- agora(); g <- perdas(prever, Xte, yte, P); tempos[[paste0("regua_", nome)]] <<- agora() - t0
    tabs[[nome]] <<- g$tab[, modelo := nome]; prevs[[nome]] <<- g$prev
    if (validar) {
      t0 <- agora(); h <- perdas(prever, Xte, yte, PR); val[[paste0("I_permsR_hist_", nome)]] <<- contraste(h$tab)[, modelo := nome]
      tempos[[paste0("validar_permsR_", nome)]] <<- agora() - t0
    }
  }
  addn <- function(det, sc) nat[[length(nat) + 1]] <<- data.table(detector = det, par = PARES, escore = as.numeric(sc[PARES]))
  if ("rf" %in% modelos) {
    t0 <- agora(); rf <- ranger(pheno ~ ., tr, num.trees = 500, mtry = m, probability = TRUE, num.threads = 1, seed = sd + 1L + OFF); tempos$rf <- agora() - t0
    prev_rf <- function(X) predict(rf, X, num.threads = 1)$predictions[, "1"]
    t0 <- agora(); h <- hstats(rf, X = Xtr, v = V7, pairwise_m = 7, n_max = 500, pred_fun = function(mm, x) predict(mm, x, num.threads = 1)$predictions[, "1"], verbose = FALSE)
    hp <- h2_pairwise(h, normalize = TRUE, squared = TRUE, zero = TRUE, top_m = 21)
    hv <- vazio; for (nm in rownames(hp)) { ab <- strsplit(nm, ":")[[1]]; hv[par_nome(ab[1], ab[2])] <- hp[nm, 1] }; tempos$h <- agora() - t0
    addn("h", hv)
    reg("rf", prev_rf)
    if (validar) { t0 <- agora(); sl <- perdas_sem_lote(prev_rf, Xte, yte, P, c("interactionSNP1", "effectSNP1", PARES[1]))
      cmp <- merge(sl, tabs$rf, by = c("conjunto", "perm"), suffixes = c("_sem_lote", "_lote"))
      val$lote_vs_sem_lote <- data.table(max_dif_ll = max(abs(cmp$logloss_sem_lote - cmp$logloss_lote)),
                                        max_dif_ac = max(abs(cmp$acuracia_sem_lote - cmp$acuracia_lote)), n = nrow(cmp))
      tempos$validar_sem_lote <- agora() - t0 }
  }
  if ("if" %in% modelos) {
    t0 <- agora(); fi <- interactionfor(dependent.variable.name = "pheno", data = tr, importance = "both", num.trees = 500, probability = TRUE,
                                        num.threads = 1, seed = sd + 3L + OFF, verbose = FALSE); tempos$if_ <- agora() - t0
    eim <- function(v) { sc <- vazio; for (nm in names(v)) { ab <- strsplit(gsub(" (large|small)", "", nm), " AND ")[[1]]
      if (all(ab %in% V7) && ab[1] != ab[2]) { k <- par_nome(ab[1], ab[2]); sc[k] <- max(sc[k], v[[nm]], na.rm = TRUE) } }; sc }
    addn("if_quant", eim(fi$eim.quant)); addn("if_qual", eim(fi$eim.qual))
    reg("if", function(X) { p <- predict(fi, data = X, num.threads = 1, verbose = FALSE)$predictions; if (is.null(dim(p))) p else p[, "1"] })
  }
  if ("irf" %in% modelos) {
    t0 <- agora(); set.seed(sd + 4L + OFF)
    f <- iRF(x = as.matrix(Xtr), y = tr$pheno, ntree = 500, mtry = m, n.iter = 5, int.return = 5, n.bootstrap = 30, signed = FALSE,
             n.core = 1, verbose = FALSE)
    it <- f$interaction; sc <- setNames(rep(0, length(PARES)), PARES)   # par não retornado = estabilidade 0 (convenção histórica)
    if (!is.null(it) && nrow(it)) for (i in seq_len(nrow(it))) { ab <- strsplit(gsub("[+-]", "", it$int[i]), "_")[[1]]
      if (length(ab) == 2 && all(ab %in% V7) && ab[1] != ab[2]) { k <- par_nome(ab[1], ab[2]); sc[k] <- max(sc[k], it$stability[i], na.rm = TRUE) } }
    tempos$irf <- agora() - t0; addn("irf", sc)
    rfk <- f$rf.list; reg("irf", function(X) as.numeric(predict(rfk, as.matrix(X), type = "prob")[, "1"]))
  }
  if ("rpf" %in% modelos) {
    t0 <- agora(); set.seed(sd + 5L + OFF); rp <- rpf(x = Xtr, y = tr$pheno, max_interaction = 2, purify = FALSE, parallel = FALSE); tempos$rpf <- agora() - t0
    reg("rpf", function(X) as.numeric(predict(rp, new_data = X, type = "prob")$.pred_1))
    if (!isFALSE(T$nativo_rpf)) {
      t0 <- agora(); purify(rp); pc <- predict_components(rp, new_data = Xte, max_interaction = 2)$m
      rv <- vazio; for (pr in PARES) { ab <- strsplit(pr, ":")[[1]]; nm <- intersect(c(paste(ab, collapse = ":"), paste(rev(ab), collapse = ":")), colnames(pc))
        rv[pr] <- if (length(nm)) var(pc[[nm[1]]]) else 0 }; tempos$rpf_componentes <- agora() - t0
      addn("rpf", rv)
    }
  }
  fwrite(rbindlist(tabs), paste0(pre, "_perdas.csv.gz"))
  fwrite(as.data.table(prevs), paste0(pre, "_previsoes.csv.gz"))
  fwrite(rbindlist(nat), paste0(pre, "_nativos.csv"))
  if (validar) for (nm in names(val)) fwrite(val[[nm]], paste0(pre, "_validar_", nm, ".csv"))
  meta <- list(desenho = T$desenho, repeticao = r, semente_dados = sd, semente_ajuste = s, deslocamento_semente = OFF, mtry = m,
    modelos = modelos, n_treino = nrow(Xtr), n_teste = nrow(Xte), prevalencia_treino = mean(tr$pheno == "1"), prevalencia_teste = mean(yte),
    arquivo_perm = sub(paste0(EXT, "/"), "", arqP), sha256_perm = digest::digest(file = arqP, algo = "sha256"), digital_perm = digital(P),
    digital_permsR_hist = digital(PR), tempos = lapply(tempos, round, 2),
    versoes = lapply(c(R = "base", ranger = "ranger", diversityForest = "diversityForest", iRF = "iRF", randomPlantedForest = "randomPlantedForest",
                       hstats = "hstats", data.table = "data.table"), function(p) as.character(packageVersion(p))),
    R = R.version.string, no = Sys.info()[["nodename"]], tarefa_slurm = Sys.getenv("SLURM_JOB_ID"), quando = format(Sys.time(), "%Y-%m-%dT%H:%M:%S%z"))
  writeLines(jsonlite::toJSON(meta, auto_unbox = TRUE, digits = NA, pretty = TRUE), paste0(pre, "_meta.json"))
}
cat("ok\n")
