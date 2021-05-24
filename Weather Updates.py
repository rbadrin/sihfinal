# Gathers the weather information of the detected district and sends it as an SMS. 

import requests, json
import time
import json
import geopy
import geocoder
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

api_key = 'Insert_your_API_key'
api_call = 'https://api.openweathermap.org/data/2.5/forecast?appid=' + api_key
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
            g = geocoder.ip('me') #This line gets your address (coordinates)
            lat=g.latlng[0]
            long=g.latlng[1]
            coordinates =str(lat)+','+str(long)
            geolocator = Nominatim(timeout=3)
            loc=geolocator.reverse(coordinates,language='en') #This line gets your city based on the coordinates
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
                #print(c);
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
                print('\n{m}/{d}/{y}'.format(**date))
       
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
            description = item['weather'][0]['description'],

        # Prints the whole information of temp in celsius and weather for tomorrow at 09:00
            print('Weather condition: %s' % description)
            print('Celcius: {:.2f}'.format(temperature - 273.15))
            print('Farenheit: %.2f' % (temperature * 9/5 - 459.67))
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
        
response = requests.request("POST", url, data="sender_id=FSTSMS&message={}&language=english&route=p&numbers=YOUR NUMBER".format(c), headers=headers)    
