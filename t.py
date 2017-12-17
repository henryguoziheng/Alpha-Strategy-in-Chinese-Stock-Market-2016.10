#coding:utf-8

import pandas as pd

__author__ = 'Henry Guo'


def CalCode(code):
    return (6-len(str(code)))*'0'+str(code)

data=pd.read_csv(u'C:\\Users\\BruceZhang\\Desktop\\Revised_momentum_All_month.csv')
data['Stkcd']=data['Stkcd'].apply(CalCode)
j=1
i=1

for i in range(len(data)/65535+1):
    print i
    if (65535+i*65535)>len(data):
        data[0+i*65535:(len(data)-1)].to_excel(u'E:\\量化研究\\学术因子库\\UtilityFactor\\%s.xls'%j,index=None)
    else:
        data[0+i*65535:65535+i*65535].to_excel(u'E:\\量化研究\\学术因子库\\UtilityFactor\\%s.xls'%j,index=None)
    j+=1
