#coding:utf-8

import pandas as pd
import QuantMethod.DataAPI as di
import numpy as np
#import scipy.stats as stats
#import matplotlib.pyplot as plt

__author__ = 'Henry Guo'


def CalMnt(date):
    """
    将时间处理为字符串
    :param date: 输入时间
    :return:时间字符串
    """
    date=str(date)[0:7]
    return date

def ClcExtrVal(data,col,d=5,u=95):
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

def SetGroup(data,col,asd=True,n=10):
    """
    对于因子进行分组。
    :param data: 数据集。
    :param col: 因子名称（即所在列）
    :param asd: 递增排序or递减排序，默认为递增
    :param n: 分组组数
    :return:分组后的数据
    """
    data.sort_values(by=col,ascending=asd,inplace=True)
    #重新设定index
    data.index=range(len(data))
    data['Group']=0
    for i in range(n):
        if i==(n-1):
            data['Group'][(0+len(data)/n*i):len(data)]=i+1
        else:
            data['Group'][(0+len(data)/n*i):len(data)/n*(i+1)]=i+1
    return data

"""
1.回测时间段
2.回测分组数——默认10组
3.回测因子名称——如何每月提取某个因子，因为函数不同
4.设置对照组
（1）某一指数
（2）等权市场收益率
5.求得：
（1）每组每月收益率+基准收益率-->绘图，统计胜率，回撤等信息
*（2）IC：每月IC、IR、t，全样本IC、IR、t-->全样本每组IC，IR，t，RankIC；总体IC，IR，t，RankIC；每月整体IR绘图；统计IR显著性比例
"""

#设置回测起始时间
BeginTime='2010-06-01'
EndTime='2016-09-30'
n=10#分组组数
Factor_Name='RFF'
Factor_Func=di.GetTrdFactor
Benchmark=['zz500','equal']#上证50,sz50-000016；沪深300,hs300-000300；中证500,zz500；全市场,m，暂不能用；指数-norm or 等权-equal

#生成因子回测的时间序列
date_list=pd.date_range(start=BeginTime,end=EndTime,freq='M')
date_list=pd.DataFrame(date_list.tolist(),columns=['Trdmnt'])
date_list['Trdmnt']=date_list['Trdmnt'].apply(CalMnt)

GroupReturn=pd.DataFrame()#记录每月分组收益和对照组收益
GroupIC=pd.DataFrame()#记录每月分组和整体IC
GroupRankIC=pd.DataFrame()#记录每月分组和整体秩IC
ICRecord=pd.DataFrame()#用于记录全样本数据，最后计算因子全区间的IC和RankIC

j=0

for mnt in date_list['Trdmnt']:
    print mnt
    #读取因子数据
    factor=apply(Factor_Func,[mnt])

    #剔除st股票
    st_list=di.GetStList(TradeTime=mnt)#读取st列表
    factor=pd.merge(factor,st_list,how='outer')
    factor.fillna(1,inplace=True)
    factor=factor[factor['STflg']==1]

    #选择股票池
    if Benchmark[0]=='m':
        stock_pool=factor
    elif Benchmark[0]=='zz500':
        stock_pool=di.GetIndxCon(Indxcd='000905',TradeTime=mnt)
        BenchmarkReturn=di.GetIndxTrm(TradeTime=mnt,IndexcdList=['000905'])
    elif Benchmark[0]=='sz50':
        stock_pool=di.GetIndxCon(Indxcd='000016',TradeTime=mnt)
        BenchmarkReturn=di.GetIndxTrm(TradeTime=mnt,IndexcdList=['000016'])
    elif Benchmark[0]=='hs300':
        stock_pool=di.GetIndxCon(Indxcd='000300',TradeTime=mnt)
        BenchmarkReturn=di.GetIndxTrm(TradeTime=mnt,IndexcdList=['000300'])
    factor=pd.merge(factor,stock_pool)
    factor=factor[['Stkcd','Trdmnt',Factor_Name]]
    BenchmarkReturn=BenchmarkReturn[['Trdmnt','Mretwd']]
    BenchmarkReturn.columns=['Trdmnt','IdxMretwd']

    #因子清洗
    factor=ClcExtrVal(factor,Factor_Name)#去极值
    factor=NormVal(factor,Factor_Name)#标准化
    factor=SetGroup(factor,Factor_Name,n=n)#股票分组

    #提取股票收益率
    stock_return=di.GetMnthTrd(TradeTime=mnt)
    stock_return=pd.merge(stock_return[['Trdmnt','Stkcd','Mretwd']],factor)

    #生成基准收益率
    if Benchmark[1]=='norm':
        stock_return=pd.merge(stock_return,BenchmarkReturn)
    else:
        stock_return['IdxMretwd']=stock_return['Mretwd'].mean()

    return_record={}
    #ic_record={}
    #ir_record={}
    #t_record={}
    #ric_record={}
    for i in range(n):
        mid_return=stock_return[stock_return['Group']==(i+1)]
        return_record.update({u'日期':mnt,u'第%s组回报'%str(i+1):mid_return['Mretwd'].mean()})#记录各组合收益率

        # ic_mnt,ic_pv=stats.pearsonr(mid_return['Mretwd'],mid_return['StdEFF'])#每月每组IC
        # ic_record.update({u'日期':mnt,u'第%s组IC'%str(i+1):ic_mnt/mid_return['Mretwd'].std(),u'第%s组IC_p值'%str(i+1):ic_pv})

        # ric_mnt,ric_pv=stats.spearmanr(mid_return['Mretwd'],mid_return['StdEFF'])#每月每组RankIC
        # ric_record.update({u'日期':mnt,u'第%s组RankIC'%str(i+1):ric_mnt,u'第%s组RankIC_p值'%str(i):ric_pv})

    return_record.update({u'基准回报':stock_return['IdxMretwd']})
    return_record=pd.DataFrame(return_record,index=[j])
    GroupReturn=pd.concat([GroupReturn,return_record])

    # IC_mnt,IC_mnt_pv=stats.pearsonr(stock_return['Mretwd'],stock_return['StdEFF'])#每月整体IC
    # ic_record.update({u'基准IC':IC_mnt,u'基准IC_p值':IC_mnt_pv})
    # ic_record=pd.DataFrame(ic_record,index=[j])
    # GroupIC=pd.concat([GroupIC,ic_record])

    # R_IC_mnt,R_IC_mnt_pv=stats.spearmanr(stock_return['Mretwd'],stock_return['StdEFF'])#每月整体IC
    # ric_record.update({u'基准RankIC':R_IC_mnt,u'基准RankIC_p值':R_IC_mnt_pv})
    # ric_record=pd.DataFrame(ric_record,index=[j])
    # GroupRankIC=pd.concat([GroupRankIC,ic_record])

    j+=1

    # ICRecord=pd.concat([ICRecord,stock_return[['Trdmnt','Stkcd','Mretwd','StdEFF','Group']]])

# GroupReturn.to_excel(u'E:\\量化研究\\学术因子库\\FactorBacktest\\return.xls',index=None)
# GroupIC.to_excel(u'E:\\量化研究\\学术因子库\\FactorBacktest\\ic.xls',index=None)