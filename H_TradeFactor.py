#coding:utf-8

import pandas as pd
import QuantMethod.DataAPI as di
import numpy as np

__author__ = 'Henry Guo'


#生成时间序列
date_list1=pd.date_range(start='2016-10-01',end='2016-10-31',freq='M')
date_list2=date_list1+pd.to_timedelta(1,'D')
date_list1=date_list1.tolist()[1:len(date_list1)]
date_list2=date_list2.tolist()[0:(len(date_list2)-1)]
date_list=zip(date_list2,date_list1)

i=0
TradeFactor=pd.DataFrame()
for begintime,endtime in date_list:
    begintime=str(begintime)[0:10]
    #begintime='2016-10'
    #endtime=pd.Timestamp('2016-10-31')
    print begintime
    stock_data=di.GetDalyTrd(BeginTime=begintime,EndTime=str(endtime)[0:10])
    ff=di.GetFF3F(BeginTime=begintime,EndTime=str(endtime)[0:10])
    stock_data=pd.merge(stock_data,ff)
    stock_data['c']=1
    for code in stock_data['Stkcd'].unique():
        try:
            mid=stock_data[stock_data['Stkcd']==code]
            (x1,res,rank,s)=np.linalg.lstsq(mid[['MKT','c']],mid['Dretwd'])
            mid['e1']=mid['Dretwd']-np.dot(mid[['MKT','c']],x1)
            r1=1-res/((mid['Dretwd']-mid['Dretwd'].mean())*(mid['Dretwd']-mid['Dretwd'].mean())).sum()
            (x2,res,rank,s)=np.linalg.lstsq(mid[['MKT','SMB','HML','c']],mid['Dretwd'])
            mid['e2']=mid['Dretwd']-np.dot(mid[['MKT','SMB','HML','c']],x2)
            r2=1-res/((mid['Dretwd']-mid['Dretwd'].mean())*(mid['Dretwd']-mid['Dretwd'].mean())).sum()
            record=pd.DataFrame({'Trdmnt':str(endtime+pd.to_timedelta(5,'D'))[0:7],'Stkcd':code,'BetaCapm':x1[0],\
                                 'AlphaCapm':x1[1],'RCapm':r1,'StdECapm':mid['e1'].std(),'BetaMKT':x2[0],'BetaSMB':x2[1],\
                                 'BetaHML':x2[2],'RFF':r2,'StdEFF':mid['e2'].std(),'AlphaFF':x2[3]},index=[i])
        except:
            pass
        TradeFactor=pd.concat([TradeFactor,record])
        i+=1

j=1
i=1
for i in range(len(TradeFactor)/65535+1):
    print i
    if (65535+i*65535)>len(TradeFactor):
        TradeFactor[0+i*65535:(len(TradeFactor)-1)].to_excel(u'E:\\量化研究\\学术因子库\\TradeFactor\\%s_%s.xls'%(j,begintime),index=None)
    else:
        TradeFactor[0+i*65535:65535+i*65535].to_excel(u'E:\\量化研究\\学术因子库\\TradeFactor\\%s_%s.xls'%(j,begintime),index=None)
    j+=1