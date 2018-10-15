import nltk
from nltk.corpus import wordnet
from nltk.wsd import lesk
# Let's compare the noun of "ship" and "boat:"
 
##w1 = wordnet.synset('direct.s.08') # v here denotes the tag verb
##w2 = wordnet.synset('direct.a.07')
##print(w1.wup_similarity(w2))

##sent = ['I', 'want', 'clean', 'shirt']
##sent2 = ['My', 'clothing', 'was', 'good']
##synset = lesk(sent, 'shirt', 'n')
##synset2 = lesk(sent, 'clothing', 'n')
##print(synset.wup_similarity(synset2))
##print(synset)
##print(synset.name())
##print(type(synset.wup_similarity(synset2)))
##print(wordnet.synset(synset.name()).wup_similarity(wordnet.synset(synset2.name())))
##w1 = wordnet.synset('swallow.n.02')
##print(w1.definition())
##print(synset.name())

list_topics = set(['email', 'online',  'page', 'card', 'browser', 'error', 'assist', 'password', 'fee', 'online' , 'representative', 'staff', 'attendent', 'communication',  'message', 'on hold', 'spoke', 'spoken', 'rude', 'service', 'calling', 'desk', 'airport', 'agent','site', 'loading', 'phone', 'hang up'])

for each_topic in list_topics:
    syn = (wordnet.synsets(each_topic))
    for each_syn in syn:
        print(each_syn)
        print(each_syn.definition())
    
##set_of_n = set()
##sync_set = set()
####
##tweets = ['@VirginAmerica You\'d think paying an extra $100 bucks RT for luggage might afford you hiring an extra hand at @sfo #lame']
####
##for tweet in tweets:
##    tokenized = nltk.word_tokenize(tweet)
##    tagged = nltk.pos_tag(tokenized)
##
##    for element in tagged:
##        if element[1]=='NN' or element[1]=='NNS' or element[1]=='NNP' or element[1]=='NNPS':
##            set_of_n.add(element[0])
##
##for each_ele in set_of_n:
##    sync_set.add(lesk(tweet,each_ele,'n'))
##
##print(sync_set)
