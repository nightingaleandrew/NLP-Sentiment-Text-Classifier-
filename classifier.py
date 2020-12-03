#This is the classifier file. The sentences below are not used for the wider application from main.py but can be used if this is run on it's own.
#Firstly I clean the data using a lemmatizer rather than a stemmer due to the fact that it's intelligence in converting words to their root than savegly chopping them. Stop words are also removed.
#
#Imports
import pandas as pd
import re
import csv
import numpy as np

from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import SelectKBest, chi2

from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer

#Method to clean the data - Lemmiziser used rather than stemmer & stop words/numbers removed, put in lowercase too
def dataPrep(file):
    all_data = []
    with open(file, encoding='utf-8') as tsvfile:
      reader = csv.DictReader(tsvfile, dialect='excel-tab')
      for row in reader:
        data_row = [row['label'], row['sentence']]

        all_data.append(data_row)
    data = pd.DataFrame(all_data) #Adds it to a panda dataframe for ease of use

    words = stopwords.words("english")
    lemmatizer = WordNetLemmatizer()

    data['cleaned'] = data[1].apply(lambda x: " ".join([lemmatizer.lemmatize(i) for i in re.sub("[^a-zA-Z]", " ", x).split() if i not in words]).lower())
    return data

#Method that firstly provides the test and train data to the classifier.
def runSystem(testing_data, training_data):
    testData = dataPrep(testing_data)
    trainData = dataPrep(training_data)

    X_train, y_train = (trainData['cleaned'], trainData[0])
    X_test, y_test = (testData['cleaned'], testData[0])

    #model
    pipeline = Pipeline([('vect', TfidfVectorizer(ngram_range=(1, 2), stop_words="english", sublinear_tf=True)), #tfidf weights words, uncommon words get greater weight - tries to get rid of unrelevent words that are not included in stop words but similar to stop words
                         ('chi',  SelectKBest(chi2, k=10000)),
                         ('clf', LinearSVC(penalty='l1', max_iter=1000, dual=False))])

    #I try to understand double negative reviews eg. company had not good sales this year through using ngrams on every other word (1, 2)
    model = pipeline.fit(X_train, y_train)
    accuracy = round((model.score(X_test, y_test)*100), 2)
    return model, accuracy

#This method pulls the top so many key words. The key words are defined in main.py They are then presented on the Flask front end.
def get_keywords(model, num, sentiments):
    vectorizer = model.named_steps['vect']
    chi = model.named_steps['chi']
    clf = model.named_steps['clf']

    feature_names = vectorizer.get_feature_names()
    feature_names = [feature_names[i] for i in chi.get_support(indices=True)]
    feature_names = np.asarray(feature_names)

    # print("top 10 keywords per sentiment:") ##title to print words in cmd if wanted
    # target_names = ['negative', 'neutral', 'positive']
    keywords = []
    for i, label in enumerate(sentiments):
        top = np.argsort(clf.coef_[i])[-num:]
        # print("%s: %s" % (label, " ".join(feature_names[top]))) ##Print the words in the cmd
        keywords.append(label.capitalize() + ": " + ", ".join(feature_names[top]))
    return keywords

#Method to return the results i.e sentiment predicted & sentence itself from a list of sentences eg. at the top of this file or the example reviews in main.py
def examples(model, sentence):
    results = []
    for item in sentence:
        result = []
        result.append(item)
        result.append(model.predict([item]))
        results.append(result)
    return results

#Method to simply return the prediction
def predict_input(sentence, model):
    prediction = model.predict([sentence])
    return prediction
