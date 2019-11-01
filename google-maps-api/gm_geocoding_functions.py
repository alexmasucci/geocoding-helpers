'''This program provides functions used in google_maps_api_geocoder.py'''

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

def open_connection(df, i, baseurl, outputformat, key):
    '''Opens connection to Google Maps API for address corresponding
    to the given index (i) in the given dataframe (df)'''
    
    street = df['addressline1'][i]
    city = df['city'][i]
    state = df['state'][i]
    zipcode = df['zipcode'][i]
    address = street + ',' + city + ',' + state + zipcode
    parameters = {'address': address, 'key': key}    
    url = baseurl + outputformat + '?' + urllib.parse.urlencode(parameters)
    try:
        connection = urllib.request.urlopen(url, context = ignore_ssl())
        return connection
    except:
        return None

def get_json(connection):
    '''Uses Google Maps API connection to return a dictionary with the
    full string containing the json data, the status of the search provided
    by the API, and the number of results found (returns None if unable to
    parse the data as a json object)'''
    
    try:
        searchresults = {}
        datastring = connection.read().decode()
        js = json.loads(datastring)
        searchresults['jsonstring'] = datastring
        searchresults['matchstatus'] = js['status']
        searchresults['numberofresults'] = int(len(js['results']))
        return searchresults
    except:
        return None