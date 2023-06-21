import pandas as pd 

import numpy as np
import pandas as pd
import warnings 
from sklearn.model_selection import train_test_split

# rids the console of warnings
import warnings
warnings.filterwarnings("ignore")

# reads in the data
data = pd.read_csv('data/allData.csv')
data.drop('Id',axis=1 , inplace=True)

CommentsToBeTokenized = data['Comment'] 
tokens = CommentsToBeTokenized[0].split()

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

# This is a function that can be used to test flask input
def online(question):
    question_as_sparse_matrix = vectorizer.transform([question])
    question_as_vector = np.array(question_as_sparse_matrix.todense())
    prediction = NB.predict(question_as_vector)
    return prediction[0]




