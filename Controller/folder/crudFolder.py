import firebase_admin
from firebase_admin import credentials, db
import uuid
from config import cred

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://lobotomia-18768-default-rtdb.firebaseio.com/'
    })

def list_folders() -> list | None:
    ref = db.reference('folders')
    folders = ref.get()
    return folders if folders else None

def create_folder(folder_name: str) -> str | None:
    ref = db.reference('folders')

    folders = ref.get() or {}
    for folder_id, folder in folders.items():
        if folder.get("name") == folder_name:
            return None  

    folder_id = str(uuid.uuid4())
    ref.child(folder_id).set({"id": folder_id, "name": folder_name})
    return folder_id

def read_folder(folder_id: str) -> dict | None:
    ref = db.reference('folders').child(folder_id)
    data = ref.get()
    return data if data else None

def update_folder(folder_id: str, new_name: str) -> bool:
    ref = db.reference('folders').child(folder_id)
    if not ref.get():
        return False
    ref.update({"name": new_name})
    return True

def delete_folder(folder_id: str) -> bool:
    ref = db.reference('folders').child(folder_id)
    if not ref.get():
        return False
    ref.delete()
    return True

def add_property_to_folder(folder_id: str, property_id: str) -> bool:

    property_ref = db.reference('test_bradesco').child(property_id)
    if not property_ref.get():
        return False 

    folder_ref = db.reference('folders').child(folder_id)
    folder = folder_ref.get()
    if not folder:
        return False 

    properties = folder.get("properties", [])
    if property_id not in properties:
        properties.append(property_id)
        folder_ref.update({"properties": properties})
    return True

def remove_property_from_folder(folder_id: str, property_id: str) -> bool:
    folder_ref = db.reference('folders').child(folder_id)
    folder = folder_ref.get()
    if not folder or "properties" not in folder:
        return False

    properties = folder["properties"]
    if property_id in properties:
        properties.remove(property_id)
        folder_ref.update({"properties": properties})
        return True
    return False

