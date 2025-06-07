from dataclasses import dataclass

@dataclass
class User:
    username: str
    email: str
    password: str 

    @staticmethod
    def from_dict(data: dict):
        return User(
            username=data.get('username', ''),
            email=data.get('email', ''),
            password=data.get('password', '')
        )

    def to_dict(self):
        return {
            'username': self.username,
            'email': self.email,
            'password': self.password
        }