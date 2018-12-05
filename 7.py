import numpy as np
import pandas as pd
import wrapt
import matplotlib.pyplot as plt
import urllib
from urllib.request import urlopen
import sklearn as skl
import seaborn as sns
import sklearn.metrics as sm
import pgmpy

url='https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.hungarian.data'
np.set_printoptions(threshold=np.nan)
names=['age','sex','cp','trestbps','chol','fbs','restecg','thalach','exang','oldpeak','slope','ca','thal','heartdisease']
heartDisease=pd.read_csv(urlopen(url),names=names)
print(heartDisease.head())
del heartDisease['thal']
del heartDisease['ca']
del heartDisease['slope']
del heartDisease['oldpeak']
heartDisease=heartDisease.replace('?',np.nan)
print(heartDisease.columns)

from pgmpy.models import BayesianModel
from pgmpy.estimators import MaximumLikelihoodEstimator,BayesianEstimator

model=BayesianModel([('age','trestbps'),('age','fbs'),('sex','trestbps'),('exang','trestbps'),('trestbps','heartdisease'),('fbs','heartdisease'),('heartdisease','restecg'),('heartdisease','chol'),('heartdisease','thalach')])
model.fit(heartDisease,estimator=MaximumLikelihoodEstimator)

print(model.get_cpds('age'))
print(model.get_cpds('sex'))
print(model.get_cpds('chol'))
model.get_independencies()

from pgmpy.inference import VariableElimination
heart_infer=VariableElimination(model)
q=heart_infer.query(variables=['heartdisease'],evidence={'age':28})
print(q['heartdisease'])
q=heart_infer.query(variables=['heartdisease'],evidence={'chol':100})
print(q['heartdisease'])
