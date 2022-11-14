from datetime import datetime
import pandas as pd
import sys

from server import Server
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import QSize

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
        self.setWindowTitle("현보현보")
        self.setFixedSize(QSize(1200,700))

        # 서버 연결
        self.server = Server()

        # 새로고침 불러오기
        refreshTime = self.server.getRefreshTime()

        if refreshTime is None :
            pass
        else:
            self.txt_stock_refreshTime.setText(refreshTime)

        # 새로고침 시간 저장하기
        self.btn_stock_refresh.clicked.connect(self.btnRefresh)

        # 관심종목 TAB-관심종목 불러오기 (/INTEREST_STOCK/)
        interestDict = self.server.getInterestInfo()

        if interestDict is None :
            self.intrstRowNum = -1
            #self.tbl_intrst_intrst.setRowCount(10)
        else:
            self.intrstSet = set(interestDict.keys())

            self.intrstRowNum = len(interestDict)
            print(self.intrstRowNum, '불러온 DICT의 길이')
            self.tbl_intrst_intrst.setRowCount(self.intrstRowNum)
            #self.tbl_intrst_intrst.setRowCount(10)
        
            i=0
            for ticker,StockName in interestDict.items():
                self.tbl_intrst_intrst.setItem(i,0,QTableWidgetItem(str(ticker)))
                self.tbl_intrst_intrst.setItem(i,1,QTableWidgetItem(str(StockName)))
                i+=1

        # 관심종목 TAB-모든종목 설정 (/CODE_DICT/)
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

    # 새로고침 버튼 클릭
    def btnRefresh(self):
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.server.saveRefreshTime(now)
        self.txt_stock_refreshTime.setText(now)

    # 관심종목 TABLE 및 DB에 종목 추가
    def addIntrst(self):
        row =  self.tbl_intrst_all.currentIndex().row()
        ticker = self.tbl_intrst_all.item(row,0).text()
        stockName = self.tbl_intrst_all.item(row,1).text()

        if ticker not in self.intrstSet:

            self.tbl_intrst_intrst.setRowCount(self.intrstRowNum+1)
            #self.tbl_intrst_intrst.insertRow(self.intrstRowNum)
            self.tbl_intrst_intrst.setItem(self.intrstRowNum,0,QTableWidgetItem(ticker))
            self.tbl_intrst_intrst.setItem(self.intrstRowNum,1,QTableWidgetItem(stockName))
            self.intrstRowNum+=1

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

    # 프로그램 종료시 이벤트
    def closeEvent(self, event):
        pass
        


if __name__=="__main__":
    # 프로그램 실행
    app = QApplication(sys.argv)
    #인스턴스 생성
    myWindow = WindowClass()
    # 화면 생성
    myWindow.show()
    app.exec_()

    
    
