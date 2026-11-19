
library(ranger)
library(randomForestSRC)
options(rf.cores = 1, mc.cores = 1)

## ================================================================= ##
## Impurity (ranger)
## ================================================================= ##
impurity_wrapper <- function(static, dynamic, num_trees, num_threads, mtry) {
  rf <- ranger(pheno ~ ., data = dynamic, importance = "impurity", 
               num.trees = num_trees, num.threads = num_threads, 
               mtry = mtry)
  ret <- ranger::importance(rf)
  
  ## Get variables beginning with interaction or effect
  #interaction_idx <- gsub("[0-9]*", "", colnames(dynamic)) == "interactionSNP"
  effect_idx <- gsub("[0-9]*", "", colnames(dynamic)) == "effectSNP"
  
  ## Return rank of marginal SNPs
  ranks <- rank(-ret) ## Largest first 
  max(ranks[colnames(dynamic)[effect_idx]])
}

## ================================================================= ##
## Permutation (ranger)
## ================================================================= ##
permutation_wrapper <- function(static, dynamic, num_trees, num_threads, mtry) {
  rf <- ranger(pheno ~ ., data = dynamic, importance = "permutation", 
               num.trees = num_trees, num.threads = num_threads, 
               mtry = mtry)
  ret <- ranger::importance(rf)
  
  ## Get variables beginning with interaction or effect
  #interaction_idx <- gsub("[0-9]*", "", colnames(dynamic)) == "interactionSNP"
  effect_idx <- gsub("[0-9]*", "", colnames(dynamic)) == "effectSNP"
  
  ## Return rank of marginal SNPs
  ranks <- rank(-ret) ## Largest first 
  max(ranks[colnames(dynamic)[effect_idx]])
}

## ================================================================= ##
## Pairwise (ranger)
## ================================================================= ##
pairwise_wrapper <- function(static, dynamic, num_trees, num_threads, mtry) {
  ## Get variables beginning with interaction or effect
  interaction_idx <- gsub("[0-9]*", "", colnames(dynamic)) == "interactionSNP"
  effect_idx <- gsub("[0-9]*", "", colnames(dynamic)) == "effectSNP"
  xvar.names <- colnames(dynamic)[interaction_idx | effect_idx]
  
  ## Compute rf, importance and cindex
  rf <- ranger(pheno ~ ., data = dynamic, importance = "pairwise", 
               pairwise.importance.variables = xvar.names, 
               num.trees = num_trees, num.threads = num_threads, 
               mtry = mtry)
  ret <- ranger::importance(rf) 
  
  ## Get all marginalSNP combinations
  evars <- colnames(dynamic)[effect_idx]
  ecombs <- combn(evars, 2, FUN = paste, collapse = ":")
  
  ## Return max rank of marginalSNP combinations
  ranks <- rank(-ret) ## Largest first 
  max(ranks[ecombs])
}

## ================================================================= ##
## JVIMP (rfsrc)
## ================================================================= ##
jvimp_wrapper <- function(static, dynamic, num_trees, num_threads, mtry) {
  rf <- rfsrc(pheno ~ ., data = dynamic, forest = TRUE, ntree = num_trees, 
              mtry = mtry)
  
  ## Get variables beginning with interaction or effect
  interaction_idx <- gsub("[0-9]*", "", colnames(dynamic)) == "interactionSNP"
  effect_idx <- gsub("[0-9]*", "", colnames(dynamic)) == "effectSNP"
  xvar.names <- colnames(dynamic)[interaction_idx | effect_idx]
  
  ## Compute importance and cindex
  vimp <- find.interaction(rf, importance = "permute", method = "vimp", 
                           xvar.names = xvar.names, verbose = FALSE)
  ret <- abs(vimp[, "Difference"])
  
  ## Get all marginalSNP combinations
  evars <- colnames(dynamic)[effect_idx]
  ecombs <- combn(evars, 2, FUN = paste, collapse = ":")
  
  ## Return max rank of marginalSNP combinations
  ranks <- rank(-ret) ## Largest first 
  max(ranks[ecombs])
}

## ================================================================= ##
## JSMST (rfsrc)
## ================================================================= ##
jmst_wrapper <- function(static, dynamic, num_trees, num_threads, mtry) {
  rf <- rfsrc(pheno ~ ., data = dynamic, forest = TRUE, ntree = num_trees, 
              mtry = mtry)
 
  ## Get variables beginning with interaction or effect
  interaction_idx <- gsub("[0-9]*", "", colnames(dynamic)) == "interactionSNP"
  effect_idx <- gsub("[0-9]*", "", colnames(dynamic)) == "effectSNP"
  xvar.names <- colnames(dynamic)[interaction_idx | effect_idx]
  
  ## Compute importance and cindex
  vimp <- find.interaction(rf, importance = "permute", method = "maxsubtree", 
                           xvar.names = xvar.names, verbose = FALSE)
  p <- nrow(vimp)
  ret <- rep(NA, p*(p-1)/2)
  names(ret) <- rep(NA, p*(p-1)/2)
  k <- 1
  for (i in 1:(p-1)) {
    for (j in (i+1):p) {
      ret[k] <- (vimp[i, j] + vimp[j, i]) / 2
      names(ret)[k] <- paste(rownames(vimp)[i], colnames(vimp)[j], sep = ":")
      k <- k + 1
    }
  }
  
  ## Get all marginalSNP combinations
  evars <- colnames(dynamic)[effect_idx]
  ecombs <- combn(evars, 2, FUN = paste, collapse = ":")
  
  ## Return max rank of marginalSNP combinations
  ranks <- rank(ret)
  max(ranks[ecombs])
}



