import numpy as np
from sklearn.datasets import fetch_20newsgroups
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

t_train=fetch_20newsgroups(subset='train', shuffle=True)
for i in range(len(t_train.target_names)):
	print('\nCategory[{0}]: '.format(i),t_train.target_names[i])
	
category=['alt.atheism','comp.graphics','soc.religion.christian','sci.med']

t_train=fetch_20newsgroups(subset='train',categories=category,shuffle=True)
t_test=fetch_20newsgroups(subset='test',categories=category,shuffle=True)

print('\nTarget_names:',t_train.target_names)
print('\nLen of train: ',len(t_train))
print('\nLen of test: ',len(t_test))

from sklearn.feature_extraction.text import CountVectorizer
cnt_vect=CountVectorizer()
X_train_tf = cnt_vect.fit_transform(t_train.data)
print('\nX_train_tf: ',X_train_tf.shape)

from sklearn.feature_extraction.text import TfidfTransformer
tfidf_transform=TfidfTransformer()
X_train_tfidf=tfidf_transform.fit_transform(X_train_tf)
print('\nX_train_tfid: ',X_train_tfidf.shape)

X_test_tf = cnt_vect.transform(t_test.data)
print('\nX_test_tf: ',X_test_tf.shape)
X_test_tfidf=tfidf_transform.transform(X_test_tf)
print('\nX_test_tfid: ',X_test_tfidf.shape)

from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn import metrics

mod=MultinomialNB()
mod.fit(X_train_tfidf,t_train.target)
prediction=mod.predict(X_test_tfidf)
print('\nAccuracy: ',accuracy_score(t_test.target,prediction))
print('\nClassification: ',classification_report(t_test.target,prediction,target_names=t_test.target_names))
print('\nConfusion: ',metrics.confusion_matrix(t_test.target,prediction))



