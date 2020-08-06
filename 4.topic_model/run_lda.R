# load up some R packages including a few we'll need later

library(reshape2)
library(dplyr)
library(quanteda)

tweets <- read.csv('replies.csv', stringsAsFactors = FALSE)

unique_tweets <- unique(tweets$in_reply_to_status)

corpus <- corpus(unique_tweets)
cdfm <- dfm(corpus, remove=stopwords("spanish"), verbose=TRUE,
            remove_punct=TRUE, remove_numbers=TRUE)
cdfm <- dfm_trim(cdfm, min_docfreq = 2)

doc_ntokens <- rowSums(cdfm)
drop_idx <- which(doc_ntokens==0)

cdfm <- cdfm[-drop_idx,]

test <- convert(cdfm, to='matrix')


burnin = 1000
iter = 1000
keep = 50
full_data  <- test
n <- nrow(full_data)

library(topicmodels)
library(doParallel)
library(ggplot2)
library(scales)

cluster <- makeCluster(detectCores(logical = TRUE) - 1) # leave one CPU spare...
registerDoParallel(cluster)

# load up the needed R package on all the parallel sessions
clusterEvalQ(cluster, {
  library(topicmodels)
})

folds <- 5
splitfolds <- sample(1:folds, n, replace = TRUE)
candidate_k <- c(5,10,20,30,40,50,60,70,80) # candidates for how many topics

# export all the needed R objects to the parallel sessions
clusterExport(cluster, c("full_data", "burnin", "iter", "keep", "splitfolds", "folds", "candidate_k"))

# we parallelize by the different number of topics.  A processor is allocated a value
# of k, and does the cross-validation serially.  This is because it is assumed there
# are more candidate values of k than there are cross-validation folds, hence it
# will be more efficient to parallelise
system.time({
  results <- foreach(j = 1:length(candidate_k), .combine = rbind) %dopar%{
    k <- candidate_k[j]
    results_1k <- matrix(0, nrow = folds, ncol = 3)
    colnames(results_1k) <- c("k", "perplexity", "loglik")
    for(i in 1:folds){
      train_set <- full_data[splitfolds != i , ]
      valid_set <- full_data[splitfolds == i, ]
      
      fitted <- LDA(train_set, k = k, method = "Gibbs",
                    control = list(burnin = burnin, iter = iter, keep = keep) )
      results_1k[i,] <- c(k, perplexity(fitted, newdata = valid_set), logLik(fitted))
    }
    return(results_1k)
  }
})
stopCluster(cluster)

results_df <- as.data.frame(results)

save(results_df, file="results_df.Rdata")