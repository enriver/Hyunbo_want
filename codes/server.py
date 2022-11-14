from firebase import Firebase
from krx_info import KRX_Info as KRX
import pandas as pd
import json

class Server(Firebase, KRX):
    def __init__(self):
        self.db = Firebase() # DB연결
        stock = KRX() # StockInfo 연결
        
        if self.db.checkDB('SAVE_CODE_DICT') is False:
            self.db.setAddress('CODE_DICT')

            codeDict = stock.getCodeDict()
            self.db.setDB(codeDict)

            self.db.setAddress('DEFAULT_SETTING/SAVE_CODE_DICT')
            self.db.setDB(True)

    # {Ticker:종목명} dictionary return
    def getTickerInfo(self):
        self.db.setAddress('CODE_DICT')
        codeDict = self.db.getDB()
        codeDict = codeDict.replace("'","\"")
        codeDict = json.loads(codeDict)

        return codeDict

    # 관심종목 불러오기 {Ticker : 종목명} dictionary return
    def getInterestInfo(self):
        self.db.setAddress('INTEREST_STOCK')
        interestDict = self.db.getDB()

        if interestDict is None:
            return None

        return interestDict

    # 관심종목 추가하기 {Ticker : 종목명}
    def setInterestInfo(self,tickerJSON):
        self.db.setAddress('INTEREST_STOCK')
        self.db.updateDB(tickerJSON)

    # 관심종목 삭제하기 {Ticker}
    def deleteInterestInfo(self,ticker):
        if self.db.getAddress()!= 'INTEREST_STOCK':
            self.db.setAddress('INTEREST_STOCK')

        self.db.deleteDB(ticker)
    