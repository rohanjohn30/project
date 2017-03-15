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