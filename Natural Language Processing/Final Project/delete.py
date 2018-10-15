import pandas as pd
from nltk.corpus import wordnet

kb = set(['mesa.n.01'])

for each_know in kb:
    each_know = wordnet.synset(each_know)
    print(each_know.definition())