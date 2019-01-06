from typing import Optional

import bcrypt

from wt.user._model import UserModel
from wt.user._obj import BoundUser


def authenticate(user_model: UserModel, username, password) -> Optional[BoundUser]:
    user = user_model.get_user(username)

    if user and check_password(password, user.hashed_password):
        return user
    return None


def check_password(password, hashed_password):
    return bcrypt.checkpw(
        password.encode("utf-8"),
        hashed_password,
    )
