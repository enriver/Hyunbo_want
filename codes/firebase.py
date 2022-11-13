import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import secretKey
import json

class Firebase:
    __address=None
    __dir=None

    def __init__(self):
        #Firebase database 인증 및 앱 초기화
        cred = credentials.Certificate(secretKey.cred_json)
        firebase_admin.initialize_app(cred, {
            'databaseURL' : secretKey.db_url_address
        })

        self.__address = 'DEFAULT_SETTING'
        self.__dir = db.reference(self.__address)

    # reference 설정
    def setAddress(self, __address=None):
        if __address is None :
            print('DB address 설정을 해주세요')

        self.__address = __address
        self.__dir = db.reference(self.__address)
        
    
    # 현재 reference 주소 반환
    def getAddress(self):
        if self.__address is None:
            print('DB address 설정이 되지 않았습니다.')
            return
        return self.__address

    # 현재 reference 경로에 set (NEW)
    def setDB(self, values):
        json_values = json.dumps(values, ensure_ascii=False)
        self.__dir.set(json_values)

    # 현재 reference 경로에 push (NODE NEW)
    def pushDB(self, values):
        json_values = json.dumps(values, ensure_ascii=False)
        self.__dir.push(json_values)

    # 현재 reference 경로에 update
    def updateDB(self,dict_values):
        self.__dir.update(dict_values)


    # 현재 reference 경로에 있는 값 추출
    def getDB(self):
        return self.__dir.get()

    #
    def checkDB(self,path):
        self.__dir = db.reference(self.__address+'/'+path)
        
        if self.__dir.get() is True:
            return True
        else:
            self.__dir.set(True)
            return False
