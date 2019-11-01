'''This program asks the user for a range of addressids to search on
the Google Maps API. For searched addresses, it saves the data
string, match status, and number of results in a pickle. At the 
end of the program, the pickle is exported to CSV. If the program
is terminated early, the pickle should be exported to CSV manually using 
the program pickle_to_csv.py'''


import urllib.request, urllib.parse, urllib.error
import ssl
import json
import numpy as np
import pandas as pd
import time
import pickle
import os
from gm_geocoding_functions import *


# set directory and Google Maps API key
key = 'INSERT GOOGLE MAPS API KEY HERE'


# ask user for addressid range to search in the current session
print()
firstid = int(input('Enter first addressid to search: '))
lastid = int(input('Enter last addressid to search: '))


# set base parameters
baseurl = 'https://maps.googleapis.com/maps/api/geocode/'
outputformat = 'json'


# load in doc address data and set search index
print('\nReading in addresses...', end = ' ')
df = pd.read_pickle('addresses.pkl')
print('Done')

searchindex = df[(df['addressid'] >= firstid) & (df['addressid'] <= lastid)].index
numaddresses = len(searchindex)
if numaddresses == 0:
    print('No addresses in search range')
    quit()


# retrieve geo data, put results into dataframe, and pickle 
# the dataframe after each search
print('\nRetrieving data...')
delay = 0
searchcount = 0
searchstart = time.time()
reportratefreq = 25
reportratestart = time.time()
for i in searchindex:
    searchcount += 1
    print('Address', searchcount, 'of', str(numaddresses) + ':', end = ' ')
    
    time.sleep(delay)
    attempts = 0
    underlimit = False
    while underlimit != True and attempts < 3:
        connection = open_connection(df, i, baseurl, outputformat, key)
        if connection == None:
            matchstatus = 'Connection Error'
            underlimit = True
        else:
            searchresults = get_json(connection)
            if searchresults == None:
                matchstatus = 'Parsing Error'
                underlimit = True
            else:
                matchstatus = searchresults['matchstatus']
                if matchstatus == 'OVER_QUERY_LIMIT':
                    delay += 0.1
                    time.sleep(2)
                    attempts += 1
                    continue
                else:
                    for var in ['jsonstring','numberofresults']:
                        df.loc[i,var] = searchresults[var]
                    underlimit = True
            
    print(matchstatus)
    df.loc[i,'matchstatus'] = matchstatus
    
    df.to_pickle('addresses.pkl')
    
    if searchcount % reportratefreq == 0:
        reportratestop = time.time()
        print('(Current address retrieval/save rate:', round((reportratestop - reportratestart)/reportratefreq, 2), 'seconds per address)')
        reportratestart = reportratestop
    
    if attempts == 3:
        print('Daily search limit has been reached')
        break


# report search statistics
searchstop = time.time()
print('Took', round(searchstop - searchstart, 2), 'seconds to retrieve data on', searchcount, 'addresses')
print('(' + str(round((searchstop - searchstart) / searchcount, 2)), 'seconds per address)')

tabmatchstatus = df['matchstatus'][searchindex].value_counts()
print('\n-----Match Success Report-----')
for status in tabmatchstatus.index:
    print(status + ':', tabmatchstatus[status], 'addresses', '(' + str(round(tabmatchstatus[status]/searchcount*100,2)) + '%)')


# export data to csv file
print('\nSaving data...')
savestart = time.time()
df.to_csv('geocoded-addresses.csv', index = False)
savestop = time.time()
print('Took', round(savestop - savestart, 2), 'seconds to save data with', df.shape[0], 'observations')