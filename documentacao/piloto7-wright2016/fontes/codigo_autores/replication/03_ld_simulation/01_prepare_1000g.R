library(readr)
library(hapsim)
library(snpStats)

## Get haplotypes from vcf file
## 1000g vcf required!
vcf_file <- "chr22.vcf"
outname <- "new2"
system(paste("~/vcftools",
             "--vcf", vcf_file, 
             "--ldhat",
             "--out", outname, 
             "--chr", 22, 
             "--maf", 0.05, 
             "--max-maf", 0.2,
             "--max-missing", 1.0))

## Get haplotypes
system(paste0("grep \\> ", outname, ".ldhat.sites -v > ", outname, ".haplo"))
system(paste0("grep \\> ", outname, ".ldhat.sites > ", outname, ".ids"))

## Read haplotypes
haplo <- read_fwf(paste0(outname, ".haplo"), fwf_widths(rep(1, 54389)), skip = 1)
colnames(haplo) <- gsub("X", "SNP", colnames(haplo))
saveRDS(haplo, "haplo2.Rds")
haplo <- readRDS("haplo2.Rds")

## Subset haplotypes
idx <- 20000:(20000+1000)
haplo_small <- haplo[, idx]
saveRDS(haplo_small, "haplo_small.Rds")
