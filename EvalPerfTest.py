# -*- coding: utf-8 -*-

import pandas as pd
import QuantMethod.EvalPerf as EP

__author__ = 'Henry Guo'

data=pd.read_excel(u'C:\\Users\\50599\\Desktop\\sample.xlsx')
data['date']=pd.to_datetime(data['date'])

EP.AnnualReturn(data,freq='Day',prt=True)
EP.MaxDrawdown(data,prt=True)
EP.AverageChange(data,prt=True)
EP.ProbUp(data)
EP.Volatility(data,prt=True)
EP.Beta(data,prt=True)
EP.Alpha(data,prt=True)
EP.SharpeRatio(data,prt=True)
EP.InfoRatio(data,prt=True)
EP.CumulativeReturn(data,file_loc='',prt=False)