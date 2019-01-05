class AuthModel:
    def create_user(self, user):
        raise NotImplementedError()

    def authorize(self, username, password):
        raise NotImplementedError()
