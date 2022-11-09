import pandas as pd
import FinanceDataReader as fdr
from datetime import datetime

class KRX_Info:
    __df_krx=None
    __codeDict = dict()
    def __init__(self):
        self.__df_krx = fdr.StockListing('KRX')

    def getCodeDict(self):

        for i in range(self.__df_krx.shape[0]):
            self.__codeDict[self.__df_krx['Name'][i]] = self.__df_krx['Code'][i]

        return self.__codeDict
    
    def getClose(self,code):
        today = datetime.today()

        year  = today.year
        month = today.month
        day   = today.day

        s_day = str(year-1)+'-'+str(month)+'-'+str(day) # 시작날짜
        l_day = str(year)  +'-'+str(month)+'-'+str(day) # 종료날짜