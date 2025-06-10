import firebase_admin
from firebase_admin import credentials, db
from config import cred

if not firebase_admin._apps:
 firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://lobotomia-18768-default-rtdb.firebaseio.com/'
    })

def delete_user(username: str) -> bool:
    ref = db.reference('users')
    user_ref = ref.child(username)
    if user_ref.get() is None:
        return False 
    user_ref.delete()
    return True