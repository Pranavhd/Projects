import nltk
from nltk.corpus import wordnet
from nltk.wsd import lesk
import operator
import pandas as pd
import time

from nltk.corpus import stopwords 
from nltk.stem.wordnet import WordNetLemmatizer
import string
import gensim
from gensim import corpora

start_time = time.time()
num_sem_words = 7

kb = set(['bag.n.01','bag.n.04','bag.n.05','bag.n.06','baggage.n.01','baggage.n.03','staff.n.01', 'lost.a.01','dress.v.02','dress.v.10','dress.v.02','break.v.02','clothing.n.01','apparel.n.01','staff.v.02','seat.n.01','seat.v.01','seat.v.05','call.n.01','support.n.02','support.n.01','support.n.11','support.v.01','booking.n.02','reservation.n.06','avail.n.01','internet.n.01', 'engagement.n.05', 'booking.n.02', 'reserve.v.04', 'answer.v.01', 'answer.v.02', 'answer.v.03', 'answer.v.05', 'answer.v.08', 'answer.v.09', 'answer.v.10',  'answer.n.01', 'solution.n.02', 'answer.n.03', 'answer.n.05', 'service.n.01', 'service.n.02', 'service.n.05', 'avail.n.01', 'overhaul.n.01', 'service.n.15', 'call.n.01', 'cry.n.01', 'call.n.06', 'call.n.09', 'name.v.01', 'call.v.03', 'shout.v.02', 'call.v.05', 'visit.v.03', 'call.v.07', 'call.v.09', 'call.v.10', 'call.v.11', 'address.v.06', 'bid.v.04', 'call.v.23', 'call.v.24', 'call.v.25', 'telephone.n.01', 'earphone.n.01', 'chat.n.01', 'support.n.01', 'support.n.02', 'web_site.n.01', 'table.n.02', 'table.n.03', 'floor.n.01', 'floor.n.06', 'shock.v.01', 'customer.n.01', 'services.n.01', 'service.v.01', 'service.v.02', 'speak.v.03', 'address.v.02', 'reservation.n.01', 'reservation.n.05', 'reservation.n.06', 'reservation.n.07', 'hang.v.01', 'hang.v.02', 'hang.v.04', 'hang.v.08', 'cling.v.03', 'ticket.n.01', 'tag.n.01', 'ticket.v.02', 'class.n.01', 'class.n.03', 'class.n.08', 'classify.v.01', 'web.n.01', 'network.n.01', 'world_wide_web.n.01', 'reply.n.02', 'aid.n.02', 'talk.v.02', 'talk.v.01', 'communication.n.01', 'agent.n.02', 'message.n.01', 'message.v.03', 'staff.n.01', 'fee.n.01', 'service.n.02', 'electronic_mail.n.01', 'e-mail.v.01', 'on-line.a.02', 'help.v.01', 'desk.n.01', 'password.n.01', 'card.n.02', 'error.n.06', 'browser.n.02'])

df = pd.read_csv('Bag.csv')
df2 = pd.read_csv('Flight.csv')
df3 = pd.read_csv('Service.csv')
#df4 = pd.DataFrame()
#df5 = pd.DataFrame()
#df6 = pd.DataFrame()
#dfannon = pd.read_csv('Annoted_Training_Tweets_13_semwords.csv')
#df_input = pd.read_csv('Input_Tweets.csv')
df_senti = pd.DataFrame()
df_inter = pd.DataFrame()
# df_inter = pd.read_csv('Interim.csv')
# df_clean = pd.DataFrame()
#df_clean = pd.read_csv('Interim_clean.csv')


df_Bag = df
df_Flight = df2
# df_Bag_test = df[630:]
# df_Flight_test = df2[2615:]
# len_df3 = int(0.8*float(len(df3['text'].tolist())))
df_Service = df3
# df_Service_test = df3[len_df3:]

list_text = []
list_topic = []
# list_sentiment = []
# list_text_Bag = []
# list_text_Flight = []
# list_text_Service = []

training_tweets = df_Bag['text'].tolist()
training_tweets.extend(df_Flight['text'].tolist())
training_tweets.extend(df_Service['text'].tolist())
# training_tweets = df_inter['text'].tolist()

##testing_tweets = df_Bag_test['text'].tolist()
##testing_tweets = df_input['text'].tolist()
testing_tweets = []

topics = ['bag','flight']

set_of_adv = set()

def strip_all_entities(text):
    entity_prefixes = ['@', '#', 'virgin', 'america', 'united', 'delta', 'jetblue', 'southwest']
    for separator in string.punctuation:
        if separator not in entity_prefixes:
            text = text.replace(separator, " ")
    words = []
    for word in text.split():
        word = word.strip()
        if word:
            if word[0] not in entity_prefixes:
                # words.append(" ")
                words.append(word)
            # print(type(''.join(words)))
    return " ".join(words)

for train_i in range(len(training_tweets)):
    tweet = training_tweets[train_i]
    tweet = strip_all_entities(tweet)
    tokenized = nltk.word_tokenize(tweet)
    tagged = nltk.pos_tag(tokenized)

    dict_kb = {}
    for each_know in kb:
        dict_kb[each_know] = 0.0

    set_of_n = set()
    set_of_v = set()
    set_of_adj = set()
    sync_set = set()
    for element in tagged:
        if element[1]=='NN' or element[1]=='NNS' or element[1]=='NNP' or element[1]=='NNPS':
            set_of_n.add(element[0])
        if element[1]=='VB' or element[1]=='VBD' or element[1]=='VBG' or element[1]=='VBN' or element[1]=='VBP' or element[1]=='VBZ':
            set_of_v.add(element[0])
        if element[1]=='JJ' or element[1]=='JJR' or element[1]=='JJS':
            set_of_adj.add(element[0])
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
    for each_ele in set_of_adj:
        ele_to_add = lesk(tweet, each_ele, 'a')
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

print("--- %s seconds ---" % (time.time() - start_time))
df_inter['text'] = pd.Series(training_tweets)
df_inter.to_csv('Interim_7_words.csv')

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

# df_clean['text'] = pd.Series(doc_clean)
# df_clean.to_csv('Interim_clean.csv')

print("--- %s seconds ---" % (time.time() - start_time))

dictionary = corpora.Dictionary(doc_clean)
doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]

Lda = gensim.models.ldamodel.LdaModel
ldamodel = Lda(doc_term_matrix, num_topics=3, id2word = dictionary, passes=350)
ldamodel.save('Model_phase_3_7_words')

# ldamodel = gensim.models.LdaModel.load('final_model_phase_3')
print(ldamodel.print_topics(num_topics=3, num_words=9))

dict_topic_number = {}
dict_prediction = {}
dict_prediction[0] = 0
dict_prediction[1] = 0
dict_prediction[2] = 0

temp_set = set([0,1,2])
for tweet in topics:
    doc = clean(tweet)
    bow = dictionary.doc2bow(doc.split())
    t = ldamodel.get_document_topics(bow)
    maxi = 0.0
    tid = -1
    for ele in t:
        if ele[1]>maxi:
            maxi = ele[1]
            tid = ele[0]
    dict_topic_number[int(tid)] = tweet
    temp_set.remove(int(tid))

temp_tid = int(temp_set.pop())
dict_topic_number[temp_tid] = 'service'
print(dict_topic_number)

print("--- %s seconds ---" % (time.time() - start_time))
print("Enter number of testing tweets")
number = int(input())
for i in range(number):
    print("Enter input tweet")
    #find sentiment of each tweet here, store in sentiment_value
    tweet = input()

    tweet = strip_all_entities(tweet)
    tokenized = nltk.word_tokenize(tweet)
    tagged = nltk.pos_tag(tokenized)

    set_of_n = set()
    set_of_v = set()
    set_of_adj = set()
    sync_set = set()
    for element in tagged:
        if element[1] == 'NN' or element[1] == 'NNS' or element[1] == 'NNP' or element[1] == 'NNPS':
            set_of_n.add(element[0])
        if element[1] == 'VB' or element[1] == 'VBD' or element[1] == 'VBG' or element[1] == 'VBN' or element[
            1] == 'VBP' or element[1] == 'VBZ':
            set_of_v.add(element[0])
        if element[1] == 'JJ' or element[1] == 'JJR' or element[1] == 'JJS':
            set_of_adj.add(element[0])
        if element[1] == 'RBR' or element[1] == 'RB' or element[1] == 'RBS' or element[1] == 'WRB':
            set_of_v.add(element[0])

    for each_ele in set_of_n:
        ele_to_add = lesk(tweet, each_ele, 'n')
        if ele_to_add is not None:
            sync_set.add(ele_to_add)
    for each_ele in set_of_v:
        ele_to_add = lesk(tweet, each_ele, 'v')
        if ele_to_add is not None:
            sync_set.add(ele_to_add)
    for each_ele in set_of_adj:
        ele_to_add = lesk(tweet, each_ele, 'a')
        if ele_to_add is not None:
            sync_set.add(ele_to_add)

    for each_know in kb:
        sync_each_know = wordnet.synset(each_know)
        for each_sync in sync_set:
            similarity = each_sync.wup_similarity(sync_each_know)
            if similarity is not None and float(similarity)>0.80:
                dotted_word = each_sync.name()
                temp_string = ""
                for j in range(len(dotted_word)):
                    if dotted_word[j] == '.':
                        temp_string += " " + dotted_word[:j]
                        break
                tweet += temp_string
    doc = clean(tweet)
    bow = dictionary.doc2bow(doc.split())
    t = ldamodel.get_document_topics(bow)
    maxi = 0.0
    tid = -1
    for ele in t:
        if ele[1]>maxi:
            maxi = ele[1]
            tid = ele[0]
    dict_prediction[int(tid)] += 1
    topic_name = dict_topic_number[int(tid)]
    list_text.append(tweet)
    list_topic.append(topic_name)
    #list_sentiment.append(sentiment_value)
    print(topic_name)
    print("--- %s seconds ---" % (time.time() - start_time))


df_senti['text'] = pd.Series(list_text)
df_senti['topic'] = pd.Series(list_topic)
#df_senti['sentiment'] = pd.Series(list_sentiment)
df_senti.to_csv('Output_Final_phase.csv')

#ldamodel.save('final_model_phase_3')
print("--- %s seconds ---" % (time.time() - start_time))
