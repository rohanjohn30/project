# -*- coding: utf-8 -*-
"""
This program runs a multivariate regression for Keynesian Investment function.
The independent variables are business sentiment, GDP, funds Rate and R&D.
The dependent varibale is Investment rate.
The data is automatically downloaded from the Federal Reserve.
"""

from pandas import read_csv
import pandas.io.data as web
import matplotlib.pyplot as plt
import datetime as dt
import os
import subprocess
from statsmodels.formula.api import ols
from statsmodels.iolib.summary2 import summary_col
import statsmodels.api as sm

start = dt.datetime(1970, 1, 1)     #sets the start year of analysis. 1970 seems to be the starting year for most data sets.
end = dt.datetime(2017, 1, 1)      #sets the end year of analysis. 

 con = web.DataReader(["A191RL1Q225SBEA","BSCICP02USQ460S",
                          "A006RL1A225NBEA","IRSTFR01USA156N","Y006RL1A225NBEA"], 
                            "fred", start, end)
    con.ix['2013-01-01']
    con.to_csv('raw.csv')
    con = read_csv('raw.csv')
    con.columns = ['Date', 'GDP','bsent', 'investment','rate','research']
    #con['lagGDP'] = con['GDP'].shift(-1)
    con.to_csv('test.csv')
    os.remove('raw.csv')
    f= read_csv("test.csv")
    keep_col = ['Date', 'GDP','bsent','investment','rate','research']
    new_f = f[keep_col]
    new_f.dropna(how='any', inplace=True)
    new_f.to_csv('data.csv', index=False) # creates csv file with the given headers
    new_f.head()
    os.remove('test.csv')
    return new_f