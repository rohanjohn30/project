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

# sets the start year of analysis. 1970 seems to be the starting year for
# most data sets.
start = dt.datetime(1970, 1, 1)
end = dt.datetime(2017, 1, 1)  # sets the end year of analysis.


def data():
    '''Downloads data from Federal Reserve for the variables Investment, GDP,
    Business sentiment, Federal funds rate, and R&D expenditure. All the variables
    are downloaded as percent change from preceding period which removes most
    effects of lagged varibles. Adds labels for each variables in the csv file.
    '''
    con = web.DataReader(["A191RL1Q225SBEA",
                          "BSCICP02USQ460S",
                          "A006RL1A225NBEA",
                          "IRSTFR01USA156N",
                          "Y006RL1A225NBEA"],
                         "fred",
                         start,
                         end)
    con.ix['2013-01-01']
    con.to_csv('raw.csv')
    con = read_csv('raw.csv')
    con.columns = ['Date', 'GDP', 'bsent', 'investment', 'rate', 'research']
    con.to_csv('test.csv')
    os.remove('raw.csv')
    f = read_csv("test.csv")
    keep_col = ['Date', 'GDP', 'bsent', 'investment', 'rate', 'research']
    new_file = f[keep_col]
    new_file.dropna(how='any', inplace=True)  #drops any row with NaN entry
    new_file.to_csv('data1.csv', index=False) # creates csv file with the given headers
    new_file.head()
    os.remove('test.csv')
    new_f= read_csv("data1.csv")
    new_f.to_csv('data.csv', index=False)    #contains complete entries of the variables
    os.remove('data1.csv')                   
    return new_f

def compare(res,x,y):
    '''Plots a graphs with with actual Y and forcasted Y using global variable j
    to keep track and name intermediary image files. Uses regression results(res), 
    independent variable(x) and dependent variable(y)'''
    global i
    ypred = res.predict(x)
    pred= pd.DataFrame(ypred)
    ax=y.plot()
    pred.plot(ax=ax)
    plt.legend(["Actual Y","Forecast Y'"])
    plt.savefig(str(i)+'.png', dpi=150)
    i+=1
    plt.show()

'''We run the first regression here with investment as the dependent variable without intercept'''
dat = data()
model = ols('investment ~ rate + GDP + bsent -1', data=dat)
res1 = model.fit()

'''Plotting investment wrt business sentiment'''
fig = plt.figure(figsize=(12, 8))
fig = sm.graphics.plot_regress_exog(res1, "bsent", fig=fig)
fig.savefig('res1.png')

'''We run the second regression here with R&D as the independent variable'''
mod2 = ols('investment ~ rate + GDP + bsent + research -1', data=dat)
res2 = mod2.fit()

'''Plotting investment wrt R&D'''
fig = plt.figure(figsize=(12, 8))
fig = sm.graphics.plot_regress_exog(res2, "research", fig=fig)
fig.savefig('res2.png')


'''Plotting investment wrt funds rate'''
fig = plt.figure(figsize=(12, 8))
fig = sm.graphics.plot_regress_exog(res2, "rate", fig=fig)
fig.savefig('res3.png')

'''Gives a summary of both regressions'''
res3 = summary_col([res1, res2], stars=True, float_format='%0.2f',
                   info_dict={'R2': lambda x: "{:.2f}".format(x.rsquared)})

'''runs a for loop to write the summary output to latex'''
result = [res1, res2]
filename = ['res1', 'res2']

for (res, name) in zip(result, filename):
    f = open(name + '.tex', 'w')
    f.write(res.summary().as_latex())
    f.close()

f = open('res3.tex', 'w')
f.write(res3.as_latex())
f.close()

'''runs the tex file called Results and deletes all the intermediary files'''
subprocess.check_call(['pdflatex', 'Results.tex'])
subprocess.Popen('Results.pdf', shell=True)
results = ['res1', 'res2', 'res3']
for r in results:
    os.remove(r + '.tex')
    os.remove(r + '.png')
