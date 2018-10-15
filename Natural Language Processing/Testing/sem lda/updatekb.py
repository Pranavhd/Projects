import nltk
from nltk.corpus import wordnet
from nltk.wsd import lesk
import operator

from nltk.corpus import stopwords 
from nltk.stem.wordnet import WordNetLemmatizer
import string
import gensim
from gensim import corpora

num_sem_words = 5
kb = set(['bag.n.01','bag.n.04'])

training_tweets = [' everything was fine until you lost my bag.',
          ' I don\'t understand why you need a DM to give me an answer on if you have a damaged luggage policy.',
          ' does that mean you don\'t have a policy for destroyed luggage?',
          ' We\'re on flight 910 Vegas to Boston today, checked in online but our bag count didn\'t register. Can I fix that somehow?',
          ' Luggage Suitcase bags',
          ' heyyyy guyyyys.. been trying to get through for an hour. can someone call me please? :/',
          ' your airline is awesome but your lax loft needs to step up its game. $40 for dirty tables and floors? http://t.co/hy0VrfhjHt',
          ' I need to register a service dog for a first class ticket from SFO &gt; Dulles. The phone queue is an hour or longer. Pls advise',
          ' You\'d think paying an extra $100 bucks RT for luggage might afford you hiring an extra hand at @sfo #lame']

testing_tweets = [' great job getting flight 28 in 10 minutes early. Too bad we\'re at 50 minutes and counting waiting for our bags.',
                  ' no, we are at a hotel.  Also, Jetblue lost my daughters luggage.  How do you lose luggage if the plane never actually left!!!',
                  ' called your service line and was hung up on. This is awesome. #sarcasm',
                  ' heyyyy guyyyys.. been trying to get through for an hour. can someone call me please? :/',
                  'we have a traveler whose bags did not make it on his flight. This is a very quick, turn-around trip (CLT to HPN) - what are our options? The personnel at the airport were not helpful at all. I can DM you the luggage tag if needed.']

for train_i in range(len(training_tweets)):
    tweet = training_tweets[train_i]
    tokenized = nltk.word_tokenize(tweet)
    tagged = nltk.pos_tag(tokenized)

    dict_kb = {}
    for each_know in kb:
        dict_kb[each_know] = 0.0
    
    set_of_n = set()
    set_of_v = set()
    sync_set = set()
    for element in tagged:
        if element[1]=='NN' or element[1]=='NNS' or element[1]=='NNP' or element[1]=='NNPS':
            set_of_n.add(element[0])
        if element[1]=='VB' or element[1]=='VBD' or element[1]=='VBG' or element[1]=='VBN' or element[1]=='VBP' or element[1]=='VBZ':
            set_of_v.add(element[0])
        if element[1]=='JJ' or element[1]=='JJR' or element[1]=='JJS':
            set_of_v.add(element[0])
        if element[1]=='RBR' or element[1]=='RB' or element[1]=='RBS' or element[1]=='WRB':
            set_of_v.add(element[0])

    for each_ele in set_of_n:
        ele_to_add = lesk(tweet,each_ele,'n')
        if ele_to_add is not None:
            sync_set.add(ele_to_add)
    for each_ele in set_of_v:
        ele_to_add = lesk(tweet,each_ele,'v')
        if ele_to_add is not None:
            sync_set.add(ele_to_add)

    set_update_kb = set()
    for each_know in kb:
        sync_each_know = wordnet.synset(each_know)
        for each_sync in sync_set:
            similarity = each_sync.wup_similarity(sync_each_know)
            if similarity is not None:
                dict_kb[each_know] += similarity
            if similarity > 0.85:
                set_update_kb.add(each_sync.name())

    kb = kb | set_update_kb
print(kb)
