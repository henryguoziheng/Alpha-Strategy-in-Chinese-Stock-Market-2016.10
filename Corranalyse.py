#coding:utf-8

import pandas as pd
import QuantMethod.DataAPI as di

__author__ = 'Henry Guo'


month='2016-10'
StockPool=di.GetIndxCon(TradeTime=month,Indxcd='000905')
StockPool=StockPool[['Trdmnt','Stkcd']]
MVFactor=di.GetMarketValueFactor(TradeTime=month)#对数流通市值因子
StockPool=pd.merge(StockPool,MVFactor[['Trdmnt','Stkcd','FLnMsmvttl']])
R2Factor=di.GetTrdFactor(TradeTime=month)#特异度因子
StockPool=pd.merge(StockPool,R2Factor[['Trdmnt','Stkcd','RFF']])
TOFactor=di.GetTurnoverFactor(TradeTime=month)#市值调整换手率因子
StockPool=pd.merge(StockPool,TOFactor[['Trdmnt','Stkcd','TO_MVFactor']])
TSFactor=di.GetRetStatFactor(TradeTime=month)#博彩型偏好因子
StockPool=pd.merge(StockPool,TSFactor[['Trdmnt','Stkcd','FSkew252']])
PEPBFactor=di.Get3Factors(TradeTime=month)#PB和PE因子
StockPool=pd.merge(StockPool,PEPBFactor[['Trdmnt','Stkcd','PB','PE']])

StockPool=StockPool[['FLnMsmvttl','RFF','TO_MVFactor','FSkew252','PB','PE']]
result=StockPool.corr()
result.to_excel(u'E:\\量化研究\\学术因子库\\组合回测\\因子相关性.xls')