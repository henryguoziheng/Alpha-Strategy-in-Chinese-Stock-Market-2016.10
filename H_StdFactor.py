#coding:utf-8

import pandas as pd
import QuantMethod.DataAPI as di

__author__ = 'Henry Guo'


def caldate(date):
    """
    将YYYY-MM-DD转为YYYY-MM。
    :param date: YYYY-MM-DD
    :return:YYYY-MM
    """
    date=str(date)[0:7]
    return date

#选取全部股票数据
#BeginTime='2013-09-30',EndTime='2016-09-30'-->2014-11~2016-09
#BeginTime='2010-09-30',EndTime='2013-09-30'-->2011-11~2013-09
#BeginTime='2012-09-30',EndTime='2014-09-30'-->2013-11~2014-09
#BeginTime='2009-06-30',EndTime='2011-12-31'-->2010-08~2012-01
#BeginTime='2007-06-30',EndTime='2010-12-31'-->2008-08~2011-01
#BeginTime='2012-07-31',EndTime='2013-11-30'-->2013-10
#完全覆盖区域：2008-08~2013-09,2013-11~2014-09,2014-11~2016-09,和2014-10
data=di.GetDalyTrd(BeginTime='2013-07-31',EndTime='2014-11-30')
print 'done'

FactorData=pd.DataFrame()
for code in data['Stkcd'].unique():
    print code
    mid=data[data['Stkcd']==code]
    for c in [21,63,126,252]:#前一个月,前一季度,前半年,前一年
        mid['FStd%s'%str(c)]=mid['Dretwd'].rolling(c).std()
        mid['FSkew%s'%str(c)]=mid['Dretwd'].rolling(c).skew()
        mid['FKurt%s'%str(c)]=mid['Dretwd'].rolling(c).kurt()
    mid['Trddt']=mid['Trddt'].apply(caldate)
    mid['Trdmnt']=mid['Trddt'].shift(-1)#滞后一期
    mid=mid[mid['Trddt']!=mid['Trdmnt']]
    c=['FStd%s'%str(c) for c in [21,63,126,252]]
    c=c+['FSkew%s'%c for c in [21,63,126,252]]
    c=c+['FKurt%s'%c for c in [21,63,126,252]]
    FactorData=pd.concat([FactorData,mid[['Stkcd','Trdmnt']+c]])
    FactorData.dropna(inplace=True)

j=7
i=1

for i in range(len(FactorData)/65535+1):
    print i
    if (65535+i*65535)>len(FactorData):
        FactorData[0+i*65535:(len(FactorData)-1)].to_excel(u'E:\\量化研究\\学术因子库\\StdFactor\\%s.xls'%j,index=None)
    else:
        FactorData[0+i*65535:65535+i*65535].to_excel(u'E:\\量化研究\\学术因子库\\StdFactor\\%s.xls'%j,index=None)
    j+=1