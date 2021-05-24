# This program detects your coordinates and returns the city/district the coordinates belonging to.

import geocoder
import reverse_geocoder as rg
import geopy
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

def reverseGeocode(coordinates):
    geolocator = Nominatim(timeout=3)
    loc=geolocator.reverse(coordinates,language='en')
    loc=loc.raw
    #Printing city/district name
    print(loc['address']['city'])
    
# Driver function
if __name__=="__main__":
    g = geocoder.ip('me') #This line gets your address(coordinates)
    lat=g.latlng[0]
    long=g.latlng[1]
    coordinates =str(lat)+','+str(long)
    # reverseGeocode to find the city/district the coordinates belonging to
    reverseGeocode(coordinates)  

