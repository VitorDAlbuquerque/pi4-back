import firebase_admin
from firebase_admin import credentials, db
from Controller.listAll.listAllBradesco import listAllBradesco
from Controller.listAll.listAllCaixa import listAllCaixa
from Controller.listAll.listAllSantander import listAllSantander
from Controller.listAll.listAllItau import listAllItau
from config import cred

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://lobotomia-18768-default-rtdb.firebaseio.com/'
    })

def upload_all_banks():
    data_bradesco = listAllBradesco()
    data_caixa = listAllCaixa()
    data_santander = listAllSantander()
    data_itau = listAllItau()
    all_data = data_bradesco + data_caixa + data_santander + data_itau

    ref = db.reference('test_all_banks')
    ref.delete()
    print("All banks data deleted.")

    ref.set(all_data)
    print("All banks data uploaded.")

def delete_all_banks():
    ref = db.reference('test_all_banks')
    ref.delete()
    print("All banks data deleted.")
