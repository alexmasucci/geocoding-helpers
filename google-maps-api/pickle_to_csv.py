'''This program exports the pickle of geocoded address data to a csv file.
This program should be run whenever google_maps_api_geocoder.py is terminated early'''

import time
import pandas as pd
import os

df = pd.read_pickle('addresses.pkl')
print('\nSaving data...')
savestart = time.time()
df.to_csv('geocoded-addresses.csv', index = False)
savestop = time.time()
print('Took', round(savestop - savestart, 2), 'seconds to save data with', df.shape[0], 'observations')