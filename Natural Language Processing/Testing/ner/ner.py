import nltk
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet
import re
import string

eg = ['@VirginAmerica  I flew from NYC to SFO last week and couldn\'t fully sit in my seat due to two large gentleman on either side of me. HELP!',
      '@united so you\'re telling me there is no number to call after being left in an airport because of a negligent pilot and staff?']

stop = set(stopwords.words('english'))
exclude = set(string.punctuation) 
lemma = WordNetLemmatizer()

w1 = wordnet.synset('pizza') # v here denotes the tag verb
w2 = wordnet.synset('food')
print(w1.wup_similarity(w2))

##for doc in eg:
##    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
##    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
##    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
##
##    print(normalized)
##    tokenized = nltk.word_tokenize(normalized)
##    tagged = nltk.pos_tag(tokenized)
##    print(tagged)

##    chunkGram = r"""Chunk: {<NNP>*<NP>*<NN>*}"""
##    chunkParser = nltk.RegexpParser(chunkGram)
##
##    chunked = chunkParser.parse(tagged)
##    print(chunked)
##    chunked.draw()

##    namedEnt = nltk.ne_chunk(tagged, binary = False)
##    print(namedEnt)
    
##    namedEnt.draw()
