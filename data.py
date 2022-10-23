'''
ATTRIBUTION: Proper attribution requires clear indication of the data source as "www.macrotrends.net".
A "dofollow" backlink to the originating page is also required if the data is displayed on a web page.
'''

import matplotlib.pyplot as plt
import pandas as pd
import csv
  
x = []
y = []
  
with open('MORTGAGE30US.csv', 'r') as csvfile:
    plots = csv.reader(csvfile, delimiter = ',')
          
    for row in plots:
        x.append(row[0])
        y.append(float(row[1]))
  
date_time = pd.to_datetime(x)
  
DF = pd.DataFrame()
DF['value'] = y
DF = DF.set_index(date_time)
plt.plot(DF)

with open('vix-volatility-index-historical-chart.csv', 'r') as csvfile:
    plots = csv.reader(csvfile, delimiter = ',')
          
    for row in plots:
        x.append(row[0])
        y.append(float(row[1]))
  
date_time = pd.to_datetime(x)
  
DF = pd.DataFrame()
DF['value'] = y
DF = DF.set_index(date_time)
plt.plot(DF)

plt.gcf().autofmt_xdate()
plt.show()