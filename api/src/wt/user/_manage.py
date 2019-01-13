import bcrypt

from wt.user._model import UserModel
from wt.user._obj import BoundUser


def add_user(user_model: UserModel, username: str, password: str) -> BoundUser:
    return user_model.create_user(username, hash_password(password))


def hash_password(password):
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt(),
    )
