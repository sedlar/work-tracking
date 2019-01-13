from typing import Optional

from wt.user._obj import BoundUser


class UserModel:
    def create_user(self, username: str, hashed_password: bytes) -> BoundUser:
        raise NotImplementedError()

    def get_user(self, username: str) -> Optional[BoundUser]:
        raise NotImplementedError()
