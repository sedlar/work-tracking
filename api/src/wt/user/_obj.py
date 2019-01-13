class User:
    def __init__(self, username, hashed_password):
        """

        Args:
            username (str):
            hashed_password (bytes):
        """
        self.username = username
        self.hashed_password = hashed_password


class BoundUser(User):
    def __init__(self, id_, user):
        """
        Args:
            id_ (int):
            user (User):
        """
        self.ident = id_
        super().__init__(user.username, user.hashed_password)
