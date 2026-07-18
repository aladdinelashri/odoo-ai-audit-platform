import hashlib


class AuthManager:

    def __init__(self):
        self.users = {}


    def create_user(
        self,
        username,
        password
    ):

        self.users[username] = (
            hashlib.sha256(
                password.encode()
            ).hexdigest()
        )


    def authenticate(
        self,
        username,
        password
    ):

        hashed = hashlib.sha256(
            password.encode()
        ).hexdigest()

        return self.users.get(
            username
        ) == hashed
