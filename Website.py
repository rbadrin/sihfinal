# Entire code

from flask import Flask,render_template,flash,request

import numpy as np

import pandas as pd

import geocoder

import geopy

from geopy.geocoders import Nominatim

from geopy.extra.rate_limiter import RateLimiter

import requests, json

import time

from requests.exceptions import Timeout, ConnectionError

from sklearn.preprocessing import StandardScaler

from urllib3.exceptions import ReadTimeoutError

import json

import tweepy

import sqlite3

import reverse_geocoder as rg

import pprint

from sqlite3 import Error

from datetime import date

import logging

import re

from sklearn.preprocessing import StandardScaler

from sklearn.neighbors import KNeighborsRegressor as KNR

from sklearn import ensemble

from xgboost import XGBClassifier

global api

app=Flask(__name__)

ans_crop=[]

@app.route('/crop')

def crop():

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
    sc = StandardScaler()
    X=sc.fit_transform(X)

    sc1=StandardScaler()
    sc2=StandardScaler()
    sc3=StandardScaler()

    y_N = sc1.fit_transform(y1)
    y_P = sc2.fit_transform(y2)
    y_K = sc3.fit_transform(y3)

    regP=KNR(n_neighbors=8, weights='distance')
    regP.fit(X,y_P)

    params = {'n_estimators': 500, 'max_depth': 4, 'min_samples_split': 2,
              'learning_rate': 0.01, 'loss': 'ls'}
    regN = ensemble.GradientBoostingRegressor(**params)
    regN.fit(X,y_N)


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

    usernx=[[final_result[0]]]

    userpx=[[final_result[1]]]

    userkx=[[final_result[2]]]

    # Let us suggest monsoon crops for the farmer

    csvname="monsoon.csv"

    # Average monsoon rainfall, temparature and humidity for Kanchipuram district are hard-coded.
    
    userrainx=[[130]]

    usertempx=[[20]]

    userhumx=[[80]]

    data=pd.read_csv(csvname)
    data.drop(data.columns[data.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
    max_rows=len(data)
    Nx=data.iloc[:,1:2].values
    Px=data.iloc[:,2:3].values
    Kx=data.iloc[:,3:4].values
    min_tempx=data.iloc[:,4:5].values
    max_tempx=data.iloc[:,5:6].values
    min_humx=data.iloc[:,8:9].values
    max_humx=data.iloc[:,9:10].values
    min_rainx=data.iloc[:,6:7].values
    max_rainx=data.iloc[:,7:8].values

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
    ans=[]
    pos1=error_row.index(best)
    pos2=error_row.index(second_best)
    for i in range(15):
        if(i==pos1 or i == pos2):
            ans.append((data['Crop'][i]))
    return render_template("show_crop.html", data=ans)4


@app.route ('/weather')

def weather():

    api_key = 'Insert_your_API_key_here'
    api_call = 'Insert_your_API_call_here' + api_key

    running = True
    flag=0
    red=0
    c=" "
        # Program loop
    while running and red==0:

            # Asks the user for the city or zip code to be queried
        while True:

                # Input validation

                    # Passed the validation test
                red+=1
                g = geocoder.ip('me') #This line gets your address
                lat=g.latlng[0]
                long=g.latlng[1]
                coordinates =str(lat)+','+str(long)
                geolocator = Nominatim(timeout=3)
                loc=geolocator.reverse(coordinates,language='en')
                loc=loc.raw
                city = str(loc['address']['city'])
                if city.lower() == 'sf':
                    city = 'San Francisco, US'

                        # Appends the city to the api call
                api_call += '&q=' + city
                break



            # Stores the Json response
        json_data = requests.get(api_call).json()

        location_data = {
                'city': json_data['city']['name'],
                'country': json_data['city']['country']
        }

            #print('\n{city}, {country}'.format(**location_data))

            # The current date we are iterating through
        current_date = ''
        flag=0
            # Iterates through the array of dictionaries named list in json_data
        for item in json_data['list'] :
            flag+=1
            if(flag==1):
                # Time of the weather data received, partitioned into 3 hour blocks
                time = item['dt_txt']

                # Split the time into date and hour [2018-04-15 06:00:00]
                next_date, hour = time.split(' ')

                # Stores the current date and prints it once
                if current_date != next_date:
                    current_date = next_date
                    year, month, day = current_date.split('-')
                    date = {'y': year, 'm': month, 'd': day}
                    #print('\n{m}/{d}/{y}'.format(**date))

                # Grabs the first 2 integers from our HH:MM:SS string to get the hours
                hour = int(hour[:2])

                # Sets the AM (ante meridiem) or PM (post meridiem) period
                if hour < 12:
                    if hour == 0:
                        hour = 12
                    meridiem = 'AM'
                else:
                    if hour > 12:
                        hour -= 12
                    meridiem = 'PM'

                # Prints the hours [HH:MM AM/PM]
                    #print('\n%i:00 %s' % (hour, meridiem))

                # Temperature is measured in Kelvin
                temperature = item['main']['temp']

                # Weather condition
                description = item['weather'][0]['description'],

                # Prints the description as well as the temperature in Celcius and Farenheit
                    #print('Weather condition: %s' % description)
                    #print('Celcius: {:.2f}'.format(temperature - 273.15))
                    #print('Farenheit: %.2f' % (temperature * 9/5 - 459.67))
                b=description
                d=[]
                for a in range(0,len(b)):
                    c+="Today's climate"+" : "+b[a]+" and the temperature is {:.1f}°C.".format(temperature - 273.15)
                    d.append(c)
                    
                url = "https://www.fast2sms.com/dev/bulk"
                payload = "sender_id=FSTSMS&message=",b,"&language=english&route=p&numbers=YOUR NUMBER" #Enter the number to which the message must be sent
                headers = {
                'authorization':"YOUR AUTHORIZATION",       #The authorization must be got from fast2sms website
                'Content-Type': "application/x-www-form-urlencoded",
                'Cache-Control': "no-cache",
                }
                

            elif(flag==9):
            # Time separated into 3 hours
                time = item['dt_txt']
       
            # Split into date and hour
                next_date, hour = time.split(' ')
           
            # Stores and prints the date
                if current_date != next_date:
                    current_date = next_date
                    year, month, day = current_date.split('-')
                    date = {'y': year, 'm': month, 'd': day}
           
            # Slicing is done to get HH:MM:SS format
                hour = int(hour[:2])

            # Decides AM or PM
                if hour < 12:
                    if hour == 0:
                        hour = 12
                    meridiem = 'AM'
                else:
                    if hour > 12:
                        hour -= 12
                    meridiem = 'PM'

            # Prints the time
                print('\n%i:00 %s' % (hour, meridiem))

            # Temperature in Kelvin
                temperature = item['main']['temp']

            # Weather condition or description
                description = item['weather'][0]['description']
                
                b=description
               
                for a in range(0,len(b)):
                    c+="\n"+"TOMORROW'S climate"+"\n"+b[a]+"\ntemperature is {:.1f}".format(temperature - 273.15)
                    #c is the string containing the description
                #the api used for sending messages
                url = "https://www.fast2sms.com/dev/bulk"
                payload = "sender_id=FSTSMS&message=",b,"&language=english&route=p&numbers=YOUR NUMBER" #Enter the number to which the message must be sent
                headers = {
                'authorization':"YOUR AUTHORIZATION",   #The authorization must be got from fast2sms website
                'Content-Type': "application/x-www-form-urlencoded",
                'Cache-Control': "no-cache",
                }

            elif flag>11:
                break
    #The message informing the weather description for two days is sent to the number in the position of YOUR NUMBER
            
    response = requests.request("POST", url, data="sender_id=FSTSMS&message={}&language=english&route=p&numbers=+919500048657".format(c), headers=headers)    





@app.route('/login')

def my_form2():

    return render_template('show_login.html')



@app.route('/login', methods=['POST'])

def my_form_post2():

    phoneno = request.form['text']

    password  = request.form['text1']

    ans=[]

    conn = sqlite3.connect("DATABASE CONNECTION")

    cur=conn.cursor()

    cur.execute("select * from sih_info where ph_no=(?) and password=(?)",(str(phoneno),str(password)))

    rows=cur.fetchall()

    if(rows==[]):

        ans.append("NO RECORDS FOUND")

    else:

        ans.append("you have logged in ")

    return render_template("show_login.html",data=ans)

@app.route('/signup')

def my_form1():

    return render_template('show_signup.html')



@app.route('/signup', methods=['POST'])

def my_form_post1():

    name = request.form['text']

    age  = request.form['text1']

    phoneno = request.form['text2']

    password = request.form['text3']

    conn=sqlite3.connect("DATABASE CONNECTION")

    cur=conn.cursor()

    cur.execute("insert into sih_info values(?,?,?,?)",(str(name),str(age),str(phoneno),str(password)))

    conn.commit()

    if conn :

        conn.close()

    ans=[]

    ans.append("The details have been submitted to the database")

    return render_template("show_signup.html",data=ans)



@app.route('/loans')

def my_form():

    return render_template('show_loans.html')



@app.route('/loans', methods=['POST'])

def my_form_post():

    pr = request.form['text']

    p=int(pr)

    ra = request.form['text1']

    r=int(ra)

    print(r)

    ti = request.form['text2']

    t=int(ti)

    org = request.form['text3']

    ans=[]

    ans.append(org)

    ans.append(int(p * (pow((1 + r/ 100), t))/(t*12)))

    ans.append(p)

    ans.append(r)

    ans.append(t*12)

    return render_template('show_loans.html',data =ans)



app.secret_key=('hello')

@app.route('/tweets')

def tweets():

    consumer_key="Insert_consumer_key_here"

    consumer_secret="Insert_consumer_secret"
    
    access_token="Insert_access_token"

    access_token_secret="Insert_access_token_secret"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    id_list=[1246396473983434752] #add the id's of twitter pages you want to get here. I randomly used trump and biden here.

    individual_tweet_list=[]  # the tweets of 1 particular ID or page is stored here and replaced

    # the tweets of 1 particular ID or page is stored here and replaced

    final_tweet_list=[]

    for i in range(len(id_list)):

        new_tweets=[]

        new_tweets = api.user_timeline(id= id_list[i],count=5,tweet_mode='extended') #count tell the number of most recent tweets you want

        for tweet in new_tweets:

            text=tweet.full_text.encode('utf-8')

            text = re.sub(r':', '', text)

            text = re.sub(r'[^\x00-\x7F]+',' ', text)

            final_tweet_list.append(text) # This is the final answer. It is a 2D list. First row contains the tweets of first user

        return render_template("show_tweets.html", data=final_tweet_list)





@app.route('/pesticide')

def Pesticide():

    rows=[]

    for i in ans_crop:

        # print(i)

        conn=sqlite3.connect("DATABASE CONNECTION")

        cur=conn.cursor()

        cur.execute("select pest from pesticide where crop=(?) COLLATE NOCASE",(i,))

        rows.append(cur.fetchall())

        conn.close()

    #print (rows)

    # url = "https://www.fast2sms.com/dev/bulk"

    # payload = "sender_id=FSTSMS&message=",b,"&language=english&route=p&numbers=8939632343"

    # headers = {

    # 'authorization':"Wbc2KH0nkwFvwkAlnGJiuwHUcAU83Qw7YvR9fhpWhQFqiY786XB7xYh6ZkCE",

    # 'Content-Type': "application/x-www-form-urlencoded",

    # 'Cache-Control': "no-cache",

    # }



    # response = requests.request("POST", url, data="sender_id=FSTSMS&message={}&language=english&route=p&numbers=8939632343".format(c), headers=headers)

    return render_template("show_pesticide.html", data=rows)

if __name__ == '__main__':

    app.run(debug=True)
