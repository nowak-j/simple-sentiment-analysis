# Simple statistical sentiment analysis with Python

The program performs an opinion analysis of a given text. The examination of opinions is carried out using a statistical method, i.e. by counting positive and negative words. 

The algorithm of opinion examination looks as follows:

1. ```Divide the given opinion into words. Let result = 0```
1. ```For each word s execute:```
    1. ```If word s is positive then result = result + 1```
    1. ```If word s is negative then result = result - 1```
1. ```If result > 0 then the opinion is positive, if < 0 then negative, if equal to 0 then neutral.```

Positive and negative words and stopwords were taken from the web.


Reposititories used:
https://github.com/shekhargulati/sentiment-analysis-python/blob/master/opinion-lexicon-English/positive-words.txt
https://github.com/shekhargulati/sentiment-analysis-python/blob/master/opinion-lexicon-English/negative-words.txt
https://gist.github.com/sebleier/554280
