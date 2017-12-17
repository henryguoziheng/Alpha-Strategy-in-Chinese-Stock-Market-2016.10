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
date_list=pd.date_range(start='2016-11-01',end='2016-11-30',freq='M')
date_list=pd.DataFrame(date_list.tolist())
date_list[0]=date_list[0].apply(CalMnt)

# P4=pd.DataFrame()
P10=pd.DataFrame()
# P6=pd.DataFrame()
# P7=pd.DataFrame()
# P1=pd.DataFrame()
# P2=pd.DataFrame()
# P3=pd.DataFrame()
# MVP=pd.DataFrame()
# RP=pd.DataFrame()
# TOP=pd.DataFrame()
# SKP=pd.DataFrame()

def ClearFactor(data,col):
    data=ClcExtrVal(data,col)
    data=NormVal(data,col)
    return data

for month in date_list[0]:
    print month

    #选取股票池
    #StockPool=di.GetIndxCon(TradeTime=month,Indxcd='000905')
    StockPool=di.GetMarketValueFactor(TradeTime=month)#对数流通市值因子
    StockPool=StockPool[['Trdmnt','Stkcd','FLnMsmvttl']]

    #剔除st股票
    st_list=di.GetStList(TradeTime=month)#读取st列表
    StockPool=pd.merge(StockPool,st_list,how='outer')
    StockPool.fillna(1,inplace=True)
    StockPool=StockPool[StockPool['STflg']==1]
    #StockPool=StockPool[['Trdmnt','Stkcd']]

    # MVFactor=di.GetMarketValueFactor(TradeTime=month)#对数流通市值因子
    # StockPool=pd.merge(StockPool,MVFactor[['Trdmnt','Stkcd','FLnMsmvttl']])

    #市值因子组合测试
    # MVP=pd.concat([MVP,ClearFactor(StockPool[['Trdmnt','Stkcd','FLnMsmvttl']],'FLnMsmvttl')])

    R2Factor=di.GetTrdFactor(TradeTime=month)#特异度因子
    StockPool=pd.merge(StockPool,R2Factor[['Trdmnt','Stkcd','RFF']])
    StockPool['RFF']=1./StockPool['RFF']#倒数

    #特质波动率组合测试
    # RP=pd.concat([RP,ClearFactor(StockPool[['Trdmnt','Stkcd','RFF']],'RFF')])

    TOFactor=di.GetTurnoverFactor(TradeTime=month)#市值调整换手率因子
    StockPool=pd.merge(StockPool,TOFactor[['Trdmnt','Stkcd','TO_MVFactor']])

    #市值调整换手率组合回测
    # TOP=pd.concat([TOP,ClearFactor(StockPool[['Trdmnt','Stkcd','TO_MVFactor']],'TO_MVFactor')])

    TSFactor=di.GetRetStatFactor(TradeTime=month)#博彩型偏好因子
    StockPool=pd.merge(StockPool,TSFactor[['Trdmnt','Stkcd','FSkew252']])
    print len(StockPool)

    #博彩型偏好因子回测
    # SKP=pd.concat([SKP,ClearFactor(StockPool[['Trdmnt','Stkcd','FSkew252']],'FSkew252')])

    PEPBFactor=di.Get3Factors(TradeTime=month)#PB和PE因子
    StockPool=pd.merge(StockPool,PEPBFactor[['Trdmnt','Stkcd','PB','PE']])
    print len(StockPool)

    UFactor=di.GetUtilityFactor(TradeTime=month)#效用因子
    StockPool=pd.merge(StockPool,UFactor[['Trdmnt','Stkcd','UtilityFactor']])
    print len(StockPool)

    #因子清洗
    for col in ['FLnMsmvttl','RFF','TO_MVFactor','FSkew252','PB','PE','UtilityFactor']:
        try:
            StockPool=ClearFactor(StockPool,col)
        except:
            print StockPool
    print len(StockPool)
    #1.PB,PE剔除股票，起到简单财务估值因子的剔除作用
    PB_u=np.percentile(StockPool['PB'],90)#小于最差组
    PE_u=np.percentile(StockPool['PE'],90)#小于最差组
    StockPool=StockPool[(StockPool['PB']<PB_u)&(StockPool['PE']<PE_u)]
    print len(StockPool)
    #2.赋予权重
    #组合1：2*市值+2*特质波动率+1*市值调整换手率+1*252日偏度
    # StockPool['Score']=(2*StockPool['FLnMsmvttl']+2*StockPool['RFF']+1*StockPool['TO_MVFactor']+\
    #                    1*StockPool['FSkew252'])/6
    # StockPool.sort_values(by='Score',ascending=True,inplace=True)
    # P1=pd.concat([P1,StockPool[['Trdmnt','Stkcd','Score']]])

    #组合2：2*市值+(1*特质波动率+1*市值调整换手率)
    # StockPool['Score']=(2*StockPool['FLnMsmvttl']+1*StockPool['RFF']+1*StockPool['TO_MVFactor'])
    # StockPool.sort_values(by='Score',ascending=True,inplace=True)
    # P2=pd.concat([P2,StockPool[['Trdmnt','Stkcd','Score']]])

    #组合3：1*市值+(1*特质波动率+1*市值调整换手率)=1市值+2交易热度
    # StockPool['Score']=(1*StockPool['FLnMsmvttl']+1*StockPool['RFF']+1*StockPool['TO_MVFactor'])
    # StockPool.sort_values(by='Score',ascending=True,inplace=True)
    # P3=pd.concat([P3,StockPool[['Trdmnt','Stkcd','Score']]])

    #组合P4：1*市值+(1*特质波动率+1*市值调整换手率)+0.5*252日偏度=1市值+2交易热度+0.5*252日偏度
    # StockPool['Score']=(1*StockPool['FLnMsmvttl']+1*StockPool['RFF']+1*StockPool['TO_MVFactor'])+0.5*StockPool['FSkew252']
    # StockPool.sort_values(by='Score',ascending=True,inplace=True)
    # P4=pd.concat([P4,StockPool[['Trdmnt','Stkcd','Score']]])

    #组合P5：1*市值+(1*特质波动率+1*市值调整换手率)+1*效用因子=1市值+2交易热度+1*效用因子
    # StockPool['Score']=(1*StockPool['FLnMsmvttl']+1*StockPool['RFF']+1*StockPool['TO_MVFactor'])+1*StockPool['UtilityFactor']
    # StockPool.sort_values(by='Score',ascending=True,inplace=True)
    # P5=pd.concat([P5,StockPool[['Trdmnt','Stkcd','Score']]])

    #组合P6：1*市值+(1*特质波动率+1*市值调整换手率)+2*效用因子=1市值+2交易热度+2*效用因子
    # StockPool['Score']=(1*StockPool['FLnMsmvttl']+1*StockPool['RFF']+1*StockPool['TO_MVFactor'])+2*StockPool['UtilityFactor']
    # StockPool.sort_values(by='Score',ascending=True,inplace=True)
    # P6=pd.concat([P6,StockPool[['Trdmnt','Stkcd','Score']]])

    #组合P7：1*市值+(1*特质波动率+1*市值调整换手率)+0.5*252日偏度=1市值+2交易热度+0.5*效用因子+0.5*252日偏度
    # StockPool['Score']=(1*StockPool['FLnMsmvttl']+1*StockPool['RFF']+1*StockPool['TO_MVFactor'])+0.5*StockPool['UtilityFactor']+0.5*StockPool['FSkew252']
    # StockPool.sort_values(by='Score',ascending=True,inplace=True)
    # P7=pd.concat([P7,StockPool[['Trdmnt','Stkcd','Score']]])

    #组合P8：1*市值+(1*特质波动率+1*市值调整换手率)+1*效用因子=2交易热度+1*效用因子
    StockPool['Score']=1*StockPool['FLnMsmvttl']+(1*StockPool['RFF']+1*StockPool['TO_MVFactor'])+1*StockPool['UtilityFactor']
    StockPool.sort_values(by='Score',ascending=True,inplace=True)
    P10=pd.concat([P10,StockPool[['Trdmnt','Stkcd','Score']]])

# MVP.to_excel(u'E:\\量化研究\\学术因子库\\组合回测\\市值因子组合.xls')
# RP.to_excel(u'E:\\量化研究\\学术因子库\\组合回测\\特质波动率因子组合.xls')
# TOP.to_excel(u'E:\\量化研究\\学术因子库\\组合回测\\换手率因子组合.xls')
# SKP.to_excel(u'E:\\量化研究\\学术因子库\\组合回测\\偏度因子组合.xls')
# P1.to_excel(u'E:\\量化研究\\学术因子库\\组合回测\\历史组合1.xls')
# P2.to_excel(u'E:\\量化研究\\学术因子库\\组合回测\\历史组合2.xls')
# P3.to_excel(u'E:\\量化研究\\学术因子库\\组合回测\\历史组合3.xls')
# P4.to_excel(u'E:\\量化研究\\学术因子库\\组合回测\\历史组合4.xls')

j=1
i=1
for i in range(len(P10)/65535+1):
     print i
     if (65535+i*65535)>len(P10):
         P10[0+i*65535:(len(P10)-1)].to_excel(u'E:\\量化研究\\学术因子库\\组合回测\\历史组合10_%s.xls'%j,index=None)
     else:
         P10[0+i*65535:65535+i*65535].to_excel(u'E:\\量化研究\\学术因子库\\组合回测\\历史组合10_%s.xls'%j,index=None)
     j+=1

#P5.to_excel(u'E:\\量化研究\\学术因子库\\组合回测\\历史组合8.xls')
# P6.to_excel(u'E:\\量化研究\\学术因子库\\组合回测\\历史组合6.xls')
# P7.to_excel(u'E:\\量化研究\\学术因子库\\组合回测\\历史组合7.xls')