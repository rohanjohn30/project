# project
The motivation for this project was to use econometic techniques to obtain results using python and to
build on the macroeconomic project module submitted which used keynesian investment function. The program
is used to confirm the factors resulting in investment.

This python algorithm downloads data from the Federal Reserve database and saves them in a csv file.
The data downloaded is then sorted and edited into another csv file with headers using pandas dataframe. 
The program runs OLS regression on the Keynesian Investment Function. The main independent variables 
used are :
1. Business Sentiment = bsent
2. Federal Funds rate = rate
3. GDP growth rate = GDP
4. Research and Development = research

Autonomous investment is characterised by govt spending. But according to the IS curve, G is the 
govt spending and so we will not take the intercept into consideration in this analysis. 
(It was also found that intercept was insignificant in the analysis.)
The generated results alongwith the partial regression graphs are saved. The results tex file is then executed
which compiles the results into one pdf file. 

All the data downloaded are in percentage change terms. This is ~log and allows us to remove any dependence 
on the lagged variables. The results are in no way to be taken as conclusive as proper econometric techniques
have not be used with regards to data. This is just a exercise in python programming and hence there might be 
biases as well other drawbacks using OLS.
(To check whether the results are consistent in other softwares such as Stata, the data was regressed
and the answers were found to be identical.)

 
