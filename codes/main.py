from datetime import datetime
import pandas as pd
import sys
import webbrowser

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
    df_stock=None

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

        # 관심종목 TAB-관심종목 불러오기 (/INTEREST_STOCK/)
        interestDict = self.server.getInterestInfo()

        if interestDict is None :
            self.intrstRowNum =0
            #self.tbl_intrst_intrst.setRowCount(10)
        else:
            self.intrstSet = set(interestDict.keys())

            self.intrstRowNum = len(interestDict)
            #print(self.intrstRowNum, '불러온 DICT의 길이')
            self.tbl_intrst_intrst.setRowCount(self.intrstRowNum)
            #self.tbl_intrst_intrst.setRowCount(10)
        
            i=0
            for ticker,StockName in interestDict.items():
                self.tbl_intrst_intrst.setItem(i,0,QTableWidgetItem(str(ticker)))
                self.tbl_intrst_intrst.setItem(i,1,QTableWidgetItem(str(StockName)))
                i+=1

        # 주가정보 TAB-초기 종가 등록
        if self.intrstRowNum > 0 :
            stockClose = self.server.getStockCloseFromDB()
            self.df_stock = pd.DataFrame.from_dict(stockClose)

            self.tbl_stock_info.setRowCount(self.df_stock.shape[0])
            self.tbl_stock_info.setColumnCount(self.df_stock.shape[1])
            self.tbl_stock_info.setHorizontalHeaderLabels(self.df_stock.columns.tolist())

            print(self.df_stock)
            # 생성된 종목-종가 데이터프레임 화면에 보여주기
            for i in range(self.df_stock.shape[1]):
                col_name = self.df_stock.columns[i] # 칼럼명
                for j in range(self.df_stock.shape[0]):
                    val = self.df_stock[col_name][j] # 날짜 or 종가 요소
                    item = QTableWidgetItem(str(val))
                    self.tbl_stock_info.setItem(j,i,item)

            self.tbl_stock_info.verticalHeader().hide()

        # 주가정보 TAB-엑셀 다운로드
        self.btn_stock_toExcel.clicked.connect(self.btnDownloadExcel)

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

        # investing.com 크롤링
        self.btn_investing_search.clicked.connect(self.searchInvesting)

        # 새로고침 시간 저장하기
        self.btn_stock_refresh.clicked.connect(self.btnRefresh)

        # 관심종목 TAB-관심종목 추가
        self.tbl_intrst_all.doubleClicked.connect(self.addIntrst)

        # 관심종목 TAB-관심종목 삭제
        self.tbl_intrst_intrst.doubleClicked.connect(self.deleteIntrst)

    # Investing.com 크롤링
    def searchInvesting(self):
        webbrowser.open('investing.com/equities/')

    # EXCEL 다운로드
    def btnDownloadExcel(self):
        if len(self.intrstSet) <= 0:
            print('관심 종목을 먼저 추가해주세요')
        else:
            self.df_stock.to_csv('현보_'+datetime.today().strftime('%Y-%m-%d')+'.csv')

    # 새로고침 버튼 클릭
    def btnRefresh(self):
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.tbl_stock_info.clear() # reset (테이블 값을 재생성 해주기 위함)

        # 종목별 종가 불러오기 => 데이터프레임 생성
        if len(self.intrstSet) == 0 :
            self.tbl_stock_info.setRowCount(0)
        else:
            i=0
            for ticker in self.intrstSet:
                temp_df = self.server.getStockClose(now[:11],ticker)        
                stockName = self.tickerDict[ticker]

                temp_df[stockName] = temp_df['Close']
                temp_df = temp_df[stockName]

                if i==0:
                    self.df_stock = temp_df
                    i+=1
                else:
                    self.df_stock = pd.concat([self.df_stock,temp_df], axis=1)

            if type(self.df_stock) == 'pandas.core.series.Series':
                # 종목이 하나일 경우 Series 이기에 DataFrame 타입으로 변환
                self.df_stock=self.df_stock.to_frame()
            
            self.df_stock = self.df_stock.reset_index(drop=False).sort_values(by='Date', ascending=False).reset_index(drop=True)
            # Date column 형식 바꾸기
            self.df_stock['Date']=self.df_stock['Date'].apply(lambda x:x.strftime('%Y-%m-%d'))

            self.tbl_stock_info.setRowCount(self.df_stock.shape[0])
            self.tbl_stock_info.setColumnCount(self.df_stock.shape[1])
            self.tbl_stock_info.setHorizontalHeaderLabels(self.df_stock.columns.tolist())

            # 생성된 종목-종가 데이터프레임 화면에 보여주기
            for i in range(self.df_stock.shape[1]):
                col_name = self.df_stock.columns[i] # 칼럼명
                for j in range(self.df_stock.shape[0]):
                    val = self.df_stock[col_name][j] # 날짜 or 종가 요소
                    item = QTableWidgetItem(str(val))
                    self.tbl_stock_info.setItem(j,i,item)

            self.tbl_stock_info.verticalHeader().hide()
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
        if len(self.intrstSet) > 0 :
            stockDict = set()
            for ticker in self.intrstSet:
                stockDict.add(self.tickerDict[ticker])

            columns = list(stockDict.intersection(set(self.df_stock.columns.tolist())))     
            columns.append('Date')
            self.server.saveStock(self.df_stock[columns].to_dict())
        else:
            self.server.clearStock()
        pass
        


if __name__=="__main__":
    # 프로그램 실행
    app = QApplication(sys.argv)
    #인스턴스 생성
    myWindow = WindowClass()
    # 화면 생성
    myWindow.show()
    app.exec_()

    
    
