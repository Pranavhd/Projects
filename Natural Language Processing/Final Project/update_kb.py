import pandas as pd
import nltk
from nltk.corpus import wordnet
from nltk.wsd import lesk

kb = set(['bag.n.01','bag.n.04','bag.n.05','bag.n.06','baggage.n.01','baggage.n.03','wheel.n.01','steering_wheel.n.01','wheel.n.04',
'bicycle.n.01','wheel.v.01','wheel.v.02','wheel.v.03','misplace.v.01','lose.v.05','lose.v.06','lose.v.08','suffer.v.11','material.n.01','stuff.n.02','stuff.n.03','thrust.v.02','stuff.v.03','stuff.v.01','stuff.v.06',
'break.v.02','break.v.08','break_in.v.01','violate.v.01','better.v.01','fail.v.04','dampen.v.07',
'separate.v.08','collapse.v.01','break.v.39','break.v.41','break.v.45','break.v.49','crack.v.01','break.v.56',
'steal.v.01','lock.n.01','lock.v.01','lock_in.v.02',
'carry.n.01','transport.v.02','carry.v.02','hold.v.14','hold.v.11','dribble.v.03','carry.v.32','breakage.n.03','break.n.09',
'break.n.14','break.v.02','break.v.04','break.v.05','break.v.08','break.v.43','break.v.44','transportation_security_administration.n.01',
'miss.v.06','neglect.v.01','miss.v.08','drop.n.09','drop.v.01','drop.v.02','sink.v.01','drop.v.08',
'fell.v.01','spend.v.02','dangle.v.01','shed.v.01','clasp.n.02','hold.v.28','halt.v.01','apparel.n.01','dress.v.02','cargo.n.01',
'load.v.01','case.n.05','sheath.n.02','shell.n.08','casing.n.03','case.n.19','encase.v.01','deliver.v.02','hand_over.v.01',
'surrender.v.02','delivery.n.04','detect.v.01','recover.v.01','find.v.15','pocket.n.01','pouch.n.02','air_pocket.n.01',
'cabin.n.01','carousel.n.01','clothing.n.01','claim.n.04','check.v.01','match.v.01','price.n.02','blast.n.01','bang.n.02','gust.n.01','blast.n.04','blast.v.01', 'smash.v.01', 'blast.v.04', 'blast.v.07','blast.v.09', 'blast.v.10','guest.n.01', 'guest.n.03', 'sit.v.01','sit_down.v.01', 'ride.v.01', 'sit.v.07', 'baby-sit.v.02', 'seat.v.01', 'sit.v.10','seat.n.01', 'seat.n.03','seat.n.04', 'seat.v.01','seat.v.02','seat.v.04','seat.v.05','seat.v.06','seat.v.07','vent.n.01','release.n.09','vent.v.01','vent.v.02','television_receiver.n.01','cancel.v.01','cancel.v.03','delete.v.01','cancel.v.05','off.a.03','flight.n.01','flight.n.02','escape.n.01','trajectory.n.01','flight.n.09','business.n.01','commercial_enterprise.n.02','occupation.n.01','clientele.n.01','direct.v.01','target.v.01','direct.v.04','lead.v.01','send.v.01','aim.v.01','conduct.v.02','direct.v.09','steer.v.01','stop.n.03','people.n.01','citizenry.n.01','people.n.03','multitude.n.03','peep.v.01','peep.v.02','peep.v.04','peep.v.05','airplane.n.01','plane.v.02','stop.n.01','stop.n.02','stop.n.03','arrest.n.02','stop.n.05','stop_consonant.n.01','stop.v.01','discontinue.v.01','stop.v.03','stop.v.04','stop.v.05','intercept.v.01','end.v.01','barricade.v.01','hold_on.v.02','weather.n.01','weather.v.04','premium.n.01','premium.n.04','fly.v.01','fly.v.02','fly.v.03','fly.v.04','fly.v.05','fly.v.08','fly.v.09','fly.v.10','fly.v.12','across.r.01','across.r.02','state.n.04','country.n.02','nation.n.02','country.n.04','area.n.01','flee.v.01','vanish.v.05','ascent.n.01','upgrade.n.03','upgrade.v.01','promote.v.02','upgrade.v.04','upgrade.v.05','offer.v.01','volunteer.v.02','offer.v.04','offer.v.06','offer.v.07','put_up.v.02','extend.v.04','wait.n.02','wait.v.01','expect.v.03','wait.v.04','desk.n.01','airport.n.01','landing.n.03','landing.n.04','land.v.02','land.v.04','telling.n.02','lean_back.v.01','recline.v.02','recumb.v.01','web_site.n.01','drink.n.01','drink.n.02','beverage.n.01','swallow.n.02','drink.v.01','drink.v.02','drink.v.05','mechanical.a.02','reschedule.v.01','passenger.n.01','seating.n.01','seat.v.01','seat.v.02','seat.v.04','seat.v.05','seat.v.07','row.n.01','quarrel.n.01','choose.v.01','turbulence.n.01','turbulence.n.02'])

df = pd.read_csv('Bag.csv')
#df2 = pd.read_csv('Flight.csv')
#df3 = pd.read_csv('Service.csv')
training_tweets = df['text'].tolist()
#training_tweets.extend(df2['text'].tolist())
#training_tweets.extend(df3['text'].tolist())

print(len(training_tweets))

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
        if element[1] == 'NN' or element[1] == 'NNS' or element[1] == 'NNP' or element[1] == 'NNPS':
            set_of_n.add(element[0])
        if element[1] == 'VB' or element[1] == 'VBD' or element[1] == 'VBG' or element[1] == 'VBN' or element[
            1] == 'VBP' or element[1] == 'VBZ':
            set_of_v.add(element[0])
        if element[1] == 'JJ' or element[1] == 'JJR' or element[1] == 'JJS':
            set_of_v.add(element[0])
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

    set_update_kb = set()
    set_update_kb_85 = set()
    for each_know in kb:
        sync_each_know = wordnet.synset(each_know)
        for each_sync in sync_set:
            similarity = each_sync.wup_similarity(sync_each_know)
            # if similarity is not None:
            #     dict_kb[each_know] += similarity
            if similarity > 0.80:
                set_update_kb.add(each_sync.name())
                if similarity > 0.85:
                    set_update_kb_85.add(each_sync.name())

    kb = kb | set_update_kb
print(kb)
print(set_update_kb_85)