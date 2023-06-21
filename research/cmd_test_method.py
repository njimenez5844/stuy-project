import pandas as pd 
from nltk.corpus import wordnet as wn
from nltk.corpus import genesis
genesis_ic = wn.ic(genesis, False, 0.0)

import numpy as np
import pandas as pd
import warnings 
from sklearn.neighbors import KNeighborsClassifier as KNC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# rids the console of warnings
import warnings
warnings.filterwarnings("ignore")

# reads in the data
data = pd.read_csv('data/train.csv')
data.drop('Id',axis=1 , inplace=True)

CommentsToBeTokenized = data['Comment'] 
tokens = CommentsToBeTokenized[0].split()

# tokenizes the comments
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer()
bow = cv.fit_transform(CommentsToBeTokenized)

# creates a tf-idf matrix
from sklearn.feature_extraction.text import TfidfVectorizer
tfidf = TfidfVectorizer()
tfidf_result=tfidf.fit_transform(CommentsToBeTokenized).toarray()

vectorizer = TfidfVectorizer(max_features=6000)
tfidf_result = vectorizer.fit_transform(CommentsToBeTokenized).toarray()
features = vectorizer.get_feature_names_out()
tfidf_result = pd.DataFrame(tfidf_result, columns=features)

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.naive_bayes import MultinomialNB
    
# creates a new Multinomial model 
NB= MultinomialNB()

xtrain, xtest, ytrain, ytest = train_test_split(tfidf_result, data['Topic'], test_size= 0.2)
NB.fit(xtrain, ytrain)

ypred1 = NB.predict(xtrain)
ypred = NB.predict(xtest)

ytrain=ytrain[0:1739]
ytest=ytest[0:1739]
ypred1 = ypred1[0:1739]
ypred = ypred[0:1739]


 
def cmd_test(model, vectorizer, question, right_label, error_analysis=False):
    # convert the question to a vector, using an already existing vector.
    # There is a subtle issue here - if question includes a word that
    # isn't already in the dataset, the transformer/vectorizor won't handle
    # this.
    #
    # This can be solved, but with careful consideration. Read about online 
    # feature extraction for text for some solutions. 
    #
    # Online tf-idf example https://github.com/idoshlomo/online_vectorizers
    question_as_sparse_matrix = vectorizer.transform([question])
    # convert to vector, this is inefficient but OK
    question_as_vector = np.array(question_as_sparse_matrix.todense())

    # predicts the label
    if model == "KNN":
        prediction = KNC.predict(question_as_vector)
    else: 
        prediction = model.predict(question_as_vector)
    results = {'Comment': question, 'Topic': right_label, 'Guess' : prediction[0]}
    print(results) 
    # check if the prediction is correct
    if prediction[0] == right_label:
        return "Correct"
    else:
        if error_analysis:
            global data
            data.loc[len(data)] = {'Comment': question, 'Topic': right_label}
            data.to_csv(data)
        return "Incorrect"

# This is a function that can be used to test flask input
def online_test(question):
    question_as_sparse_matrix = vectorizer.transform([question])
    question_as_vector = np.array(question_as_sparse_matrix.todense())
    prediction = NB.predict(question_as_vector)
    return prediction[0]


    

import sys # allows for command line arguments to be used as arguments for script.

# the 0th argument (shoud be in ""s) is the question
question = sys.argv[1] 
# the 1th argument ("Physics", "Chemistry", or "Biology") is the correct label to be checked with 
right_Label = sys.argv[2] 
# the 2th argument ("True" or "False") is whether or not to add the question to the dataset if it is incorrect
error_analysis = sys.argv[3]
print(cmd_test(NB, vectorizer, question, right_Label, error_analysis == "True"))