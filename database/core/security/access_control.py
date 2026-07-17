class AccessControl:

    def __init__(self):
        self.permissions = {}

    def grant(self, user, permission):
        if user not in self.permissions:
            self.permissions[user] = []

        self.permissions[user].append(permission)

    def check(self, user, permission):

        return permission in self.permissions.get(
            user,
            []
        )
