import firebase_admin
from firebase_admin import credentials, db
from Controller.listAll.listAllBradesco import listAllBradesco


if not firebase_admin._apps:
    cred = credentials.Certificate("./serviceAccountKey.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://lobotomia-18768-default-rtdb.firebaseio.com/'
    })

def upload_test_bradesco():
    """Uploads all Bradesco objects to the 'test_bradesco' node in Firebase."""
    data = listAllBradesco()
    ref = db.reference('test_bradesco')
    ref.set(data)
    print("Test Bradesco data uploaded.")

def delete_test_bradesco():
    """Deletes the 'test_bradesco' node from Firebase."""
    ref = db.reference('test_bradesco')
    ref.delete()
    print("Test Bradesco data deleted.")
