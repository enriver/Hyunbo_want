from server import Server
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import pandas as pd

# UI파일 연결
form_class = uic.loadUiType("Hyunbo_UI.ui")[0]

class WindowClass(QMainWindow, form_class):
    tickerDict = dict()
    server = None
    intrstRowNum = 0
    intrstSet=set()

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 서버 연결
        self.server = Server()
              
        # 관심종목 불러오기
        interestDict = self.server.getInterestInfo()

        if interestDict is None :
            self.intrstRowNum = -1
            #self.tbl_intrst_intrst.setRowCount(10)
        else:
            self.intrstSet = set(interestDict.keys())

            self.intrstRowNum = len(interestDict)-1
            self.tbl_intrst_intrst.setRowCount(self.intrstRowNum)
            #self.tbl_intrst_intrst.setRowCount(10)
        
            i=0
            for ticker,StockName in interestDict.items():
                self.tbl_intrst_intrst.setItem(i,0,QTableWidgetItem(str(ticker)))
                self.tbl_intrst_intrst.setItem(i,1,QTableWidgetItem(str(StockName)))
                i+=1

        # 관심종목 TAB-모든종목 설정
        self.tickerDict = self.server.getTickerInfo() # dict
        
        self.tbl_intrst_all.setRowCount(len(self.tickerDict))
        i=0
        for ticker,StockName in self.tickerDict.items():
            #print(code, StockName)
            self.tbl_intrst_all.setItem(i,0,QTableWidgetItem(str(ticker)))
            self.tbl_intrst_all.setItem(i,1,QTableWidgetItem(str(StockName)))
            i+=1
        self.tbl_intrst_all.resizeColumnsToContents()

        # 관심종목 TAB-관심종목 QTableWidget 칼럼 사이즈 맞추기
        tbl_intrst_intrst_header = self.tbl_intrst_intrst.horizontalHeader()
        tbl_intrst_intrst_header.resizeSection(0,80)
        tbl_intrst_intrst_header.resizeSection(1,280)

        # 관심종목 TAB-관심종목 추가
        self.tbl_intrst_all.doubleClicked.connect(self.addIntrst)

        # 관심종목 TAB-관심종목 삭제
        self.tbl_intrst_intrst.doubleClicked.connect(self.deleteIntrst)

    # 관심종목 TABLE 및 DB에 종목 추가
    def addIntrst(self):
        row =  self.tbl_intrst_all.currentIndex().row()
        ticker = self.tbl_intrst_all.item(row,0).text()
        stockName = self.tbl_intrst_all.item(row,1).text()

        if ticker not in self.intrstSet:
            self.intrstRowNum+=1

           # self.tbl_intrst_intrst.setRowCount(self.intrstRowNum)
            self.tbl_intrst_intrst.insertRow(self.intrstRowNum)
            self.tbl_intrst_intrst.setItem(self.intrstRowNum,0,QTableWidgetItem(ticker))
            self.tbl_intrst_intrst.setItem(self.intrstRowNum,1,QTableWidgetItem(stockName))

            self.server.setInterestInfo({ticker:stockName})
            self.intrstSet.add(ticker)
            #self.tbl_intrst_intrst.resizeColumnsToContents()
        else:
            print('이미 관심종목에 추가한 종목입니다.')

    # 관심종목 TABLE 및 DB에서 종목 삭제
    def deleteIntrst(self):
        row = self.tbl_intrst_intrst.currentRow()
        ticker = self.tbl_intrst_intrst.item(row,0).text()
        self.tbl_intrst_intrst.removeRow(row)
        self.intrstRowNum-=1

        self.server.deleteInterestInfo(ticker)
        self.intrstSet.remove(ticker)

        


if __name__=="__main__":
    # 프로그램 실행
    app = QApplication(sys.argv)
    #인스턴스 생성
    myWindow = WindowClass()
    # 화면 생성
    myWindow.show()
    app.exec_()

    
    
