#coding:utf-8

import QuantMethod.DataAPI as di
import numpy as np
import datetime
import pandas as pd

__author__ = 'Henry Guo'


def ClcExtrVal(data,col,d=2.5,u=97.5):
    """
    去除因子极值，默认为5%-95%。
    :param data: 输入的数据集
    :param col: 因子名称（即所在列）
    :param d: 下限
    :param u: 上限
    :return:因子序列
    """
    dl=np.percentile(data[col],d)
    ul=np.percentile(data[col],u)
    data=data[(data[col]>dl)&(data[col]<ul)]
    return data

def NormVal(data,col):
    """
    z-score标准化。
    :param data:数据集
    :param col: 因子名称（即所在列）
    :return:处理后数据集
    """
    data[col]=(data[col]-data[col].mean())/data[col].std()
    return data

def CalMnt(date):
    return str(date)[0:7]

#生成时间序列
month='2016-11-01'
month_end='2016-11-30'
date_list=pd.date_range(start=month,end=month_end,freq='M')
date_list=pd.DataFrame(date_list.tolist())
date_list[0]=date_list[0].apply(CalMnt)

P=pd.DataFrame()

def ClearFactor(data,col):
    data=ClcExtrVal(data,col)
    data=NormVal(data,col)
    return data

for month in date_list[0]:
    print month

    StockPool=di.GetMarketValueFactor(TradeTime=month)#对数流通市值因子

    #选取股票池
    #Indexcon=di.GetIndxCon(TradeTime=month,Indxcd='000905')
    #StockPool=pd.merge(StockPool,Indexcon)
    StockPool=StockPool[['Trdmnt','Stkcd','FLnMsmvttl']]

    #剔除st股票
    st_list=di.GetStList(TradeTime=month)#读取st列表
    StockPool=pd.merge(StockPool,st_list,how='outer')
    StockPool.fillna(1,inplace=True)
    StockPool=StockPool[StockPool['STflg']==1]

    R2Factor=di.GetTrdFactor(TradeTime=month)#特异度因子
    StockPool=pd.merge(StockPool,R2Factor[['Trdmnt','Stkcd','RFF']])
    StockPool['RFF']=1./StockPool['RFF']#倒数

    TOFactor=di.GetTurnoverFactor(TradeTime=month)#市值调整换手率因子
    StockPool=pd.merge(StockPool,TOFactor[['Trdmnt','Stkcd','TO_MVFactor']])

    PEPBFactor=di.Get3Factors(TradeTime=month)#PB和PE因子
    StockPool=pd.merge(StockPool,PEPBFactor[['Trdmnt','Stkcd','PB','PE']])

    UFactor=di.GetUtilityFactor(TradeTime=month)#效用因子
    StockPool=pd.merge(StockPool,UFactor[['Trdmnt','Stkcd','UtilityFactor']])

    TSFactor=di.GetRetStatFactor(TradeTime=month)#博彩型偏好因子
    StockPool=pd.merge(StockPool,TSFactor[['Trdmnt','Stkcd','FSkew252']])

    #因子清洗
    for col in ['FLnMsmvttl','RFF','TO_MVFactor','PB','PE','UtilityFactor','FSkew252']:
        try:
            StockPool=ClearFactor(StockPool,col)
        except:
            print StockPool

    #1.PB,PE,偏度剔除股票，起到简单财务估值因子的剔除作用
    PB_u=np.percentile(StockPool['PB'],90)#小于最差组
    PE_u=np.percentile(StockPool['PE'],90)#小于最差组
    sk_u=np.percentile(StockPool['FSkew252'],90)#小于最差组
    StockPool=StockPool[(StockPool['PB']<PB_u)&(StockPool['PE']<PE_u)&(StockPool['FSkew252']<sk_u)]

    #组合P：1*市值+(1*特质波动率+1*市值调整换手率)+1*效用因子=2交易热度+1*效用因子
    StockPool['Score']=1*StockPool['FLnMsmvttl']+(1*StockPool['RFF']+1*StockPool['TO_MVFactor'])+1*StockPool['UtilityFactor']
    StockPool.sort_values(by='Score',ascending=True,inplace=True)
    P=pd.concat([P,StockPool[['Trdmnt','Stkcd','Score']]])

j=1
i=1

for i in range(len(P)/65535+1):
     print i
     if (65535+i*65535)>len(P):
         P[0+i*65535:(len(P)-1)].to_excel(u'E:\\量化研究\\学术因子库\\组合回测\\%s_组合_%s.xls'%(month,j),index=None)
     else:
         P[0+i*65535:65535+i*65535].to_excel(u'E:\\量化研究\\学术因子库\\组合回测\\%s_组合_%s.xls'%(month,j),index=None)
     j+=1