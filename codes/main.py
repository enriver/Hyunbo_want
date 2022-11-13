from server import Server
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic


# UI파일 연결
form_class = uic.loadUiType("Hyunbo_UI.ui")[0]

class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 서버 연결
        server = Server()
        


        


if __name__=="__main__":
    # 프로그램 실행
    app = QApplication(sys.argv)
    #인스턴스 생성
    myWindow = WindowClass()
    # 화면 생성
    myWindow.show()
    app.exec_()

    
    
