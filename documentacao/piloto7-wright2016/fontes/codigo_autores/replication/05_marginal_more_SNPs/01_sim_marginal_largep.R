
source("simulate_snps.R")
#source("helper_functions.R")
source("algorithms.R")
source("problems.R")
library(BatchExperiments)
library(reshape2)
library(ggplot2)
library(RColorBrewer)
library(scales)

seed <- 12345
set.seed(seed)

## ================================================================= ##
## Create registry
## ================================================================= ##
##registries <- file.path(".")
registries <- file.path("/imbs/home/wright/batchjobs/registries")
registry_name <- 'marginal_largep'
registry <- file.path(registries, registry_name)
unlink(registry, recursive = TRUE)
reg <- makeExperimentRegistry(registry_name, file.dir = registry, 
                              packages = c("ranger", "randomForestSRC"),
                              src.files = c("simulate_snps.R", "problems.R", 
                                            "algorithms.R"), 
                              seed = seed)

## ================================================================= ##
## Problem/Simulation parameters
## ================================================================= ##
num_replicates <- 100
n <- 1000
prop_cases <- 0.5
num_effect_snps <- 5 ## Not including interaction SNPs
num_noise_snps <- 2493
model <- c("no_interaction", "synergistic", "interaction_only",
           "modifier_snp1", "modifier_snp2", "redundant")
beta <- 0.4 #c(0.4, 0.8) ## Main effect for interaction SNPS, interaction effect is determined by model
beta_effect <- 0.4 #c(0.4, 0.8)
## beta_0 is adjusted to get prop_cases as proportion of cases 

maf_interaction <- 0.2 #c(0.2, 0.2, 0.4)
maf_effect <- 0.2 #c(0.2, 0.4, 0.2) 
maf_noise <- NA # c(0.2, 0.4, 0.2) # NA is runif(0,1)

## ================================================================= ##
## Algorithm parameters
## ================================================================= ##
num_threads <- 1
num_trees <- 500
mtry <- 50 #c(10, 50)

## ================================================================= ##
## Problems
## ================================================================= ##
addProblem(reg, id = "sim", dynamic = simulate_data, seed = seed)

## ================================================================= ##
## Algorithms
## ================================================================= ##
addAlgorithm(reg, id="impurity", fun=impurity_wrapper)
addAlgorithm(reg, id="permutation", fun=permutation_wrapper)
addAlgorithm(reg, id="jvimp", fun=jvimp_wrapper)
addAlgorithm(reg, id="jmst", fun=jmst_wrapper)
addAlgorithm(reg, id="pairwise", fun=pairwise_wrapper)

## ================================================================= ##
## Problem designs
## ================================================================= ##
sim_pars <- list(n = n, prop_cases = prop_cases, num_effect_snps = num_effect_snps,
                 num_noise_snps = num_noise_snps, model = model, 
                 beta = beta, beta_effect = beta_effect)
sim_design <- makeDesign("sim", exhaustive = sim_pars, 
                         design = data.frame(maf_interaction, maf_effect, maf_noise))

## ================================================================= ##
## Algorithm designs
## ================================================================= ##
algo_pars <- list(num_trees = num_trees, num_threads = num_threads, mtry = mtry)

impurity_design <- makeDesign("impurity", exhaustive = algo_pars)
permutation_design <- makeDesign("permutation", exhaustive = algo_pars)
pairwise_design <- makeDesign("pairwise", exhaustive = algo_pars)
jvimp_design <- makeDesign("jvimp", exhaustive = algo_pars)
jmst_design <- makeDesign("jmst", exhaustive = algo_pars)

algo_designs <- list(impurity_design, permutation_design, pairwise_design, 
                     jvimp_design, jmst_design) 

## ================================================================= ##
## Add experiments
## ================================================================= ##
addExperiments(reg, prob.designs = sim_design,
               algo.designs = algo_designs,
               repls = num_replicates)

## ================================================================= ##
## Check experiments
## ================================================================= ##
summarizeExperiments(reg)

## ================================================================= ##
## Create and submit jobs, wait until finished
## ================================================================= ##
submitJobs(reg = reg, ids = chunk(getJobIds(reg), n.chunks = 1, shuffle = TRUE),
           resources = list(nodes = 1, ppn = 1, mem = "40g"), #, atonce = 150),
           chunks.as.arrayjobs = TRUE, job.delay = TRUE)

waitForJobs(reg, timeout = Inf, stop.on.error = FALSE)
##killJobs(reg, getJobIds(reg), progressbar = TRUE)

## ================================================================= ##
## Get and save results
## ================================================================= ##
result_function <- function(job, res) {
  names(res) <- "rank"
  res
}
results <- reduceResultsExperiments(reg, fun = result_function)
saveRDS(results, "results_largep.Rds")
##results <- readRDS("results_largep.Rds")

