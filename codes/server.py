from firebase import Firebase
from krx_info import KRX_Info as KRX
import pandas as pd

class Server(Firebase, KRX):
    def __init__(self):
        self.db = Firebase() # DB연결
        stock = KRX() # StockInfo 연결
        
        if self.db.checkDB('SAVE_CODE_DICT') is False:
            self.db.setAddress('CODE_DICT')

            codeDict = stock.getCodeDict()
            self.db.setDB(codeDict)

    def show_TickerInfo(self):
        self.db.setAddress('CODE_DICT')
        codeDict = self.db.getDB()

        return codeDict
        

