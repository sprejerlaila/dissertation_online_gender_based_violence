
# Perspective API
#devtools::install_github("favstats/peRspective")
library(peRspective)
library(usethis)
library(dplyr)
library(cgwtools)
options(scipen = 999)

getToxicity = function(text, idx, this.script = 1,
                       api.choice = 'not set',
                       sleepz = 30){
  dat.this.time = Sys.Date()
  
  if(api.choice == 'not set'){
    api.choice = this.script
  }
  
  api.key.all = c('XXX',
                  'XXX',
                  'XXX')
  
  api_key = api.key.all[[api.choice]]
  
  print(paste0('dat.this.time is: ', dat.this.time,
               ' and the API is: ', api_key,
               ' and this.script is equal to: ', this.script))
  
  result_sentence = data.frame(matrix(ncol = 17, nrow = 0))
  
  for (i in 1:length(text)){
    print(i)
    
    # save results
    if(i %% 100 == 0){
      print(Sys.time())
      print(text_scores)
      print(paste0('sleeping for ', sleepz, ' seconds'));
      Sys.sleep(sleepz);
    }
    
    # Collect scores
    text_scores <- prsp_score(
      text = text[[i]],
      languages = "es",
      score_model = c("TOXICITY", "SEVERE_TOXICITY","IDENTITY_ATTACK_EXPERIMENTAL",
                      "INSULT_EXPERIMENTAL","PROFANITY_EXPERIMENTAL","THREAT_EXPERIMENTAL"),
      key = api_key
    )
    
    text_scores$idx = idx[[i]]
    write.table(text_scores, paste("perspective_scores_",api.choice,".csv",sep = ""),
                sep = ",", col.names = !file.exists(paste("perspective_scores_",api.choice,".csv",sep = "")), row.names = F, append = T)
  }
  
  save(result_sentence,
       file = paste0("temp_toxicity_", this.script, ".RData"))
  
  
  return(result_sentence)
}

tweets <- readr::read_csv("unique_tweets_for_perspective.csv")
tweets <- tweets[!is.na(tweets$text), ]

args = commandArgs(trailingOnly=TRUE)
api.choice = as.numeric(args[1])
print(paste("args", api.choice))
chunks = 1000

start_tweet <- ((api.choice-1)*chunks) +1

getToxicity(text = tweets[ start_tweet : (api.choice*chunks), ]$text, idx = tweets[ start_tweet : (api.choice*chunks), ]$id, api.choice = api.choice)


