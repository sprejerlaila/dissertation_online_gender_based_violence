library("quanteda", quietly = TRUE, warn.conflicts = FALSE, verbose = FALSE)
library(dplyr)
library(tidyr)
library(stringr)
library(ggplot2)
library(ggpubr)
library(stm)
#library(furrr)
library(purrr)
library(reshape2)
library(ggplot2)
library(dplyr)


df_dir_at_congress <- read.csv("tweets_for_stm.csv", stringsAsFactors = FALSE)
df_dir_at_congress <- df_dir_at_congress[df_dir_at_congress$target_precision == "High", ]


tcorp <- corpus(df_dir_at_congress$text)
stopwords_spanish <- c(stopwords("spanish"),
                       c("https", "t.co", "rt", "vos", "sos", "usted", "q", "x", "xq", "dsd", "d"))

dfm_at <- tokens(tcorp, remove_punct = TRUE) %>%
  dfm(tolower = TRUE, remove_numbers = TRUE,
      remove = stopwords_spanish)

cdfm <- dfm_trim(dfm_at, min_docfreq = 20)

doc_ntokens <- rowSums(cdfm)
drop_idx <- which(doc_ntokens==0)

cdfm <- cdfm[-drop_idx,]

interbloque <- as.numeric(as.factor(df_dir_at_congress$directed_at_interbloque))[-drop_idx]
gender <- as.numeric(as.factor(df_dir_at_congress$directed_at_gender))[-drop_idx]
meta <- data.frame(interbloque, gender)

library(furrr)
plan(multiprocess)

set.seed(3)
many_models <- data_frame(K = c(20, 30, 40, 50, 60, 70, 80)) %>%
  mutate(topic_model = future_map(K, ~stm(cdfm, K = .,
                                          prevalence = ~interbloque + gender,
                                          data = meta,
                                          verbose = FALSE,
                                          seed = 123)))

save(many_models, file="many_models.Rdata")
