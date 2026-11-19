
## ================================================================= ##
## Simulate SNP data
## ================================================================= ##
simulate_data <- function(static, n, prop_cases, num_effect_snps, num_noise_snps, 
                          maf_interaction, maf_effect, maf_noise, model, beta, beta_effect) {
  
  num_snps <- 2 + num_effect_snps + num_noise_snps
  
  ## Adjust beta_0 to get prop_cases as proportion of cases 
  ## Additive model -> 2*maf^2
  bx_interaction <- 2*beta*(2*maf_interaction^2 + 2*maf_interaction*(1-maf_interaction))
  bx_effect <- num_effect_snps*beta_effect*(2*maf_effect^2 + 2*maf_effect*(1-maf_effect))
  beta_0 <- -log((1-prop_cases)/prop_cases) - bx_interaction - bx_effect
  
  ## Create model
  ## Intercept, Environment, SNP, Interaction, effect SNPs
  if (model == "no_interaction") {
    beta_model <- c(beta_0, beta, beta, 0, rep(beta_effect, num_effect_snps))
  } else if (model == "synergistic") {
    beta_model <- c(beta_0, beta, beta, beta, rep(beta_effect, num_effect_snps))
  } else if (model == "interaction_only") {
    beta_model <- c(beta_0, 0, 0, beta, rep(beta_effect, num_effect_snps))
  } else if (model == "modifier_snp1") {
    beta_model <- c(beta_0, 0, beta, beta, rep(beta_effect, num_effect_snps))
  } else if (model == "modifier_snp2") {
    beta_model <- c(beta_0, beta, 0, beta, rep(beta_effect, num_effect_snps))
  } else if (model == "redundant") {
    beta_model <- c(beta_0, beta, beta, -beta, rep(beta_effect, num_effect_snps))
  } else {
    stop("Unknown model.")
  }
    
  ## Simulate interaction SNPs
  interaction_snps <- as.matrix(simulate_snps(n.obs = n, n.snp = 2, maf = maf_interaction, 
                                              beta0 = 0, beta = 0, type = "binary")[, -1])
  colnames(interaction_snps) <- paste("interactionSNP", 1:2, sep = "")
  
  ## Simulate effect SNPs
  if (num_effect_snps > 0) {
    effect_snps <- as.matrix(simulate_snps(n.obs = n, n.snp = num_effect_snps, maf = maf_effect, 
                                           beta0 = 0, beta = 0, type = "binary")[, -1])
    colnames(effect_snps) <- paste("effectSNP", 1:num_effect_snps, sep = "")
  } else {
    effect_snps <- NULL
  }
  
  ## Simulate noise SNPs
  if (is.na(maf_noise)) {
    maf_noise <- runif(num_noise_snps)
  }
  if (num_noise_snps > 0) {
    noise_snps <- as.matrix(simulate_snps(n.obs = n, n.snp = num_noise_snps, maf = maf_noise, 
                                          beta0 = 0, beta = 0, type = "binary")[, -1])
    colnames(noise_snps) <- paste("noiseSNP", 1:num_noise_snps, sep = "")
  } else {
    noise_snps <- NULL
  }
  
  snps <- cbind(interaction_snps, effect_snps, noise_snps)
  
  ## Simulate phenotype, 0,1,2 coding -> additive model
  if (num_effect_snps > 0) {
    x <- rbind(1, snps[, 1], snps[, 2], snps[, 1] * snps[, 2], t(snps[, 3:(num_effect_snps+2)])) 
  } else {
    x <- rbind(1, snps[, 1], snps[, 2], snps[, 1] * snps[, 2]) 
  }
  z <- beta_model %*% x
  prob_pheno <- 1/(1+exp(-z))
  pheno <- factor(rbinom(n, 1, prob_pheno))
  
  ## Create and return dataset
  data.frame(pheno, snps)
}