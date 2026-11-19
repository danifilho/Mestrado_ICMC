
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
  
  ## Return rank of interactionSNP1:interactionSNP2
  ranks <- rank(-ret) ## Largest first 
  max(ranks["interactionSNP1"], ranks["interactionSNP2"])
}

## ================================================================= ##
## Permutation (ranger)
## ================================================================= ##
permutation_wrapper <- function(static, dynamic, num_trees, num_threads, mtry) {
  rf <- ranger(pheno ~ ., data = dynamic, importance = "permutation", 
               num.trees = num_trees, num.threads = num_threads, 
               mtry = mtry)
  ret <- ranger::importance(rf)
  
  ## Return rank of interactionSNP1:interactionSNP2
  ranks <- rank(-ret) ## Largest first 
  max(ranks["interactionSNP1"], ranks["interactionSNP2"])
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
  
  ## Return rank of interactionSNP1:interactionSNP2
  rank(-ret)["interactionSNP1:interactionSNP2"] ## Largest first 
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
  
  ## Return rank of interactionSNP1:interactionSNP2
  rank(-ret)["interactionSNP1:interactionSNP2"] ## Largest first 
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
  
  ## Return rank of interactionSNP1:interactionSNP2
  rank(ret)["interactionSNP1:interactionSNP2"] ## Smallest first because small is interaction
}



