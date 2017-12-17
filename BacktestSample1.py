#coding:utf-8

import QuantMethod.DataAPI as di
import pandas as pd
from QuantMethod.FormPFList import ClcExtrVal,NormVal

__author__ = 'Henry Guo'


def ClearFactor(data,col):
    for c in col:
        data=ClcExtrVal(data,c)
        data=NormVal(data,c)
    data=data[['Trdmnt','Stkcd']+col]
    return data

begin_date='2014-06-01'#起始回测日期
end_date='2015-10-31'#结束回测日期
time_rng=pd.Series(pd.date_range(begin_date,end_date,freq='M'))
Stock_list=pd.DataFrame()

for month in time_rng:
    print month
    month=str(month)[0:7]

    MarketFactor=di.GetMarketValueFactor(TradeTime=month)#市值因子
    MarketFactor=ClearFactor(MarketFactor,['FLnMsmvttl'])

    ThreeFactor=di.Get3Factors(TradeTime=month)#PB和PE因子
    ThreeFactor.dropna(inplace=True)
    ThreeFactor=ClearFactor(ThreeFactor,['PB','PE'])

    TrdFactor=di.GetTrdFactor(TradeTime=month)#交易因子
    TrdFactor=ClearFactor(TrdFactor,['RFF','StdEFF'])

    RetStatFactor=di.GetRetStatFactor(TradeTime=month)#偏度因子
    RetStatFactor=ClearFactor(RetStatFactor,['FSkew252'])

    factor=MarketFactor
    factor=pd.merge(factor,TrdFactor)
    factor=pd.merge(factor,ThreeFactor)
    factor=pd.merge(factor,RetStatFactor)

    #剔除st股票
    st_list=di.GetStList(TradeTime=month)#读取st列表
    factor=pd.merge(factor,st_list,how='outer')
    factor.fillna(1,inplace=True)
    factor=factor[factor['STflg']==1]
    #选择股票池
    stock_pool=di.GetIndxCon(Indxcd='000905',TradeTime=month)
    factor=pd.merge(factor,stock_pool)

    factor=factor[['Trdmnt','Stkcd','FLnMsmvttl','PB','PE','RFF','StdEFF','FSkew252']]
    factor['Score']=factor[['FLnMsmvttl','PB','PE','RFF','StdEFF','FSkew252']].mean(axis=1)

    Stock_list=pd.concat([Stock_list,factor[['Trdmnt','Stkcd','Score']]])

#输出到excel，因为行数限制而更换
j=1
i=1
for i in range(len(Stock_list)/65535+1):
    print i
    if (65535+i*65535)>len(Stock_list):
        Stock_list[0+i*65535:(len(Stock_list)-1)].to_excel(u'E:\\量化研究\\学术因子库\\%s.xls'%j,index=None)
    else:
        Stock_list[0+i*65535:65535+i*65535].to_excel(u'E:\\量化研究\\学术因子库\\%s.xls'%j,index=None)
    j+=1