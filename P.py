#coding:utf-8

import pandas as pd
import QuantMethod.DataAPI as di
import numpy as np

__author__ = 'Henry Guo'


def Code(code):
    code='0'*(6-len(str(code)))+str(code)
    return code

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

List=di.GetIndxCon(TradeTime='2016-11',Indxcd='000905')
st=di.GetStList(TradeTime='2016-11')
a['Stkcd']=a['Stkcd'].apply(Code)
a=pd.merge(a,List)
a=pd.merge(a,st[['Stkcd','STflg']],how='outer',on='Stkcd')
a.fillna(1,inplace=True)
a=a[a['STflg']==1]

#残差标准差中证500选100,150,200,250只
a=ClcExtrVal(a,'RFF')#去极值
a=ClcExtrVal(a,'StdEFF')#去极值
a=NormVal(a,'RFF')
a=NormVal(a,'StdEFF')
a['x']=0.5*(a['RFF']+a['StdEFF'])
a.sort_values('x',inplace=False,ascending=True)

p=pd.DataFrame(columns=['Stkcd','weight'])
for i in [100,150,200,250]:
    p['Stkcd']=a['Stkcd']
    p['weight']=1./i
    p[0:i].to_excel(u'E:\\量化研究\\学术因子库\\IH%s.xls'%str(i),index=None)