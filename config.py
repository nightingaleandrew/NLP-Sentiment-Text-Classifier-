#Config file for the sentiment text classifer 


#Setting up storage (All the sentences are stored in a dict if you do not want to create a db or txt file. On screen, it comes from the dict as might not want to create db or txt file)
create_db = True #Let the program know if you would like to create a DB
create_text_file = True #Let the program know if you would like ot create a text_file
##files
testing_data = './testing.tsv' #testing file
training_data = './training.tsv' #training data file
#Further variables
choose_filename_db = 'sentences.db' #alter name of the database
choose_filename_txt = 'sentences.txt' #alter name of the text file
example_sentences = ["profit rose", "profits decreased", "we were awarded lots of awards", "items were bought by customers", "we throught the service was okay", "the best!"] #Example reviews I put through
sentiments = ['negative', 'neutral', 'positive'] #Sentiments
num = 10 ##See top of so many key words on screen for each sentiment
