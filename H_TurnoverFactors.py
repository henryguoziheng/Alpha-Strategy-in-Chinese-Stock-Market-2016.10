#coding:utf-8

import QuantMethod.DataAPI as di
import pandas as pd
import math
import numpy as np

__author__ = 'Henry Guo'


def CalMnt(date):
    return str(date)[0:7]

#生成时间序列
#start='2010-01-01',end='2013-01-01',freq='M'
date_list=pd.date_range(start='2012-12-01',end='2016-10-01',freq='M')
date_list=pd.DataFrame(date_list.tolist())
date_list[0]=date_list[0].apply(CalMnt)

TurnoverFactor=pd.DataFrame()
for time in date_list[0]:
    print time
    stock_data=di.GetMnthTrd(TradeTime=time)#取每个月交易数据
    stock_data['LnTurnover']=stock_data['Mnvaltrd']/stock_data['Msmvosd']
    stock_data['LnTurnover']=stock_data['LnTurnover'].apply(math.log)#日对数换手率
    stock_data['LnMsmvosd']=stock_data['Msmvosd'].apply(math.log)#日对数流通市值
    stock_data['c']=1

    time=str(pd.Timestamp(time+'-5')+pd.to_timedelta(1,'M'))[0:7]
    (x1,res,rank,s)=np.linalg.lstsq(stock_data[['LnMsmvosd','c']],stock_data['LnTurnover'])#对数换手率对对数流通市值回归
    stock_data['TO_MVFactor']=stock_data['LnTurnover']-np.dot(stock_data[['LnMsmvosd','c']],x1)
    stock_data['Trdmnt']=time
    stock_data=stock_data[['Trdmnt','Stkcd','TO_MVFactor']]
    TurnoverFactor=pd.concat([TurnoverFactor,stock_data])

j=3
i=1
for i in range(len(TurnoverFactor)/65535+1):
    print i
    if (65535+i*65535)>len(TurnoverFactor):
        TurnoverFactor[0+i*65535:(len(TurnoverFactor)-1)].to_excel(u'E:\\量化研究\\学术因子库\\TurnoverFactor\\%s.xls'%j,index=None)
    else:
        TurnoverFactor[0+i*65535:65535+i*65535].to_excel(u'E:\\量化研究\\学术因子库\\TurnoverFactor\\%s.xls'%j,index=None)
    j+=1
