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
    
    def getClose(self,nowTime,ticker):
        lastYear = str(int(nowTime[:4])-1)
        lastTime = lastYear+nowTime[4:]

        self.__df_krx=fdr.DataReader(ticker,lastTime,nowTime)
        
        return self.__df_krx