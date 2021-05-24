# Predicts the soil contents (N,P,K) based on location (coordinates) using Machine Learning Algorithms.

import numpy as np
import pandas as pd
import geocoder
import reverse_geocoder as rg

# Importing the dataset
dataset = pd.read_csv('soil.csv')
X = dataset.iloc[:, 0:2].values
y1=dataset.iloc[:,5:6].values
y2=dataset.iloc[:,6:7].values
y3=dataset.iloc[:,7:8].values

#Getting the lat and long and initialising the final result

g = geocoder.ip('me')
lat=g.latlng[0]
long=g.latlng[1]
location=[[long,lat]]
final_result=[]
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X=sc.fit_transform(X)

sc1=StandardScaler()
sc2=StandardScaler()
sc3=StandardScaler()

y_N = sc1.fit_transform(y1)
y_P = sc2.fit_transform(y2)
y_K = sc3.fit_transform(y3)

from sklearn.neighbors import KNeighborsRegressor as KNR
regP=KNR(n_neighbors=8, weights='distance')
regP.fit(X,y_P)

from sklearn import ensemble
params = {'n_estimators': 500, 'max_depth': 4, 'min_samples_split': 2,
          'learning_rate': 0.01, 'loss': 'ls'}
regN = ensemble.GradientBoostingRegressor(**params)
regN.fit(X,y_N)

from xgboost import XGBClassifier
regK = XGBClassifier( max_depth=2,gamma=2,eta=0.8,reg_alpha=0.5,reg_lambda=0.5)
regK.fit(X,y_K)

N=(regN.predict(location))
N=list(sc1.inverse_transform(N))
final_result.extend(N)


P=regP.predict(location)
P=list(sc2.inverse_transform(P))
final_result.extend(P)


K=regK.predict(location)
K=list(sc3.inverse_transform(K))
final_result.extend(K)
final_result = [ '%.3f' % elem for elem in final_result ]
final_result = [float(i) for i in final_result] 
# final_result is of the form ['N','P','K']
