import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

iris_data=load_iris()
for i in range(len(iris_data.target_names)):
	print(iris_data.target_names[i])
	
X_train,X_test,y_train,y_test=train_test_split(iris_data['data'],iris_data['target'],random_state=0)

print('\nTarget: ',iris_data.target)
print('\nX_train: ',X_train)
print('\nX_test: ',X_test)
print('\ny_train: ',y_train)
print('\ny_test: ',y_test)

knn=KNeighborsClassifier(n_neighbors=1)
knn.fit(X_train,y_train)

for i in range(len(X_test)):
	x=X_test[i]
	x_new=np.array([x])
	prediction=knn.predict(x_new)
	print('\nActual: {0}{1}  Predicted: {2}{3}'.format(y_test[i],iris_data['target_names'][y_test[i]],prediction,iris_data['target_names'][prediction]))
	
print('\nAccuracy={:.2f}%'.format(knn.score(X_test,y_test)))
