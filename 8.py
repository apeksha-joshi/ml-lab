import numpy as np
from sklearn import datasets
import sklearn.metrics as sm
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import pandas as pd

l1=[0,1,2]
def rename(s):
	l2=[]
	for i in s:
		if i not in l2:
			l2.append(i)
	for i in range(len(s)):
		pos=l2.index(s[i])
		s[i]=l1[pos]
	return s

iris=datasets.load_iris()
print('\ndata:\n ',iris.data)
print('\ntarget names:\n ',iris.target_names)
print('\nfeature names:\n ',iris.feature_names)
print('\ntarget:\n ',iris.target)

X=pd.DataFrame(iris.data)
X.columns=['Sepal_Length','Sepal_Width','Petal_Length','Petal_Width']
y=pd.DataFrame(iris.target)
y.columns=['Targets']

km=KMeans(n_clusters=3)
km.fit(X)

plt.figure(figsize=(14,7))
colormap=np.array(['red','lime','black'])
plt.subplot(1,2,1)
plt.scatter(X.Petal_Length,X.Petal_Width,c=colormap[y.Targets],s=40)
plt.title('Real classification')

plt.subplot(1,2,2)
kn=rename(km.labels_)
plt.scatter(X.Petal_Length,X.Petal_Width,c=colormap[kn],s=40)
plt.title('KMeans classification')
plt.show()

print("\nKMeans thought: ",kn)
print('\nAccuracy: ',sm.accuracy_score(y,kn))
print('\nConfusion Matrix: ',sm.confusion_matrix(y,kn))

from sklearn import preprocessing
scaler=preprocessing.StandardScaler()
scaler.fit(X)
xsa=scaler.transform(X)
xs=pd.DataFrame(xsa,columns=X.columns)

from sklearn.mixture import GaussianMixture
from sklearn.metrics import accuracy_score
from sklearn import metrics
gmm=GaussianMixture(n_components=3)
gmm.fit(xs)
y_cluster_gmm=gmm.predict(xs)

plt.figure(figsize=(14,7))
colormap=np.array(['red','lime','black'])
plt.subplot(1,2,1)
em=rename(y_cluster_gmm)
plt.scatter(X.Petal_Length,X.Petal_Width,c=colormap[em],s=40)
plt.title('GMM classification')
plt.show()

print("\nGMM thought: ",em)
print('\nAccuracy: ',sm.accuracy_score(y,em))
print('\nConfusion Matrix: ',sm.confusion_matrix(y,em))
