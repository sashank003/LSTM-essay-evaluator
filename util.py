import os
import pandas as pd
import re
import numpy as np
from sklearn.metrics import confusion_matrix, cohen_kappa_score
from sklearn.model_selection import train_test_split, KFold
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.corpus import brown as allwords
from nltk.corpus import stopwords
from gensim.models import Word2Vec
from gensim.models import KeyedVectors

from keras.layers import Embedding, LSTM, Dense, Dropout, Lambda, Flatten
from keras.models import Sequential, load_model, model_from_config
import keras.backend as K
import pickle

b_size=32
i_size=350

def essay_to_wordlist(essay_v, remove_stopwords):
    essay_v = re.sub("[^a-zA-Z]", " ", essay_v)
    words = essay_v.lower().split()
    if remove_stopwords:
        stops = set(stopwords.words("english"))
        words = [w for w in words if not w in stops]
    return (words)

def makeFeatureVec(words, model, num_features):
    featureVec = np.zeros((num_features,),dtype="float32")
    num_words = 0.
    index2word_set = set(model.wv.index2word)
    for word in words:
        if word in index2word_set:
            num_words += 1
            featureVec = np.add(featureVec,model[word])        
    featureVec = np.divide(featureVec,num_words)
    return featureVec

def getAvgFeatureVecs(essay, model, num_features=i_size):
    counter = 0
    essayFeatureVecs = np.zeros((1,num_features),dtype="float32")
    essayFeatureVecs[counter] = makeFeatureVec(essay, model, num_features)
    return essayFeatureVecs

def get_model():
    model = Sequential()
    model.add(LSTM(i_size, dropout=0.5, recurrent_dropout=0.4, input_shape=[1, i_size], return_sequences=True))
    model.add(LSTM(120, dropout=0.4, recurrent_dropout=0.4, input_shape=[1,120], return_sequences=True))
    model.add(LSTM(b_size, recurrent_dropout=0.4))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='relu'))
    model.compile(loss='mean_squared_error', optimizer='rmsprop', metrics=['mae'])
    return model

"""import nltk

nltk.download('stopwords')"""



def final(file):
    filename = file
    script_location = os.path.dirname(os.path.abspath('__file__'))
    file_location = f"{script_location}\\files\\{filename}"
    df = pd.read_csv(file_location, names=['Essay'], encoding='mac_roman')
    test_essays=df.iloc[0]['Essay']

    model = KeyedVectors.load_word2vec_format(f"{script_location}\\word2vecmodel.bin", binary=True)

    testDataVecs = getAvgFeatureVecs(essay_to_wordlist( test_essays, remove_stopwords=True ), model)#, num_features)
    testDataVecs = np.array(testDataVecs)
    testDataVecs = np.reshape(testDataVecs, (testDataVecs.shape[0], 1, testDataVecs.shape[1]))

    lstm_model = get_model()
    lstm_model.load_weights(f"{script_location}\\final_lstm.h5")
    y_pred = lstm_model.predict(testDataVecs)
    y_pred = np.around(y_pred)
    final_answer=y_pred[0][0]
    return final_answer

