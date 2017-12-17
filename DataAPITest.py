#coding:utf-8

import QuantMethod.DataAPI as di

__author__ = 'Henry Guo'


#print di.GetCalendar()
#print di.GetCalendar('2015-01-01','2015-02-01')

stock_list=['000001','600030','600887']
#print di.GetCoFunInfo(StockList=stock_list)
#print di.GetCoFunInfo()

#print di.GetDalyTrd(TradeTime='2007-01-22')
#print di.GetDalyTrd(TradeTime='2007-01-22',StockList=stock_list)
#print di.GetDalyTrd(BeginTime='2015-01-01',EndTime='2015-02-01')
#print di.GetDalyTrd(Stkcd='000001',BeginTime='2009-01-01',EndTime='2016-09-30')

#print di.GetMnthTrd(TradeTime='2007-01')
#print di.GetMnthTrd(TradeTime='2007-01',StockList=stock_list)
#print di.GetMnthTrd(BeginTime='2015-01',EndTime='2015-02')
#print di.GetMnthTrd(BeginTime='2015-01',EndTime='2015-02',StockList=stock_list)

IndexcdList=['000300']
#print di.GetIndxTrd(TradeTime='2007-01-22')
#print di.GetIndxTrd(TradeTime='2007-01-22',IndexcdList=IndexcdList)
#print di.GetIndxTrd(BeginTime='2015-01-01',EndTime='2015-02-01')
#print di.GetIndxTrd(BeginTime='2015-01-01',EndTime='2015-02-01',IndexcdList=IndexcdList)

#print di.GetIndxTrm(TradeTime='2010-01')
#print di.GetIndxTrm(TradeTime='2010-01',IndexcdList=IndexcdList)
#print di.GetIndxTrm(BeginTime='2015-01',EndTime='2015-02')
#print di.GetIndxTrm(BeginTime='2015-01',EndTime='2015-02',IndexcdList=IndexcdList)

#print di.GetRfTrd(TradeTime='2007-01-22')
#print di.GetRfTrd(BeginTime='2015-01-01',EndTime='2015-02-01')

#print di.GetFF3F(TradeTime='2010-01-04')
#print di.GetFF3F(BeginTime='2010-01-04',EndTime='2011-01-01')

#print di.GetTrdFactor(TradeTime='2010-02')
#print di.GetTrdFactor(BeginTime='2010-01',EndTime='2011-01')

#print di.GetStList(TradeTime='2010-02')
#print di.GetStList(BeginTime='2010-01',EndTime='2011-01')

#print di.GetIndxCon(TradeTime='2010-02')
#print di.GetIndxCon(BeginTime='2010-01',EndTime='2011-01')

#print di.GetMarketValueFactor(TradeTime='2010-02')
#print di.GetMarketValueFactor(BeginTime='2010-01',EndTime='2011-01')

#print di.GetRetStatFactor(TradeTime='2010-02')
#print di.GetRetStatFactor(BeginTime='2010-01',EndTime='2011-01')

#print di.Get3Factors(TradeTime='2016-02')
#print di.Get3Factors(BeginTime='2015-01',EndTime='2016-01')

#print di.GetTurnoverFactor(TradeTime='2016-02')
#print di.GetTurnoverFactor(BeginTime='2015-01',EndTime='2016-01')

#print di.GetUtilityFactor(TradeTime='2016-02')
#print di.GetUtilityFactor(BeginTime='2015-01',EndTime='2016-01')