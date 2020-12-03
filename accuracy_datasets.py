#File to determine the accuracy of datasets according to allocated sentiments

#imports
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import csv


#Sentiments given, this file only uses the testing data in this case.
sentiments = ['positive', 'negative', 'neutral']
filename = './testing.tsv'
analyzer = SentimentIntensityAnalyzer()


#Function to allocate each sentiment to a particular list according to sentiment.
def calculate_num_sentiments(sentiments):
    sentences = []
    for sentinment in sentiments:
        sentences.append([])
    return sentences

#This data prep does not clean the data as such, it simply sorts so the data can be looked at by the later methods.
def data_prep(sentences, filename, sentiments):
    with open(filename, encoding='utf-8') as tsvfile:
      reader = csv.DictReader(tsvfile, dialect='excel-tab')
      for row in reader:
          i = 0
          for sentiment in sentiments:
              if (row['label'] == sentiment):
                  sentences[i].append(row['sentence'])
              i += 1
    return sentences

# Method to determine the sentiment accuracy for each sentence. Uses the Vader out the box sentiment analyser
def determine_sentiment_accuracy(data, label):
    number = 0
    allocated_correctly = 0
    for sentence in data:
        vs = analyzer.polarity_scores(sentence)
        if (label == 'positive'):
            if not vs['neg'] > 0.05:
                if vs['pos'] - vs['neg'] > 0:
                    allocated_correctly += 1
                number += 1

        if (label == 'negative'):
            if not vs['pos'] > 0.05:
                if vs['pos'] - vs['neg'] <= 0:
                    allocated_correctly += 1
                number +=1

        if (label == 'neutral'):
            if vs['neu'] > 0.4:
                if vs['pos'] and vs['neg'] <= 0.75:
                    allocated_correctly += 1
                number +=1
    score = [number, allocated_correctly]
    return score

#method to calculate the accuracies of the sentiments given. Uses the above functions. Returns what is viewed on screen on the front end Flask
def calculate_accuracies(filename, sentiments):
    accuracies = []
    sentences = calculate_num_sentiments(sentiments)
    data = data_prep(sentences, filename, sentiments)
    i = 0
    for item in data:
        score = determine_sentiment_accuracy(data[i], sentiments[i])
        accuracies.append(sentiments[i].capitalize() + " accuracy = {}% via {} sentences of total {} sentences".format(round(score[1]/score[0]*100.0, 2), score[0], len(data[i])))
        i += 1

    return accuracies
