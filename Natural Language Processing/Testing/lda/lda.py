from nltk.corpus import stopwords 
from nltk.stem.wordnet import WordNetLemmatizer
import string
import gensim
from gensim import corpora

doc1 = "IOTA Sugar "
doc2 = "IOTA father"
doc3 = "IOTA Doctors"
doc4 = "IOTA father"
doc5 = "ZETA Health"
doc6 = "zeta "
doc7 = "zeta "

# compile documents
doc_complete = [doc1, doc2, doc3, doc4, doc5]
doc_bow = [doc6, doc7]

stop = set(stopwords.words('english'))
exclude = set(string.punctuation) 
lemma = WordNetLemmatizer()
def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized

doc_clean = [clean(doc).split() for doc in doc_complete]

dictionary = corpora.Dictionary(doc_clean)
doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]

Lda = gensim.models.ldamodel.LdaModel

print(doc_term_matrix)
ldamodel = Lda(doc_term_matrix, num_topics=2, id2word = dictionary, passes=50)

print(ldamodel.print_topics(num_topics=2, num_words=5))

for doc in doc_bow:
    #label_list = [ldamodel.get_document_topics(doc, minimum_probability=None, minimum_phi_value=None, per_word_topics=False)]
    #label_list=[max(ldamodel.get_document_topics(doc, minimum_probability=None, minimum_phi_value=None, per_word_topics=False),key=lambda item: item[1])[0] for doc in doc_term_matrix]
    bow = dictionary.doc2bow(doc.split())
    t = ldamodel.get_document_topics(bow)
    maxi = 0.0
    tid = -1
    for ele in t:
        if ele[1]>maxi:
            maxi = ele[1]
            tid = ele[0]
    print(t)
    print(maxi, tid)
