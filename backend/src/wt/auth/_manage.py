from typing import Optional

import bcrypt

from wt.auth._model import AuthModel
from wt.auth._obj import BoundUser


def add_user(auth_model: AuthModel, username: str, password: str) -> BoundUser:
    return auth_model.create_user(username, hash_password(password))


def authenticate(auth_model: AuthModel, username, password) -> Optional[BoundUser]:
    user = auth_model.get_user(username)

    if user and check_password(password, user.hashed_password):
        return user
    return None


def hash_password(password):
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt(),
    )


def check_password(password, hashed_password):
    return bcrypt.checkpw(
        password.encode("utf-8"),
        hashed_password,
    )
