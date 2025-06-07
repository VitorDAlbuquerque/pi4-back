import firebase_admin
from firebase_admin import credentials, db
import hashlib
from Controller.models.user import User


cred = credentials.Certificate(r"D:\Area de trabalho\BackPi4Python\pi4-back\Controller\auth\serviceAccountKey.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://lobotomia-18768-default-rtdb.firebaseio.com/'
    })

def hash_password(password: str) -> str:
    """Hashes a password using SHA-256."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def register(username: str, password: str, email: str) -> bool:
    ref = db.reference('users')
    users = ref.get() or {}

    if username in users:
        return False  

    hashed_pw = hash_password(password)
    user = User(username=username, email=email, password=hashed_pw)
    ref.child(username).set(user.to_dict())
    return True

# register('Testee', 'testeaaaa', 'testee@example.com')