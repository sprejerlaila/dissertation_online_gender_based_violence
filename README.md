# Online Violence against women: a machine learning study on Argentine Politicians

Code for dissertaton - MSc. Applied Social Data Science - LSE

Content: 
- 0.Data: 
  - metadata.csv: data on politicians
  - stream_tweets.py; process_tweets.py; get_congress_tweets.py: stream tweets, tidy and process
  - target_precision.ipynb: calculate target precision and expand dataset
  - get_botometer.py: detect bots
  
- 1.EDA:
  - EDA.Rmd: Exploratory data analysis
  
- 2.Perspective:
  - get_perspective.py: get perspective scores for all tweets
  - perspective_analysis.Rmd: Analyse perspective results

- 3.Dictionaries:
  - Insults_list.csv: list of insults and RegEx patterns
  - dict_analysis.Rmd: analyse dictionary results
  
- 4.topic_model:
  - run_lda.py: run LDA models
  - lda.Rmd: analyse LDA results
  - run_stm.py: run STM models
  - stm.Rmd: analyse STm results
  
- 5.stereotypes:
  - run_lasso.py: run lasso models
