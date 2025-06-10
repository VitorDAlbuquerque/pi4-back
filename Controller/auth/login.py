import firebase_admin
from firebase_admin import credentials, db
import hashlib
from Controller.models.user import User
from Controller.auth.auth_utils import generate_token
from config import cred

if not firebase_admin._apps:
 firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://lobotomia-18768-default-rtdb.firebaseio.com/'
    })

def hash_password(password: str) -> str:
    """Hashes a password using SHA-256."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def login(username: str, password: str) -> str | None:
    ref = db.reference('users')
    user_data = ref.child(username).get()
    if not user_data:
        return None

    user = User.from_dict(user_data)
    hashed_pw = hash_password(password)
    if user.password == hashed_pw:
        return generate_token(username)
    return None
