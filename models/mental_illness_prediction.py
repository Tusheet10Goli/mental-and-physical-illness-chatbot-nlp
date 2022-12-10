from email import message
from pyexpat.errors import messages
from itsdangerous import exc
from numpy import vectorize
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
# from pip_datasets import EMOTION_TEST_PATH, EMOTION_TRAIN_PATH
import joblib
import os
import platform 



#Define Constants
CURR_FILE = os.path.abspath(__file__)
CURR_DIR = CURR_FILE[:CURR_FILE.rfind('/') + 1]
if platform.system() == 'Windows':
    CURR_DIR = CURR_FILE[:CURR_FILE.rfind('\\') + 1]
LR_CLASSIFIER_SAVE_PATH = CURR_DIR + 'mip_classifier_logistic_regression.joblib'
LR_VECTORIZER_SAVE_PATH = CURR_DIR + 'mip_vectorizer_logistic_regression.joblib'


def mip_train_classifier():
    #Read in the data
    df = pd.read_csv('datasets/sentiment_analysis/emotions_dataset_for_nlp/train.txt', names=['text', 'sentiment'], delimiter=';')
    df2 = pd.read_csv('datasets/sentiment_analysis/emotions_dataset_for_nlp/test.txt', names=['text', 'sentiment'], delimiter=';')

    samplesTrain = df['text'].values
    yTrain = df['sentiment'].values
    samplesTest = df2['text'].values
    yTest = df2['sentiment'].values

    vectorizer = CountVectorizer()
    vectorizer.fit(samplesTrain)

    X_train = vectorizer.transform(samplesTrain)
    X_test = vectorizer.transform(samplesTest)

    classifer = LogisticRegression()
    classifer.fit(X_train, yTrain)
    accuracy = classifer.score(X_test, yTest)
    print("Accuracy: ", accuracy)
    return classifer, vectorizer


def mip_predict(messageList):
    try:
        # load existing model for symptom extraction
        # print('Loading existing logistic regression classifier for mip...')
        classifier = joblib.load(LR_CLASSIFIER_SAVE_PATH)
        vectorizer = joblib.load(LR_VECTORIZER_SAVE_PATH)
        x_new = vectorizer.transform(messageList)
        return classifier.predict(x_new)
    except:
        # print('Creating new logistic regression classifer for mip...')
        classifier, vectorizer = mip_train_classifier()
        if (type(messageList) is str):
            messageList = [messageList]
        x_new = vectorizer.transform(messageList)
        joblib.dump(classifier, LR_CLASSIFIER_SAVE_PATH)
        joblib.dump(vectorizer, LR_VECTORIZER_SAVE_PATH)
        return classifier.predict(x_new)


def build_mip_response(user_messages):
    # mip_predictions = mip_predict(user_messages)
    # mip_predictions_list = mip_predictions.tolist()
    # sadnessCount = mip_predictions_list.count('sadness')
    # joyCount = mip_predictions_list.count('joy')
    # fearCount = mip_predictions_list.count('fear')

    if type(user_messages) != list: 
        user_messages = [user_messages]

    predictions = []
    for message in user_messages:
        message = message.replace('?', '.')
        message = message.replace('!', '.')
        parts = message.split('.')

        curPrediction = mip_predict(parts)
        curPredictionList = curPrediction.tolist()
        sadnessCount = curPredictionList.count('sadness')
        joyCount = curPredictionList.count('joy')
        fearCount = curPredictionList.count('fear')

    #Options: Depression, Bipolar Disorder, Anxiety
        TOP_PREDICTION = ""
        if sadnessCount > (len(curPredictionList) / 2) or (sadnessCount > joyCount and sadnessCount > fearCount):
            TOP_PREDICTION = "Depression"

        elif (sadnessCount > (len(curPredictionList) / 3) or fearCount > (len(curPredictionList) / 3)) \
                and joyCount > (len(curPredictionList) / 3):
            TOP_PREDICTION = "Bipolar Disorder"
        elif fearCount > (len(curPredictionList) / 2) or (fearCount > joyCount and fearCount > sadnessCount):
            TOP_PREDICTION = "Anxiety"

        else:
            TOP_PREDICTION = "No Mental Illness"



        mip_response = TOP_PREDICTION
        predictions.append(mip_response)
    
    return predictions



#messages = ['I hate everything and I feel alone', 'I woke up in a sad mood today and felt down', 'I am always crying and am sad all the time']

#result = build_mip_response(messages)
#print(result)

#print("Cur path: ")
#print(CURR_FILE)
#print ("Cur directory")
#print(CURR_DIR)