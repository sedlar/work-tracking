class User:
    def __init__(self, username):
        self.username = username


class BoundUser(User):
    def __init__(self, id_, user):
        """
        Args:
            id_ (int):
            user (User):
        """
        self.ident = id_
        super().__init__(user.username)
