
##Summary
The file consists of a sentiment text classifier with a Flask front end and an SQLAlchemy database. The file is run through main.py

To use this file please enquire about gaining access to the TSV review training and testing datasets or please use your own. I am uploading some of my own soon. 

There are some example reviews within main.py that are run when the file is run.

##Structure
The file consists of: 

- Flask front end within main.py 
- A sentiment analyser using vader 
- A accuracy determining analyser using vader
- A classifier model to be trained on the data to supply
- HTML templates for the construction of the Flask front end

##What data do I need to supply?
To prevent any re-structuring please use TSV files with 2 tabs. The first tab containing the labels and the second the reviews. 

For best use please use the 3 labels: [Poitive, Negative, Neutral] and classify your data training/testing data accordingly.

##
- Within the web app you can insert a sentence into the classifier to determine it's sentiment based on the training data. 
- You can compare this data with the basic out of the box sentiment analysers using Vader 
- These can be downloaded into an SQL Alchemy db or a text file. This can be optional and can be determined inside main.py if either are not wanted. 


#Installations:
I have installed the following:
flask_sqlalchemy
flask
wtforms
nltk
sklearn
vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer