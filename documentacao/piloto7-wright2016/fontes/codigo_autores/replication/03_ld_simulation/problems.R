
## ================================================================= ##
## Simulate SNP data
## ================================================================= ##
simulate_data <- function(static, n, prop_cases, num_effect_snps, num_noise_snps, 
                          #maf_interaction, maf_effect, maf_noise, 
                          model, beta, beta_effect) {
  
  num_snps <- 2 + num_effect_snps + num_noise_snps
  
  ## Simulate SNPs
  snps <- as.matrix(simulate_ld_snps(n.obs = n, n.snp = num_snps))
  
  ## Get MAF
  maf_interaction <- mean(snps[, 1:2])/2
  maf_effect <- mean(snps[, 3:(3+num_effect_snps-1)])/2
  
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
    
  ## Interaction SNPs
  colnames(snps)[1:2] <- paste("interactionSNP", 1:2, sep = "")
  
  ## Effect SNPs
  idx <- 3
  if (num_effect_snps > 0) {
    colnames(snps)[idx:(idx+num_effect_snps-1)] <- paste("effectSNP", 1:num_effect_snps, sep = "")
    idx <- idx+num_effect_snps
  } 
  
  ## Noise SNPs
  if (num_noise_snps > 0) {
    colnames(snps)[idx:(idx+num_noise_snps-1)] <- paste("noiseSNP", 1:num_noise_snps, sep = "")
  }
  
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