#coding:utf-8

import pandas as pd
import QuantMethod.DataAPI as di
import math

__author__ = 'Henry Guo'

"""
提取2013年1月-2016年9月的月股票市值因子
"""
def reformdate(date):
    """
    转化日期，将YYYY-MM-DD转为YYYY-MM。
    :param date: 年月日。
    :return:年月。
    """
    date=str(date)[0:7]
    return date

def stkcd(code):
    """
    转换股票代码，将csv对于股票代码的数字储存方式改为字符储存，保留6位。
    :param code:
    :return:
    """
    code=(6-len(str(code)))*'0'+str(code)
    return code

#因为市值是月末市值，所以滞后一期
data=di.GetMnthTrd(BeginTime='2012-12',EndTime='2016-09')#所得月市值是当月月末市值
data.to_csv(u'E:\\量化研究\\学术因子库\\MarketValueFactors.csv')

#取上市时间，上市需满6个月
ipo_date=di.GetCoFunInfo()
ipo_date['Listdt']=pd.to_datetime(ipo_date['Listdt'])+pd.to_timedelta(6,unit='M')

ipo_date['Listdt']=ipo_date['Listdt'].apply(reformdate)
ipo_date=ipo_date[['Stkcd','Listdt']]
ipo_date['Stkcd']=ipo_date['Stkcd'].apply(stkcd)

data=pd.read_csv(u'E:\\量化研究\\学术因子库\\MarketValueFactors.csv',index_col=0)
#当时先利用上面下载数据，然后再跑下面运行的
data['Stkcd']=data['Stkcd'].apply(stkcd)
data=pd.merge(data,ipo_date)
data=data[data['Trdmnt']>=data['Listdt']]

after_data=pd.DataFrame()

for stkcd in data['Stkcd'].unique():
    print stkcd
    mid_data=data[data['Stkcd']==stkcd]
    mid_data['FMsmvttl']=mid_data['Msmvttl'].shift(1)#总市值，都滞后一月
    mid_data['FMsmvosd']=mid_data['Msmvosd'].shift(1)#流通市值
    mid_data['FLnMsmvosd']=mid_data['FMsmvosd'].apply(math.log)#对数流通市值
    mid_data['FLnMsmvttl']=mid_data['FMsmvttl'].apply(math.log)#对数总市值
    mid_data.dropna(inplace=True)
    after_data=pd.concat([after_data,mid_data])

after_data=after_data[['Stkcd','Trdmnt','FMsmvttl','FMsmvosd','FLnMsmvttl','FLnMsmvosd']]
#输出到excel，因为行数限制而更换
j=1
i=1
for i in range(len(after_data)/65535+1):
    print i
    if (65535+i*65535)>len(after_data):
        after_data[0+i*65535:(len(after_data)-1)].to_excel(u'E:\\量化研究\\学术因子库\\%s.xls'%j,index=None)
    else:
        after_data[0+i*65535:65535+i*65535].to_excel(u'E:\\量化研究\\学术因子库\\%s.xls'%j,index=None)
    j+=1