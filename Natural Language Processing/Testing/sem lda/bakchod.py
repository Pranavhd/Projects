from nltk.corpus import wordnet
import pandas as pd

df = pd.read_csv('Book1.csv')
my = df['Text'].tolist()

ano = []
for ele in my:
    n = len(ele)
    ano.append(ele[8:n-2])

print(ano)
