#Determining whether the sentence is positive or negative using vader. This is independent to the classifier used.

#imports
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

#Sentence
# sentence = "profits increased by 100% last year"

#Function to decide the sentiment of the statement accoridng to vader
def decide_sentiment(sentence):
    # Create a SentimentIntensityAnalyzer object.
    sid_obj = SentimentIntensityAnalyzer()
    # polarity_scores method of SentimentIntensityAnalyzer, oject gives a sentiment dictionary, which contains pos, neg, neu, and compound scores.
    sentiment_dict = sid_obj.polarity_scores(sentence)

    #Provide the sentiment based on the compound rating
    if sentiment_dict['compound'] >= 0.05 :
        print(sentiment_dict['compound'])
        sentiment = "Positive"
    elif sentiment_dict['compound'] <= - 0.05 :
        print(sentiment_dict['compound'])
        sentiment = "Negative"
    else :
        print(sentiment_dict['compound'])
        sentiment = "Neutral"

    #Present the scores
    # print("Overall for: '" + sentence + "': " + sentiment)
    # print("Breakdown: |" + str(round(sentiment_dict['pos']*100, 2)), "% Positive |" + str(round(sentiment_dict['neg']*100, 2)) + "% Negative |" + str(round(sentiment_dict['neu']*100, 2)) + "% Neutral |" )
    # print("")

#Function returns the overall sentiment & not breakdown
def return_sentiment(sentence):
    sid_obj = SentimentIntensityAnalyzer()
    sentiment_dict = sid_obj.polarity_scores(sentence)

    if sentiment_dict['compound'] >= 0.05 :
        sentiment = "Positive"
    elif sentiment_dict['compound'] <= - 0.05 :
        sentiment = "Negative"
    else :
        sentiment = "Neutral"
    return sentiment

#To run the sentiment function for the sentence
def reveal_scores(sentence):
    result = return_sentiment(sentence)
    return result

# # Run Main
# if __name__ == "__main__" :
#     #Run reveal Scores method
#     reveal_scores(sentence)
