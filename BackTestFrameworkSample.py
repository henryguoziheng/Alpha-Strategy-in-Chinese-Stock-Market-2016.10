# coding: utf-8

import MySQLdb as mdb
import pandas as pd
import math
import numpy as np

__author__ = 'Henry Guo'


"""
该文件为股票回测框架，回测频率为月度
"""

def ClearExtremeValue(data,col,d=5,u=95):
    #去极值，5%-95%
    for c in col:
        dl=np.percentile(data[c],d)
        ul=np.percentile(data[c],u)
        data=data[(data[c]>dl)&(data[c]<ul)]
    return data

def Normalise(data,col):
    #z-score标准化
    for c in col:
        data[c]=(data[c]-data[c].mean())/data[c].std()
    return data

def FormRecord(record):
    record=pd.DataFrame(record,columns=['Date','Portfolio','Cash'])
    return record

def ReadTradingData(time):
    con=mdb.connect('localhost', 'root','19941123', 'csma')
    cur=con.cursor()
    cur.execute("SELECT Stkcd,Trdmnt,Mopnprc,Mclsprc,Mnvaltrd,Mretwd,Msmvosd from trd_mnth WHERE Trdmnt='%s'"%time)
    data = cur.fetchall()
    data=pd.DataFrame(list(data),columns=['Stkcd','Trdmnt','Mopnprc','Mclsprc','Mnvaltrd','Mretwd','Msmvosd'])
    con.close()
    return data

def ReadFinancialData(table_name,begin_time,end_time,columns):
    for attr in columns:
        if columns.index(attr)==0:
            c=attr
        else:
            c=c+','+attr
    con=mdb.connect('localhost', 'root','19941123', 'csma')
    cur=con.cursor()
    cur.execute("SELECT %s from %s WHERE (Accper>='%s')&(Accper<='%s')"%(c,table_name,begin_time,end_time))
    data = list(cur.fetchall())
    data=pd.DataFrame(data,columns=columns)
    return data

begin_date='2013-08-01'
end_date='2014-12-31'
friction=0.003
capital=100000000
weight_way='Score'#'Score','MarketValue'
portfolio_num=50
local=u'C:\\Users\\BruceZhang\\Desktop\\'

time_rng=pd.Series(pd.date_range(begin_date,end_date,freq='M'))
j=0

for i in time_rng:
    """
    逐月回测，以简单的E/P,B/M股票打分法为例
    """
    print str(i)[0:10]
    #读取该时间股票交易数据
    time=str(i)[0:7]
    ret_df=ReadTradingData(time)
    #去除停牌股票
    ret_df=ret_df[ret_df['Mnvaltrd']!=0]

    #假设是多因子打分，生成股票得分:股票代码，财报时间，市盈率TTM，市净率，市销率TTM
    financial_data=ReadFinancialData('fi_t10',str(i-pd.to_timedelta(75,unit='D')),str(i)[0:10],['Stkcd','Accper','F100103C','F100401A','F100203C'])
    #去除市盈率和市净率为负的股票，并且全取倒数
    financial_data=financial_data[financial_data['F100401A']>=0]
    financial_data['F100401A']=1/financial_data['F100401A']
    financial_data=financial_data[financial_data['F100103C']>=0]
    financial_data['F100103C']=1/financial_data['F100103C']
    financial_data=financial_data[financial_data['F100203C']>=0]
    financial_data['F100203C']=1/financial_data['F100203C']
    ret_df['Msmvosd']=1/ret_df['Msmvosd']
    #合并数据：股票代码，市盈率TTM倒数，市净率倒数，市销率倒数，复权收益率，流通市值,月开盘价，月收盘价,时间
    panel_data=pd.merge(financial_data[['Stkcd','F100103C','F100401A','F100203C']],ret_df[['Stkcd','Trdmnt','Mopnprc','Mclsprc','Mretwd','Msmvosd']])
    #中心化
    panel_data=Normalise(panel_data,['F100103C','F100401A','F100203C','Msmvosd'])
    #去极值
    panel_data=ClearExtremeValue(panel_data,['F100103C','F100401A','F100203C','Msmvosd'])
    #计算得分
    weight=[0.25,0.25,0.25,0.25]
    panel_data['score']=(panel_data[['F100103C','F100401A','F100203C','Msmvosd']]*weight).sum(axis=1)

    panel_data.sort_values(by='score',inplace=True,ascending=False)
    #取前n只股票构建组合
    panel_data=panel_data[0:portfolio_num]

    #组合权重（给出权重or生成权重）
    if weight_way=='Score':
        panel_data['weight']=panel_data['score']/panel_data['score'].sum()
    elif weight_way=='MarketValue':
        panel_data['weight']=panel_data['Msmvosd']/panel_data['Msmvosd'].sum()
    else:
        panel_data['weight']=1.0/portfolio_num

    #每只股票上可以投入资金
    panel_data['weight']=panel_data['weight']*capital
    #每只股买了多少股票（满100股为1手），friction是交易成本
    panel_data['Volume']=panel_data['weight']/(panel_data['Mopnprc']*(1+friction)*100)
    panel_data['Volume']=panel_data['Volume'].apply(math.floor)*100
    panel_data['Amount']=panel_data['Volume']*panel_data['Mopnprc']*(1+friction)
    panel_data['Pct%']=panel_data['Mretwd']*(1-friction)
    #当期现金剩余
    cash=capital-panel_data['Amount'].sum()
    #当期结束组合净值
    net_portfolio=(panel_data['Volume']*panel_data['Mclsprc']).sum()

    #设置初始组合情形
    if i==time_rng[0]:
        position_record=panel_data[['Trdmnt','Stkcd','Volume','Amount','Pct%']]
        capital_record=pd.DataFrame({'Date':str(i)[0:7],'Cash':cash,'Amount':net_portfolio},index=[j])

    else:
        position_record=pd.concat([position_record,panel_data[['Trdmnt','Stkcd','Volume','Amount','Pct%']]])
        capital_record=pd.concat([capital_record,pd.DataFrame({'Date':str(i)[0:7],'Cash':cash,'Amount':net_portfolio},index=[j])])
    j+=1
    capital=cash+net_portfolio

position_record.columns=['Date','Code','Volume','Amount','Pct%']
position_record.to_csv(local+u'头寸记录.csv',index=False)
#净值记录生成
capital_record=capital_record[['Date','Cash','Amount']]
capital_record.columns=['Date','Cash','Porfolio']
capital_record['Capital']=capital_record['Porfolio']+capital_record['Cash']
capital_record['Index']=capital_record['Capital']/100000000
capital_record['Return']=capital_record['Index'].shift(0)/capital_record['Index'].shift(1)-1
capital_record.to_csv(local+u'交易记录.csv',index=False)