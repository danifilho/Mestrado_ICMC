
library(snpStats)
source("simulate_ld_snps.R")

## Parameters
n <- 1000
num_snps <- 100

## Simulate SNPs
snps <- as.matrix(simulate_ld_snps(n.obs = n, n.snp = num_snps))
snp_matrix <- new("SnpMatrix", snps)

## Compute LD: D' and r^2
ld <- ld(snp_matrix, depth = num_snps-1, stats = c("R.squared", "D.prime"))
d <- ld$D.prime[upper.tri(ld$D.prime)]
r2 <- ld$R.squared[upper.tri(ld$R.squared)]

mean(d, na.rm = TRUE)
sd(d, na.rm = TRUE)

mean(r2, na.rm = TRUE)
sd(r2, na.rm = TRUE)