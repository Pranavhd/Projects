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
kb = ['bag.n.01','bag.n.04','bag.n.05','bag.n.06','baggage.n.01','baggage.n.03','staff.n.01', 'staff.v.02','crew.n.01','gang.n.03','crew.v.01','seat.n.01','seat.v.01','seat.v.05','call.n.01','cry.n.01','call.n.04','call.n.09','call.v.03','call.v.05','call.v.03','support.n.02','support.n.01','support.n.11','support.v.01','booking.n.02','reservation.n.06','service.n.15','avail.n.01','service.n.04','service.n.02']

training_tweets = [' everything was fine until you lost my bag.',
          ' I don\'t understand why you need a DM to give me an answer on if you have a damaged luggage policy.',
          ' does that mean you don\'t have a policy for destroyed luggage?',
          ' We\'re on flight 910 Vegas to Boston today, checked in online but our bag count didn\'t register. Can I fix that somehow?',
          ' heyyyy guyyyys.. been trying to get through for an hour. can someone call me please? :/',
          ' your airline is awesome but your lax loft needs to step up its game. $40 for dirty tables and floors? http://t.co/hy0VrfhjHt',
          ' I need to register a service dog for a first class ticket from SFO &gt; Dulles. The phone queue is an hour or longer. Pls advise',
          ' You\'d think paying an extra $100 bucks RT for luggage might afford you hiring an extra hand at @sfo #lame']

testing_tweets = [' great job getting flight 28 in 10 minutes early. Too bad we\'re at 50 minutes and counting waiting for our bags.',
                  ' no, we are at a hotel.  Also, Jetblue lost my daughters luggage.  How do you lose luggage if the plane never actually left!!!',
                  ' called your service line and was hung up on. This is awesome. #sarcasm',
                  ' heyyyy guyyyys.. been trying to get through for an hour. can someone call me please? :/',
                  'we have a traveler whose bags did not make it on his flight. This is a very quick, turn-around trip (CLT to HPN) - what are our options? The personnel at the airport were not helpful at all. I can DM you the luggage tag if needed.']

set_of_adj = set()
set_of_adv = set()


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

    for each_know in kb:
        sync_each_know = wordnet.synset(each_know)
        for each_sync in sync_set:
            similarity = each_sync.wup_similarity(sync_each_know)
            if similarity is not None:
                dict_kb[each_know] += similarity

    sorted_dict = sorted(dict_kb.items(), key=operator.itemgetter(1),reverse=True)
    #print(sorted_dict)
    temp_string = ""
    for i in range(num_sem_words):
        dotted_word = sorted_dict[i][0]
        for j in range(len(dotted_word)):
            if dotted_word[j]=='.':
                temp_string += " " + dotted_word[:j]
                break
    training_tweets[train_i] += temp_string

##print("-----------------------------plz---------------------------------")
##for i in range(len(training_tweets)):
##    print(training_tweets[i])

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

doc_clean = [clean(tweet).split() for tweet in training_tweets]
dictionary = corpora.Dictionary(doc_clean)
doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]
Lda = gensim.models.ldamodel.LdaModel
ldamodel = Lda(doc_term_matrix, num_topics=2, id2word = dictionary, passes=250)
print(ldamodel.print_topics(num_topics=2, num_words=7))

for tweet in testing_tweets:
    doc = clean(tweet)
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
