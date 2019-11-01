'''This program creates a dataframe from the address data, creates
fields for the new variables we want, then saves the dataframe as a 
pickle.

The address data is assumed to be saved as a CSV file called
addresses.csv with the following variables:
addressid - An integer uniquely identifying each address
addressline1 - Address line 1
addressline2 - Address line 2
city - Address city
state - Address state
zipcode - Address ZIP code'''

import pandas as pd
import numpy as np
import time
import os

if 'addresses.pkl' in os.listdir():
    print('addresses.pkl already exists - delete manually before creating a new pickle')
    quit()

conv = {'addressid': int, 'addressline1': str, 'addressline2': str, 
        'city': str, 'state': str, 'zipcode': str}
loadstart = time.time()
df = pd.read_csv('addresses.csv', header = 0, converters = conv)
loadstop = time.time()
print('Took', round(loadstop - loadstart, 2), 'seconds to read in', df.shape[0], 'addresses')

df['matchedaddress'] = np.nan
df['longitude'] = np.nan
df['latitude'] = np.nan
df['countycode'] = np.nan
df['censustractcode'] = np.nan
df['matchstatus'] = np.nan

df.to_pickle('addresses.pkl')