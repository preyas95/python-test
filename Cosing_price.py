#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 22:02:20 2018

@author: preyas
"""

from nsepy import get_history
from datetime import date
import pandas as pd
#from pandas.tseries.offsets import *
'''
Choose the stock from TCS or INFY 
to start 
'''
stock=input("Choose stocks:\t TCS or INFY \n")
data = get_history(symbol=stock, start=date(2015,1,1), end=date(2015,12,31))


weeks=input("Weeks 4,8,16,...52\n") #input the week for the moving average
weeks = int(weeks)
ndays=weeks*7 
'''
MA is the module to calculate the moving average for the input stock(TCS or INFY)
and for the input week.. it can be for 52 weeks 
''' 
def MA(ndays,data):
    SMA=pd.Series((data['Close']).rolling(window=ndays).mean(),name = 'SMA')
    data=data.join(SMA)
    data.to_csv('/home/preyas/Downloads/xxx.csv')
    return(data)

data=MA(ndays,data)
#print(data)
'''
caclute the volume shock and including a column name volume shocks in the data
'''
shock=[]
shock.append(0)
for i in range(1,len(data['Volume'])):
    flag=0
    x1=data.iloc[i,9]
    x2=data.iloc[i-1,9]
    if x1>x2:
        diff=1.1*x2
        if x1>diff:
            flag=1
        
    else:
        diff=0.9*x2
        if x1<diff:
            flag=1
    shock.append(flag)
    
data['Volume Shocks']=shock
 
'''
caclute the price shock and including a column name price shocks in the data
'''
shock=[]
for i in range(0,len(data['Close'])):
    flag=0
    x1=data.iloc[i,7]
    x2=data.iloc[i,2]
    if x1>x2:
        diff=1.02*x2
        if x1>diff:
            flag=1
        
    else:
        diff=0.98*x2
        if x1<diff:
            flag=1
    shock.append(flag)
    
data['Price Shocks']=shock 

'''
caclute the Pricing shock without volume shock and including a column name Pricing shock without volume shock in the data
Pricing shock without volume shock
'''
shock=[]
for i in range(0,len(data['Close'])):
    if data.iloc[i,15]==0 and data.iloc[i,16]==1:
        shock.append(1)
    else:
        shock.append(0)
data['Pricing shock without volume shock']=shock

 # Creating a 0/1 dummy-coded time series for direction of shocks.       
data = pd.get_dummies(data, columns=['Volume Shocks','Price Shocks','Pricing shock without volume shock'])
        


       
            
        