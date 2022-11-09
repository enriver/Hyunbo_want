from firebase import Firebase
from krx_info import KRX_Info as KRX

if __name__=="__main__":
    stock = KRX()
    db = Firebase()
    
    if db.checkDB('SAVE_CODE_DICT') is False:
        db.setAddress('CODE_DICT')

        codeDict = stock.getCodeDict()
        db.setDB(codeDict)

        #print(db.getDB())
    
