import pandas as pd
import FinanceDataReader as fdr
from datetime import datetime

class KRX_Info:
    __df_krx=None

    def __init__(self):
        pass

    def getCodeDict(self):
        self.__df_krx = fdr.StockListing('KRX')
        self.__df_krx = self.__df_krx.sort_values(by=['Code']).reset_index(drop=True)

        codeDict = dict()

        for i in range(self.__df_krx.shape[0]):
            codeDict[self.__df_krx['Code'][i]] = self.__df_krx['Name'][i]

        return codeDict
    
    def getClose(self,code):
        today = datetime.today()

        year  = today.year
        month = today.month
        day   = today.day

        s_day = str(year-1)+'-'+str(month)+'-'+str(day) # 시작날짜
        l_day = str(year)  +'-'+str(month)+'-'+str(day) # 종료날짜

        self.__df_krx=fdr.DataReader(code,s_day,l_day)
        
        return self.__df_krx['Close']