##from summa import keywords
from summa import summarizer
import nltk
from nltk.corpus import wordnet
from nltk.wsd import lesk
# Let's compare the noun of "ship" and "boat:"
 
##w1 = wordnet.synset('food.n.01') # v here denotes the tag verb
##w2 = wordnet.synset('food.n.02')
##print(w1.wup_similarity(w2))

##sent = ['The', 'drink', 'is', 'good']
##synset = lesk(sent, 'drink', 'n')
##print(synset)
##w1 = wordnet.synset('swallow.n.02')
##print(w1.definition())
##print(synset.name())

##list_topics = ['Food','Staff','Baggage']
##
##for each_topic in list_topics:
##    syn = (wordnet.synsets(each_topic))
##    for each_syn in syn:
##        print(each_syn)
##        print(each_syn.definition())
    
##set_of_n = set()
##sync_set = set()
##
tweets = ['@VirginAmerica You\'d think paying an extra $100 bucks RT for luggage might afford you hiring an extra hand at @sfo #lame',
'@VirginAmerica  for all my flight stuff wrong and did nothing about it. Had #worst #flight ever',
'@VirginAmerica husband and I ordered three drinks via my screen and they never came. Awesome!',
'@VirginAmerica All of group E was told there was no more room in the bins. when I got on the plane, was room for at least 4 bags in my row!',
'@united yes, we\'ve been with the agents for the last 50 minutes. One of the agents have been very rude, but thankfully Ladan has been nice.',
'@united iah to charlotte. Baggage claim rep latrice h. #customerservice non existent, Ignored customer then inappropriately touched customer',
'@united v upset with your disability  "services". When I told one of your employees I was carrying medical equipment she was very rude.',
'@united silly I\'m flying delta today. Your united club staff and attendants are surly and unhelpful and always seem bothered by pesky folk']

for tweet in tweets:
    print(summarizer.summarize(text))
##    print(keywords.keywords(text))
    print("-----------------------------")

##
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
