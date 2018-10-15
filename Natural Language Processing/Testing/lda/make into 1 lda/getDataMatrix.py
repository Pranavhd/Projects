#nltk.download('stopwords')

from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import csr_matrix
import scipy.sparse
import pandas as pd
import csv
import re
import string
import math
import numpy as np
from nltk.corpus import stopwords
from datetime import datetime
from scipy.sparse import csr_matrix
from nltk.stem import PorterStemmer

stop_words = list(stopwords.words('english'))
port = PorterStemmer()
def main(path): 
	dataFrame = pd.read_csv(path)
	#getting date in "%Y-%m-%dT%H:%M:%S.%fZ" format
	dataFrame["DateTime"] = dataFrame["Date"].map(str) + 'T'+ dataFrame["Hour"] + ':00.00Z'

	tweetdatalist = list(dataFrame.loc[:, "Tweet content"])
	tweettimelist = list(dataFrame.loc[:, "DateTime"])
	rtlist = list(dataFrame.loc[:, "RTs"])
	followerslist = list(dataFrame.loc[:, "Followers"])

	vocabularylist = list(build_lexicon(tweetdatalist))
	vectorizer = TfidfVectorizer(min_df=1, vocabulary=vocabularylist)
	tfidfvector= vectorizer.fit_transform(tweetdatalist)

	timenormlist = []
	rtnormlist = []
	followersnormlist = []
	size = len(tweettimelist)
	min_tweet_time =  datetime.strptime(min(tweettimelist), "%Y-%m-%dT%H:%M:%S.%fZ")
	max_tweet_time =  datetime.strptime(max(tweettimelist), "%Y-%m-%dT%H:%M:%S.%fZ")
	range_tweet_time = (max_tweet_time - min_tweet_time).total_seconds()
	max_rt = max(rtlist)
	max_followers = max(followerslist)

	for i in range(0, size):
		time_diff = (datetime.strptime(tweettimelist[i], "%Y-%m-%dT%H:%M:%S.%fZ") - min_tweet_time).total_seconds()
		timenormlist.append(1+(float(time_diff)/range_tweet_time))
		if math.isnan(rtlist[i]):
			rtnormlist.append(1)
		else:
			rtnormlist.append(1+ float(rtlist[i])/float(max_rt))
		if math.isnan(followerslist[i]):
			followersnormlist.append(1)
		else:
			followersnormlist.append(1+float(followerslist[i])/float(max_followers)) 

	rows,cols = tfidfvector.nonzero()

	for row,col in zip(rows,cols):
	    tfidfvector[row,col] = float(tfidfvector[row,col])*timenormlist[row]*rtnormlist[row]*followersnormlist[row]
	    
	scipy.sparse.save_npz(path[:-5]+'.npz', tfidfvector)
	feature_list = vectorizer.get_feature_names()
	#print(feature_list)
	return tfidfvector, feature_list 

def method2(path): 
	dataFrame = pd.read_csv(path)
	#getting date in "%Y-%m-%dT%H:%M:%S.%fZ" format
	dataFrame["DateTime"] = dataFrame["Date"].map(str) + 'T'+ dataFrame["Hour"] + ':00.00Z'

	tweetdatalist = [" ".join([port.stem(i) for i in doc.split()]) for doc in dataFrame.loc[:, "Tweet content"]]
	tweettimelist = list(dataFrame.loc[:, "DateTime"])
	rtlist = list(dataFrame.loc[:, "RTs"])
	followerslist = list(dataFrame.loc[:, "Followers"])

	vocabularylist = list(build_lexicon_method2(tweetdatalist))
	vectorizer = TfidfVectorizer(min_df=1, vocabulary=vocabularylist)
	tfidfvector= vectorizer.fit_transform(tweetdatalist)

	timenormlist = []
	rtnormlist = []
	followersnormlist = []
	size = len(tweettimelist)
	min_tweet_time =  datetime.strptime(min(tweettimelist), "%Y-%m-%dT%H:%M:%S.%fZ")
	max_tweet_time =  datetime.strptime(max(tweettimelist), "%Y-%m-%dT%H:%M:%S.%fZ")
	range_tweet_time = (max_tweet_time - min_tweet_time).total_seconds()
	max_rt = max(rtlist)
	max_followers = max(followerslist)

	for i in range(0, size):
		time_diff = (datetime.strptime(tweettimelist[i], "%Y-%m-%dT%H:%M:%S.%fZ") - min_tweet_time).total_seconds()
		timenormlist.append(1+(float(time_diff)/range_tweet_time))
		if math.isnan(rtlist[i]):
			rtnormlist.append(1)
		else:
			rtnormlist.append(1+ float(rtlist[i])/float(max_rt))
		if math.isnan(followerslist[i]):
			followersnormlist.append(1)
		else:
			followersnormlist.append(1+float(followerslist[i])/float(max_followers)) 

	rows,cols = tfidfvector.nonzero()

	for row,col in zip(rows,cols):
	    tfidfvector[row,col] = float(tfidfvector[row,col])*timenormlist[row]*rtnormlist[row]*followersnormlist[row]
	    
	scipy.sparse.save_npz(path[:-5]+'.npz', tfidfvector)
	feature_list = vectorizer.get_feature_names()
	#print(feature_list)
	return tfidfvector, feature_list 
	
def build_lexicon_method2(corpus):
    lexicon = set() 
    positive_words = [port.stem(word) for word in read_words('positive-words.txt')]
    negative_words = [port.stem(word) for word in read_words('negative-words.txt')]
    for doc in corpus:
        #removing links
        doc = re.sub(r'http\S+','', doc)        
        #remove punctuation
        doc = doc.translate(None, string.punctuation)               
        list_of_words_n_doc = doc.split()
        lexicon.update([word for word in list_of_words_n_doc if word in positive_words or word in negative_words])
    return lexicon

def read_words(words_file):
    return [word for line in open(words_file, 'r') for word in line.split()]

def build_lexicon(corpus):
    lexicon = set()    
    for doc in corpus:
        #removing links
        doc = re.sub(r'http\S+','', doc)        
        #remove punctuation
        doc = doc.translate(None, string.punctuation)               
        list_of_words_n_doc = doc.split()
        lexicon.update([word for word in list_of_words_n_doc if not word in stop_words])
    return lexicon

if __name__ == "__main__":
    main(path)
    