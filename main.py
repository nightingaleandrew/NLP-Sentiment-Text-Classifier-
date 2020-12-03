# Main file to be run. Please see README.txt if not already read.


#imports
from random import randint
import random
from time import strftime
import os

#installed files
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, flash, request, session
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

#Fellow files in dir
from classifier import dataPrep, runSystem, examples, predict_input, get_keywords
from independent_sentence_analysis import *
from accuracy_datasets import *

import config #config vars 

debug_mode = False #remember in debug mode, it initalises twice
secret_key = 'verysecretkey123lol' #secret key for Flash
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

#Class for config of the db using SQLAlchemy
class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, config.choose_filename_db)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

app.config.from_object(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

#Model of the db
class sentences(db.Model):
    _id = db.Column("Id", db.Integer, primary_key=True)
    time = db.Column("Time Added", db.String)
    label = db.Column("Classifier Label", db.String)
    sentence = db.Column("Sentence", db.String)
    independent = db.Column("Independent Vader Sentiment", db.String)

    def __init__(self, time, label, sentence, independent):
        self.time = time
        self.label = label
        self.sentence = sentence
        self.independent = independent

#Variables to not be changed, some checks etc, storage of sentences in test cases
testCases = [{ }]
id = 0
sentences_present = False

#For the accurcies of the dataset according to basic vader. Just using testing data in this case
accuracies = calculate_accuracies(config.testing_data, config.sentiments)

#Class for the form on screen
class InputForm(Form):
    sentence = TextField('Test Sentence:', validators=[validators.DataRequired()])

#Ensures that the ids in the text file are correct
def id_calculator(List_of_Dict):
    if (len(List_of_Dict) == 0):
        id = 0
    else:
        id = List_of_Dict[len(List_of_Dict) - 1]['id']
    return id

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

#Gets the timestamp for when the sentence is created
def get_time():
    time = strftime("%Y-%m-%dT%H:%M")
    return time

#Function to write the text file if wanted
def write_to_disk(id, sentence, label, filename, independent_sentiment):
    data = open(filename, 'a')
    timestamp = get_time()
    data.write('Id: {}, DateStamp: {}, Predicted Label: {}, Sentence Text: {}, Independent Sentiment: {} \n'.format(id, timestamp, label, sentence, independent_sentiment))
    data.close()

#Function that stores the sentence in a dictionary
def sentence_details(id, sentence, label, date, independent_sentiment):
    testCases.append({
        'id': id + 1,
        'text': sentence,
        'label': label,
        'independent_sentiment': independent_sentiment,
        'create_date': date,
    })

#Function to run the classifier
def create_classifier_func(testing_data, training_data):
    system = runSystem(testing_data, training_data) #As I am also returning the accuracy score
    model = system[0]
    accuracy = system[1]
    return model, accuracy

#Function to run the examples that were inputted
def run_examples(classifierSystem, sentences):
    example = examples(classifierSystem, sentences)
    return example

# Run the classifier and run the example sentences through it
classifier = create_classifier_func(config.testing_data, config.training_data)
exampleSentences = run_examples(classifier[0], config.example_sentences)
accuracy = classifier[1]

##top keywords for each sentiment
keywords = get_keywords(classifier[0], config.num, config.sentiments)

if ((config.create_db) and (not (os.path.isfile("./" + config.choose_filename_db)))): ##create database if not already created & add example files
    db.create_all()
    for example in exampleSentences:
        sentence = sentences(get_time(), example[1][0].capitalize(), example[0].capitalize(), reveal_scores(example[0]))
        db.session.add(sentence)
        db.session.commit()

if ((config.create_text_file) and (not (os.path.isfile("./" + config.choose_filename_txt)))): #If file present then the example sentences won't be added again
    id = 1
    for example in exampleSentences:
        write_to_disk(id, example[0].capitalize(), example[1][0].capitalize(), config.choose_filename_txt, reveal_scores(example[0]))
        id += 1

if (not sentences_present):
    id = 1
    for example in exampleSentences:
        sentence_details(id, example[0].capitalize(), example[1][0].capitalize(), get_time(), reveal_scores(example[0]))
        id += 1
sentences_present = True

#Run creation model before application starts
# @app.before_first_request

#Route with Post request as well as defualt Get
@app.route("/", methods=['GET', 'POST'])
def create():
    form = InputForm(request.form)
    if request.method == 'POST':
        sentence = request.form['sentence']
        if form.validate():
            #Flash message if sentences is validated okay
            flash("""Sentence Added: "{}" """.format(sentence))
            #Various varibles to setup the sentence info that was just inputted in by the user
            id = id_calculator(testCases)
            prediction = predict_input(sentence, classifier[0])
            independent_sentiment = reveal_scores(sentence)
            sentence_details(id, sentence.capitalize(), prediction[0].capitalize(), get_time(), independent_sentiment)
            id = file_len("./" + config.choose_filename_txt) + 1
            label = prediction[0].title()
            #Adds to text file if created
            if (config.create_text_file):
                write_to_disk(id, sentence.capitalize(), prediction[0].capitalize(), config.choose_filename_txt, independent_sentiment)
            #Adds to db if created by user
            if (config.create_db):
                sentence = sentences(get_time(), prediction[0].capitalize(), sentence.capitalize(), independent_sentiment)
                db.session.add(sentence)
                db.session.commit()
        else:
            #Flashes up in red that the sentence is needed - link to html
            flash('Error: Sentence required')

    #Passes through template html file, form & textCases which is the dict of examples
    return render_template('index.html', form = form, TestCases = testCases, accuracy = accuracy, accuracies=accuracies, keywords = keywords, num=config.num)

if __name__ == "__main__":
    app.secret_key = secret_key
    app.run(debug = debug_mode, host='127.0.0.1', port=4000)
