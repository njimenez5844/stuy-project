import pandas as pd 
import nltk
import numpy as np

data = pd.read_csv('train.csv')
data.drop('Id',axis=1 , inplace=True)

CommentsToBeTokenized = data['Comment'] 
tokens = CommentsToBeTokenized[0].split()

from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer()
bow = cv.fit_transform(CommentsToBeTokenized)

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

 
def online_test(vectorizer, question, right_label):
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
    
    # creates a new model 
    NB= MultinomialNB()

    xtrain, xtest, ytrain, ytest = train_test_split(tfidf_result, data['Topic'], test_size= 0.2)
    NB.fit(xtrain, ytrain)

    ypred1 = NB.predict(xtrain)
    ypred = NB.predict(xtest)

    ytrain=ytrain[0:1739]
    ytest=ytest[0:1739]
    ypred1 = ypred1[0:1739]
    ypred = ypred[0:1739]

    # predict the label
    prediction = NB.predict(question_as_vector)
    results = {'Comment': question, 'Topic': right_label, 'Guess' : prediction[0]}
    print(results) 
    # check if the prediction is correct
    if prediction[0] == right_label:
        return "Correct"
    else:
        return "Incorrect"
    
import sys # allows for command line arguments to be used as arguments for script.

# the 0th argument (shoud be in ""s) is the question
question = sys.argv[1] 
# the 1th argument ("Physics", "Chemistry", or "Biology") is the correct label to be checked with 
right_Label = sys.argv[2] 

print(online_test(vectorizer, question, right_Label))