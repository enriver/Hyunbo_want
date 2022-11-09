import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import key

#Firebase database 인증 및 앱 초기화
cred = credentials.Certificate(key.cred_json)
firebase_admin.initialize_app(cred, {
    'databaseURL' : key.db_address
})

dir = db.reference()
print(dir.get())

dir = db.reference('가격/종가')
print(dir.get())