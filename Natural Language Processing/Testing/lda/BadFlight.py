import pandas as pd

query = 'Cancelled Flight'

df = pd.read_csv('Tweets.csv')
df2 = pd.DataFrame()

list_text = []
list_nega = []
list_sent = []

for index,row in df.iterrows():
    if row['negativereason']==query:
        list_text.append(row['text'])
        list_nega.append(row['negativereason'])
        list_sent.append(row['airline_sentiment_confidence'])

df2['text'] = pd.Series(list_text)
df2['negativereason'] = pd.Series(list_nega)
df2['airline_sentiment_confidence'] = pd.Series(list_sent)

query = query.replace(" ","")

df2.to_csv(query + '.csv')



