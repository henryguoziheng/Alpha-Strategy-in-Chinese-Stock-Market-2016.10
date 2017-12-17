#coding:utf-8

import QuantMethod.DataAPI as di
import pandas as pd
import math

__author__ = 'Henry Guo'

a=0.88
n=2.25
g=0.61
t=0.69

def caldate(date):
    """
    将YYYY-MM-DD转为YYYY-MM。
    :param date: YYYY-MM-DD
    :return:YYYY-MM
    """
    date=str(date)[0:7]
    return date


def w_p(p):
    return pow(p,g)/pow((pow(p,g)+pow((1-p),g)),1/g)

def w_n(p):
    return pow(p,t)/pow((pow(p,t)+pow((1-p),t)),1/t)

def v(r):
    if r>=0:
        r=pow(r,a)
    else:
        r=-n*pow(r,-a)
    return r

def er(r):
    return -math.exp(-g*r)

#选取全部股票数据
#BeginTime='2010-06-01',EndTime='2012-01-01'-->2010-06~2011-01

#完全覆盖区域：2010-06~2011-01,
begin_time=pd.Timestamp('2010-06-01')
end_time=pd.Timestamp('2012-01-01')

data=di.GetDalyTrd(BeginTime=str(begin_time-pd.to_timedelta(400,'D'))[0:10],EndTime=str(end_time)[0:10])
data['LnAR']=(data['Dretwd']+1).apply(math.log)
data['er']=data['Dretwd'].apply(er)
print 'done'

FactorData=pd.DataFrame()
col=['Momentum%s'%str(c) for c in [21,63,126,252]]
col=col+['ClaEU%s'%c for c in [21,63,126,252]]
col=col+['RiskNU%s'%c for c in [21,63,126,252]]
col=['Stkcd','Trdmnt']+col

for code in data['Stkcd'].unique():
    print code
    mid=data[data['Stkcd']==code]#单只股票
    for c in [21,63,126,252]:#前一个月,前一季度,前半年,前一年
        mid['Momentum%s'%str(c)]=mid['LnAR'].rolling(window=c).sum()#动量因子
        mid['ClaEU%s'%str(c)]=mid['er'].rolling(c).mean()#古典效用因子
        mid['RiskNU%s'%str(c)]=mid['Dretwd'].rolling(c).mean()#风险中性因子

    mid['Trddt']=mid['Trddt'].apply(caldate)
    mid['Trdmnt']=mid['Trddt'].shift(-1)#滞后一期
    mid=mid[mid['Trddt']!=mid['Trdmnt']]

    FactorData=pd.concat([FactorData,mid[col]])
    FactorData.dropna(inplace=True)

for i in [21,63,126,252]:
    FactorData['Momentum%s'%str(i)]=FactorData['Momentum%s'%str(i)].apply(math.exp)-1

j=7
i=1
for i in range(len(FactorData)/65535+1):
    print i
    if (65535+i*65535)>len(FactorData):
        FactorData[0+i*65535:(len(FactorData)-1)].to_excel(u'E:\\量化研究\\学术因子库\\MomentumFactor\\%s.xls'%j,index=None)
    else:
        FactorData[0+i*65535:65535+i*65535].to_excel(u'E:\\量化研究\\学术因子库\\MomentumFactor\\%s.xls'%j,index=None)
    j+=1