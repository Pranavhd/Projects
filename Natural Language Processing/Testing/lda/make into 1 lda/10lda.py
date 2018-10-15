import pandas as pd
from nltk.corpus import stopwords 
from nltk.stem.wordnet import WordNetLemmatizer
import string
import gensim
from gensim import corpora

##df = pd.read_csv('Tweets.csv')
##df2 = pd.DataFrame()
##
##df2['text'] = df['text']

##df2['negativereason'] = df['negativereason']
##df2['airline_sentiment_confidence'] = df['airline_sentiment_confidence']
##
##df2.to_csv('R.csv')

#query = 'Cancelled Flight'

query = 'Tweets'

df = pd.read_csv(query + '.csv')

doc_complete = df['text']

stop = set(stopwords.words('english'))
exclude = set(string.punctuation) 
lemma = WordNetLemmatizer()
def clean(doc):
    try:
        stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
        punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
        normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
        return normalized
    except:
        pass

print("1")
doc_clean = [clean(doc).split() for doc in doc_complete]

print("2")
dictionary = corpora.Dictionary(doc_clean)
doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]

print("3")
Lda = gensim.models.ldamodel.LdaModel

print("4")
ldamodel = Lda(doc_term_matrix, num_topics=10, id2word = dictionary, passes=50)

print(query)
print(ldamodel.print_topics(num_topics=10, num_words=5))
print("----------------------------------------------------")
