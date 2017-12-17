#coding:utf-8

import pandas as pd
import matplotlib.pyplot as plt
import math
import QuantMethod.EvalPerf as ep

__author__ = 'Henry Guo'


GroupReturn=pd.read_excel(u'E:\\量化研究\\学术因子库\\FactorBacktest\\AllMarket_RFF.xls')
col_list=[u'日期',u'基准回报']+[u'第%s组回报'%str(i) for i in range(1,11)]
GroupReturn=GroupReturn[col_list]

#计算胜率
ProbRecord=pd.DataFrame()
for i in range(10):
    win_prob=len(GroupReturn[GroupReturn[u'第%s组回报'%(str(i+1))]>GroupReturn[u'基准回报']])/float(len(GroupReturn))
    anual_std=GroupReturn[u'第%s组回报'%(str(i+1))].std()
    record={u'组别':str(i+1),u'月波动率':anual_std,u'胜率':win_prob}
    ProbRecord=pd.concat([ProbRecord,pd.DataFrame(record,index=[i])])

for col in col_list[1:]:
    GroupReturn[col]=GroupReturn[col]+1
strat_record=pd.DataFrame([['start']+[1]*11],columns=col_list)
GroupReturn=pd.concat([strat_record,GroupReturn])
for col in col_list[1:]:
    GroupReturn[col]=GroupReturn[col].cumprod()

#收益率曲线构造
ReturnRecord=pd.DataFrame()
for i in range(10):
    anual_return=pow(GroupReturn[u'第%s组回报'%(str(i+1))][len(GroupReturn)-1:len(GroupReturn)].tolist()[0],12./len(GroupReturn))-1
    record={u'组别':str(i+1),u'年化收益率':anual_return,u'基准回报':pow(GroupReturn[u'基准回报'][len(GroupReturn)-1:len(GroupReturn)].tolist()[0],12./len(GroupReturn))-1}
    ReturnRecord=pd.concat([ReturnRecord,pd.DataFrame(record,index=[i])])
ReturnRecord=ReturnRecord[[u'组别',u'年化收益率',u'基准回报']]
ReturnRecord=pd.merge(ProbRecord,ReturnRecord)

#ReturnRecord[[u'组别',u'年化收益率',u'月波动率',u'胜率',u'基准回报']].to_excel(u'E:\\量化研究\\学术因子库\\FactorBacktest\\AllMarket_StdEFF_Record.xls',index=None)
#ReturnRecord[[u'年化收益率',u'基准回报']].plot(kind='bar')
#plt.show()

data=GroupReturn[[u'日期',u'第10组回报',u'基准回报']]
apply(ep.AnnualReturn,[data,'Mon',True])
ep.MaxDrawdown(data,prt=True)
ep.AverageChange(data,prt=True)
ep.ProbUp(data)
ep.ProbWin(data)
ep.Volatility(data,prt=True,freq='Mon')
ep.Beta(data,prt=True)
ep.Alpha(data,prt=True,freq='Mon')
ep.SharpeRatio(data,prt=True,freq='Mon')
ep.InfoRatio(data,prt=True,freq='Mon')
ep.CumulativeReturn(data,file_loc='',prt=False)