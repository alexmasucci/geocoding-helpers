'''This program provides functions used in census_geocoder.py'''

import urllib.request, urllib.parse, urllib.error
import ssl
import json
import numpy as np
import pandas as pd

def ignore_ssl():
    '''Returns context to ignore SSL certificate errors'''
    
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


def open_connection(df, i, baseurl, parameters):
    '''Opens connection to Census Geocoder for address corresponding
    to the given index (i) in the given dataframe (df)'''
    
    parameters['street'] = df['addressline1'][i]
    parameters['city'] = df['city'][i]
    parameters['state'] = df['state'][i]
    parameters['zipcode'] = df['zipcode'][i]
    url = baseurl + urllib.parse.urlencode(parameters)
    try:
        connection = urllib.request.urlopen(url, context = ignore_ssl())
        return connection
    except:
        return None


def retrieve_geodata(connection):
    '''Uses Census Geocoder connection to return a dictionary with 
    matched address, latitude, longitude, census tract code, and county code
    (returns empty dictionary if there is no match data)'''
    
    try:
        datastring = connection.read().decode()
        js = json.loads(datastring)
        geodata = {}
        if len(js['result']['addressMatches']) == 0:
            return geodata
        geodata['matchedaddress'] = js['result']['addressMatches'][0]['matchedAddress']
        geodata['longitude'] = js['result']['addressMatches'][0]['coordinates']['x']
        geodata['latitude'] = js['result']['addressMatches'][0]['coordinates']['y']
        geodata['countycode'] = js['result']['addressMatches'][0]['geographies']['Counties'][0]['GEOID']
        geodata['censustractcode'] = js['result']['addressMatches'][0]['geographies']['Census Tracts'][0]['GEOID']
        return geodata
    except:
        return None