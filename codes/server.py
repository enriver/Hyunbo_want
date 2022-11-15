from firebase import Firebase
from krx_info import KRX_Info as KRX
import pandas as pd
import json

class Server(Firebase, KRX):
    def __init__(self):
        self.db = Firebase() # DB연결
        self.stock = KRX() # StockInfo 연결
        
        if self.db.checkDB('SAVE_CODE_DICT') is False:
            self.db.setAddress('CODE_DICT')

            codeDict = self.stock.getCodeDict()
            self.db.setDB(codeDict)

            self.db.setAddress('DEFAULT_SETTING/SAVE_CODE_DICT')
            self.db.setDB(True)

    # 주가 정보 DB에 저장하기
    def saveStock(self,dfStockDict):
        self.db.setAddress('STOCK_CLOSE_INFO')
        self.db.deleteDB()
        self.db.updateDB(dfStockDict)

    # 주가 정보 DB에서 전부 삭제하기
    def clearStock(self):
        self.db.setAddress('STOCK_CLOSE_INFO')
        self.db.deleteDB()

    # DB에서 주가 정보 불러오기
    def getStockCloseFromDB(self):
        if self.db.getAddress() != 'STOCK_CLOSE_INFO':
            self.db.setAddress('STOCK_CLOSE_INFO')

        return self.db.getDB()

    # 주가 정보 받아오기
    def getStockClose(self,nowTime,ticker):
        return self.stock.getClose(nowTime,ticker)

    # 새로고침 시간 저장하기
    def saveRefreshTime(self,nowTime):
        self.db.setAddress('DEFAULT_SETTING/REFRESH_TIME')
        self.db.setDB(nowTime)
        
    # 새로고침 시간 가져오기
    def getRefreshTime(self):
        self.db.setAddress('DEFAULT_SETTING/REFRESH_TIME')
        refreshTime = self.db.getDB()

        if refreshTime is None:
            return None
        return refreshTime.replace('"','')

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
    