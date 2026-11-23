##----------------------------------------------------------------------
## Simulate SNP data
##----------------------------------------------------------------------
simulate_snps <- function(n.obs = 100, n.snp = 5000, maf = 0.25, 
                          beta0 = 0, beta = 0, type = "binary") {
  
  if (length(beta) == 1) {
    beta <- rep(beta, n.snp)
  }
  if (length(maf) == 1) {
    maf <- rep(maf, n.snp)
  }
  
  ## Create design matrix
  X <- data.frame(sapply(maf, function(x) {
      sample(c(0,1,2), n.obs, replace = TRUE, 
             prob = c({1-x}**2, 2*{1-x}*x, x**2))
      }))
  colnames(X) <- paste('SNP.', 1:n.snp, sep='')
  rownames(X) <- paste('ID', 1:n.obs, sep='')
  
  ## Create response and return
  y.linear <- as.matrix(X) %*% matrix(beta, ncol = 1) + beta0
  if (type == "binary") {
    y <- as.factor(rbinom(n.obs, size=1, prob = plogis(y.linear)))
    return(data.frame(y, X))
  } else  if (type == "quant") {
    y <- y.linear 
    return(data.frame(y, X))
  } else  if (type == "surv") {
    time <- y.linear + rnorm(n.obs)
    time <- time - min(time)
    status <- rbinom(n.obs, 1, 0.8)
    y <- data.frame(time = time, status = status)
    return(cbind(y, X))
  }
}

