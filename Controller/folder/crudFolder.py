import firebase_admin
from firebase_admin import credentials, db
import uuid
from config import cred
from Controller.filter.filter import pickProperty
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://lobotomia-18768-default-rtdb.firebaseio.com/'
    })

def list_folders() -> list:
    ref = db.reference('folders')
    folders = ref.get()
    if not folders:
        return []
    return list(folders.values())

def create_folder(folder_name: str) -> str | None:
    ref = db.reference('folders')

    folders = ref.get() or {}
    for folder_id, folder in folders.items():
        if folder.get("name") == folder_name:
            return None  

    folder_id = str(uuid.uuid4())
    ref.child(folder_id).set({"id": folder_id, "name": folder_name})
    return folder_id

def read_folder(folder_id: str) -> list | None:
    folder_ref = db.reference('folders').child(folder_id)
    folder = folder_ref.get()
    if not folder:
        return None

    all_properties = db.reference('test_all_banks').get() or {}

    property_ids = folder.get("properties", [])
    properties = []
    for prop in all_properties.values():
        if str(prop.get("id")) in [str(pid) for pid in property_ids]:
            properties.append(prop)

    return properties if properties else []

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
    # Ensure the property exists by its "id" field
    property_data = pickProperty(property_id)
    print(property_data)
    if not property_data:
        return False

    folder_ref = db.reference('folders').child(folder_id)
    folder = folder_ref.get()
    if not folder:
        return False
    

    # Ensure "properties" is a list
    properties = folder.get("properties")
    if not isinstance(properties, list):
        properties = []

    # Only add if not already present (as string for consistency)
    if str(property_id) not in [str(pid) for pid in properties]:
        properties.append(str(property_id))
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

