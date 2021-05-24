# Suggesting crops based on the soil predicted.

import pandas as pd
import numpy as np

# Providing random values
userph=[[5.3]]
usernx=[[53]]
userpx=[[65]]
userkx=[[89]]


csvname="monsoon.csv"
userrainx=[[130]]
usertempx=[[20]]
userhumx=[[80]]

data=pd.read_csv(csvname)
data.drop(data.columns[data.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
max_rows=len(data)
Nx=data.iloc[:,2:3].values
Px=data.iloc[:,3:4].values
Kx=data.iloc[:,4:5].values
min_tempx=data.iloc[:,5:6].values
max_tempx=data.iloc[:,6:7].values
min_humx=data.iloc[:,9:10].values
max_humx=data.iloc[:,10:11].values
min_rainx=data.iloc[:,7:8].values
max_rainx=data.iloc[:,8:9].values

# Scaling columns
from sklearn.preprocessing import StandardScaler

sc1 = StandardScaler()
sc2=StandardScaler()
sc3=StandardScaler()
sc4=StandardScaler()
sc5=StandardScaler()
sc6=StandardScaler()
sc7=StandardScaler()
sc8=StandardScaler()
sc9=StandardScaler()

Nx1=np.append(Nx,usernx)
Nx1=Nx1.reshape(-1,1)
Nx1=sc1.fit_transform(Nx1)
Nx1=sc1.transform(Nx1)

Px1=np.append(Px,userpx)
Px1=Px1.reshape(-1,1)
Px1=sc2.fit_transform(Px1)
Px1=sc2.transform(Px1)

Kx1=np.append(Kx,userkx)
Kx1=Kx1.reshape(-1,1)
Kx1=sc3.fit_transform(Kx1)
Kx1=sc3.transform(Kx1)

min_tempx1=np.append(min_tempx,usertempx)
min_tempx1=min_tempx1.reshape(-1,1)
min_tempx1 = sc4.fit_transform(min_tempx1)
min_tempx1 = sc4.transform(min_tempx1)

max_tempx1=np.append(max_tempx,usertempx)
max_tempx1=max_tempx1.reshape(-1,1)
max_tempx1 = sc5.fit_transform(max_tempx1)
max_tempx1 = sc5.transform(max_tempx1)

min_humx1=np.append(min_humx,userhumx)
min_humx1=min_humx1.reshape(-1,1)
min_humx1 = sc6.fit_transform(min_humx1)
min_humx1 = sc6.transform(min_humx1)

max_humx1=np.append(max_humx,userhumx)
max_humx1=max_humx1.reshape(-1,1)
max_humx1 = sc7.fit_transform(max_humx1)
max_humx1 = sc7.transform(max_humx1)

min_rainx1=np.append(min_rainx,userrainx)
min_rainx1=min_rainx1.reshape(-1,1)
min_rainx1 = sc8.fit_transform(min_rainx1)
min_rainx1 = sc8.transform(min_rainx1)

max_rainx1=np.append(max_rainx,userrainx)
max_rainx1=max_rainx1.reshape(-1,1)
max_rainx1 = sc9.fit_transform(max_rainx1)
max_rainx1= sc9.transform(max_rainx1)

# Finding rmse of the scaled columns, error_row contains the iterated error through each crop 
error_row=[]
for i in range(max_rows-1):
    error=float(pow((Nx1[i][0]-Nx1[max_rows][0]),2)+pow((Px1[i][0]-Px1[max_rows][0]),2)+pow((Kx1[i][0]-Kx1[max_rows][0]),2))
    error_row.append(error)

for i in range(max_rows-1):    
    if(userrainx[0][0]>=data['min_rain'][i] and userrainx[0][0]<=data['max_rain'][i]):
         error_row[i]+=0.0
       
    elif(userrainx[0][0]>data['max_rain'][i]):
        
        error_row[i]+=float(pow(max_rainx1[i][0]-max_rainx1[max_rows][0],2))
    elif(userrainx[0][0]<data['min_rain'][i]):
        
        error_row[i]+=float(pow(min_rainx1[i][0]-min_rainx1[max_rows][0],2) )

    if(userhumx[0][0]>=data['min_hum'][i] and userhumx[0][0]<=data['max_hum'][i]):
        error_row[i]+=0.0
        
    elif(userhumx[0][0]>data['max_hum'][i]):
        
        error_row[i]+=float(pow(max_humx1[i][0]-max_humx1[max_rows][0],2) )
    elif(userhumx[0][0]<data['min_hum'][i]):
         
         error_row[i]+=float(pow(min_humx1[i][0]-min_humx1[max_rows][0],2) )
    
    if(usertempx[0][0]>=data['min_temp'][i] and usertempx[0][0]<=data['max_temp'][i]):
        error_row[i]+=0.0
        
        
    elif(usertempx[0][0]>data['max_temp'][i]):
        
        error_row[i]+=float(pow(max_tempx1[i][0]-max_tempx1[max_rows][0],2) )
    elif(usertempx[0][0]<data['min_temp'][i]):
         error_row[i]+=float(pow(min_tempx1[i][0]-min_tempx1[max_rows][0],2))   
        
for i in range(max_rows-1):
    error_row[i]=0.5*(pow(error_row[i],0.5))
        

q=[]
q=error_row[:]
q.sort()
best=q[0]
second_best=q[1]
pos1=error_row.index(best)
pos2=error_row.index(second_best)

ans=[]
for i in range(15):
    if(i==pos1 or i == pos2):
        ans.append((data['Crop'][i]))
print(ans)

