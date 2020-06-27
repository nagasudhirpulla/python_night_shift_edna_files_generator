# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 18:10:22 2020

@author: Nagasudhir Pulla

Python script for fetching the monthly stats of lines
"""
import pandas as pd
import datetime as dt
from ednaFetcher import fetchEdnaHistData
import argparse
import os
import numpy as np

parser = argparse.ArgumentParser()

parser.add_argument('--config', help='filepath of config file')
args = parser.parse_args()

configFilename = args.config

if configFilename == None:
    configFilename = 'config.xlsx'

# todo donot allow absence of config param
# get points
pntsDf = pd.read_excel(configFilename, sheet_name='pnts')

# get config
configObj = pd.read_excel(configFilename, header=None, sheet_name='config')
configObj.set_index(0, inplace=True)
configObj = configObj[1].to_dict()

yestDate = dt.datetime.now() - dt.timedelta(days=1)
startDate = dt.datetime(yestDate.year, yestDate.month, yestDate.day)
endDate = startDate + dt.timedelta(minutes=59+23*60)

pntsDataObj = {}

print('number of points = {0}'.format(pntsDf.shape[0]))

for itr in range(pntsDf.shape[0]):
    pnt = pntsDf.iloc[itr, 0]
    genName = pntsDf.iloc[itr, 1]
    print('{0} - {1}'.format(itr+1, pnt))
    pntData = fetchEdnaHistData(pnt, startDate, endDate, 'snap', 60)
    if itr == 0:
        pntsDataObj['time'] = [t['t'] for t in pntData]
    pntsDataObj[genName] = [t['v'] for t in pntData]

pntsDataDf = pd.DataFrame(pntsDataObj)

# todo handle illegal format
file_suffix = dt.datetime.strftime(startDate, configObj['formatString'])

fileType = configObj['fileType'].lower()

folderPath = configObj['folderPath']

if pd.isnull(configObj['folderPath']):
    folderPath = ''

# todo handle illegal fileType
fileName = '{0}_{1}.{2}'.format(
    configObj['prefix'], file_suffix, configObj['fileType'])
fileName = os.path.join(folderPath, fileName)

skipRows = 0
if not pd.isnull(configObj['skipRows']):
    skipRows = configObj['skipRows']

if fileType == 'csv':
    writeMode = 'w'
    if skipRows != 0:
        writeMode = 'a'
        pd.DataFrame({'a': [np.nan] * skipRows}
                     ).to_csv(fileName, index=False, header=None)
    pntsDataDf.to_csv(fileName, index=False, mode=writeMode)
else:
    pntsDataDf.to_excel(fileName, index=False, startrow=skipRows)
