import firebase_admin
from firebase_admin import credentials, db

from config import cred

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://lobotomia-18768-default-rtdb.firebaseio.com/'
    })


def list_all_propertys():
    ref = db.reference('test_all_banks')
    data = ref.get()
    # If data is None, return empty list
    if not data:
        return []
    # If data is a dict, return its values as a list of dicts
    if isinstance(data, dict):
        return list(data.values())
    # If data is already a list, return as is
    return data
