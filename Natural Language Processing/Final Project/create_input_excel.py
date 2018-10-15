import pandas as pd

df = pd.DataFrame()
number_of_tweets = int(input())

list_tweets = []
for i in range(number_of_tweets):
    tweet = input()
    list_tweets.append(tweet)

df['text'] = pd.Series(list_tweets)
df.to_csv('Input_Tweets.csv')
