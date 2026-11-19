library(hapsim)

##----------------------------------------------------------------------
## Simulate SNP data
##----------------------------------------------------------------------
simulate_ld_snps <- function(n.obs = 100, n.snp = 100) {
  ## Read haplotype data
  haplo_small <- readRDS("../03_ld_simulation/haplo_small.Rds")
  
  ## Select haplotypes
  haplo_sampled <- haplo_small[, sample(ncol(haplo_small), n.snp)]
  
  ## Simulate LD structure
  library(hapsim)
  hapdat <- haplodata(haplo_sampled)
  hapsim <- haplosim(n = 2*n.obs, hapdat)
  
  ## Merge every 2 rows to create genotypes
  haplo_1g <- hapsim$data
  geno_1g <- haplo_1g[seq(1, nrow(haplo_1g), 2), ] + haplo_1g[seq(2, nrow(haplo_1g), 2), ]
  
  ## Change names
  colnames(geno_1g) <- paste('SNP.', 1:n.snp, sep='')
  rownames(geno_1g) <- paste('ID', 1:n.obs, sep='')
  return(geno_1g)
}

