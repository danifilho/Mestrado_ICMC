source("simulate_snps.R")
#source("helper_functions.R")
source("algorithms.R")
source("problems.R")
library(BatchExperiments)
library(reshape2)
library(ggplot2)
library(RColorBrewer)
library(scales)

results <- readRDS("results.Rds")

## ================================================================= ##
## Prepare plots
## ================================================================= ##
k <- 1:20

## Compute proportion of top-k places for each combination
in_top_k <- data.frame(sapply(k, function(kk) {
  results$rank <= kk
}))
colnames(in_top_k) <- paste("top", k, sep = "")
param_names <- c("n", "prop_cases", "num_effect_snps", "num_noise_snps", "model", "beta", "beta_effect", "maf_interaction", "maf_effect", "algo", "mtry")
params <- results[, param_names]
dat <- aggregate(in_top_k, by = params, FUN = mean)

## Plot each model with all 5 algos, all models in one plot for each combination
df <- melt(dat, id.vars = param_names, value.name = "detection")

## Rename algos
df$algo <- factor(df$algo, levels = c("impurity", "permutation", "jvimp", "jmst", "pairwise"), c("Gini", "Permutation", "JVIMP", "JMST", "PPI"))

plot_param_names <- c("n", "prop_cases", "num_effect_snps", "num_noise_snps", "beta", "beta_effect", "maf_interaction", "maf_effect", "mtry")
unique_params <- unique(df[, plot_param_names])
levels(df$variable) <- k
df$k <- as.numeric(as.character(df$variable))

## Exclude "modifier_snp2" model
df <- df[df$model != "modifier_snp2", ]

## Rename models
levels(df$model) <- c("Interaction only", "Modifier SNP", "XXX", "No Interaction", 
                      "Redundant", "Synergistic")

## ================================================================= ##
## Plots single measures
## ================================================================= ##
## Create plots for single measures
plots_single <- apply(unique_params, 1, function(y) {
  idx <- apply(df[, plot_param_names], 1, function(x) {
    all(x == y)
  })
  plot_data <- subset(df[idx, ], algo %in% c("Gini", "Permutation") & k >= 5 & k <= 15)
  
  show_params <- c("beta", "beta_effect", "maf_interaction", "maf_effect", "mtry")
  param_names <- c("beta_I", "beta_M", "MAF_I", "MAF_M", "mtry")
  title <- paste(param_names, y[show_params], collapse = ",  ", sep = "=")
  
  ggplot(plot_data, aes(x = k, y = detection, color = algo, shape = algo)) + 
    geom_line() + geom_point() + 
    facet_wrap(~model, nrow = 1) + 
    xlab("Number of top SNPs considered") + 
    ylim(0, 1) + 
    ylab("Included proportion") + 
    scale_color_brewer(palette = "Set1", name = "Importance measure") + 
    scale_shape_discrete(name = "Importance measure") + 
    scale_x_continuous(breaks = seq(5, 15, by = 2)) + 
    ggtitle(title) + 
    theme(plot.title = element_text(size = rel(0.8))) + 
    coord_fixed(ratio = 10)
})

## Plot in one pdf
pdf("marginal_single.pdf", width = 10, height = 3)
print(plots_single)
dev.off()

## Plot in multiple pdfs
dir.create("marginal_single")
lapply(plots_single, function(x) {
  filename <- gsub("\n ", "_", x$labels$title)
  ggsave(file.path("marginal_single", paste0("marginal_single_", filename, ".pdf")), x + ggtitle(""), 
         width = 10, height = 3)
})

## ================================================================= ##
## Plots pairwise measures
## ================================================================= ##
## Create plots for pairwise measures
plots_pairwise <- apply(unique_params, 1, function(y) {
  idx <- apply(df[, plot_param_names], 1, function(x) {
    all(x == y)
  })
  plot_data <- subset(df[idx, ], algo %in% c("JVIMP", "JMST", "PPI") & k >= 10 & k <= 20)
  
  show_params <- c("beta", "beta_effect", "maf_interaction", "maf_effect", "mtry")
  param_names <- c("beta_I", "beta_M", "MAF_I", "MAF_M", "mtry")
  title <- paste(param_names, y[show_params], collapse = ",  ", sep = "=")
  
  ggplot(plot_data, aes(x = k, y = detection, color = algo, shape = algo)) + 
    geom_line() + geom_point() + 
    facet_wrap(~model, nrow = 1) + 
    xlab("Number of top SNP pairs considered") + 
    ylim(0, 1) + 
    ylab("Included proportion") + 
    scale_color_manual(values = brewer.pal(5, "Set1")[3:5], name = "Importance measure") + 
    scale_shape_discrete(name = "Importance measure") + 
    scale_x_continuous(breaks = seq(10, 20, by = 2)) + 
    ggtitle(title) +
    theme(plot.title = element_text(size = rel(0.8))) + 
    coord_fixed(ratio = 10)
})

## Plot in one pdf
pdf("marginal_pairwise.pdf", width = 10, height = 3)
print(plots_pairwise)
dev.off()

## Plot in multiple pdfs
dir.create("marginal_pairwise")
lapply(plots_pairwise, function(x) {
  filename <- gsub("\n ", "_", x$labels$title)
  ggsave(file.path("marginal_pairwise", paste0("marginal_pairwise_", filename, ".pdf")), x + ggtitle(""), 
         width = 10, height = 3)
})


