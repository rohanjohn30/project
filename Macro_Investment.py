# -*- coding: utf-8 -*-
"""
This program runs a multivariate regression for Keynesian Investment function.
The independent variables are business sentiment, GDP, funds Rate and R&D.
The dependent varibale is Investment rate.
The data is automatically downloaded from the Federal Reserve.
"""
import pandas as pd
from pandas import read_csv
import pandas.io.data as web
import matplotlib.pyplot as plt
import datetime as dt
import os
import subprocess
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
import statsmodels.api as sm

# 1970 seems to be the starting year for most data sets
start = dt.datetime(1970, 1, 1)    # sets the start year of analysis.
end = dt.datetime(2017, 1, 1)      # sets the end year of analysis.
global i, j  # sets a counter for the functions compare() and plot()
i = 1
j = 1


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
    new_file.dropna(how='any', inplace=True)  # drops any row with NaN entry
    # creates csv file with the given headers
    new_file.to_csv('data1.csv', index=False)
    new_file.head()
    os.remove('test.csv')
    new_f = read_csv("data1.csv")
    # contains complete entries of the variables
    new_f.to_csv('data.csv', index=False)
    os.remove('data1.csv')
    return new_f


def compare(res, x, y):
    '''Plots a graphs with with actual Y and forcasted Y using global variable j
    to keep track and name intermediary image files. Uses regression results(res),
    independent variable(x) and dependent variable(y)'''
    global i
    ypred = res.predict(x)
    pred = pd.DataFrame(ypred)
    ax = y.plot()
    pred.plot(ax=ax)
    plt.legend(["Actual Y", "Forecast Y'"])
    plt.savefig(str(i) + '.png', dpi=150)
    i += 1
    plt.show()


def plot(res, var):
    '''Plots multiple partial regression graphs wrt to an independent variable (var)
    passed as arguments and the regression results (res).'''
    global j
    fig = plt.figure(figsize=(12, 8))
    fig = sm.graphics.plot_regress_exog(res, var, fig=fig)
    graph = "res" + str(j)
    fig.savefig(graph + '.png')
    j += 1

# We run the first regression here with investment as the dependent
# variable without intercept
dat = data()
model = ols('investment ~ rate + GDP -1', data=dat)
res1 = model.fit()

# plot graph with actual and forecasted values of investment rates for the
# first regression
y = dat['investment']
x = dat[['rate', 'GDP']]
compare(res1, x, y)

# We run the second regression here with Business sentiment as the
# independent variable
mod2 = ols('investment ~ rate + GDP + bsent -1', data=dat)
res2 = mod2.fit()

# We run the Third regression here with R&D as the independent variable
mod3 = ols('investment ~ rate + GDP + bsent + research -1', data=dat)
res3 = mod3.fit()

# plot graph with actual and forecasted values of investment rates for the
# third regression
x = dat[['rate', 'GDP', 'bsent', 'research']]
compare(res3, x, y)

# Peform analysis of variance on fitted linear model with all variables
anova_results = anova_lm(res3)
f = open('anova.tex', 'w')
f.write(anova_results.to_latex())
f.close()

# plotting investment wrt funds rate, business sentiment and R&D
plot(res1, "rate")
plot(res2, "bsent")
plot(res3, "research")
plot(res1, "GDP")

# runs a for loop to write the intermediary summary output to latex
result = [res1, res2, res3]
filename = ['res1', 'res2', 'res3']
for (res, name) in zip(result, filename):
    f = open(name + '.tex', 'w')
    f.write(res.summary().as_latex())
    f.close()

# runs the tex file called Results
subprocess.check_call(['pdflatex', 'Results.tex'])
subprocess.Popen('Results.pdf', shell=True)

# deletes all the intermediary files
results = ['res1', 'res2', 'res3']
for r in results:
    os.remove(r + '.tex')
    os.remove(r + '.png')
os.remove('anova.tex')
pic = ['1', '2']
for r in pic:
    os.remove(r + '.png')
