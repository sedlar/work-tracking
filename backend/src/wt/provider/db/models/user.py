from typing import Optional

from sqlalchemy import Table, Column, Integer, String, LargeBinary, insert, select
from zope.sqlalchemy import mark_changed

from wt.provider.db.provider import METADATA, DbModel
from wt.user import UserModel, BoundUser, User

USER_TABLE = Table(
    "users",
    METADATA,
    Column("id", Integer(), primary_key=True, autoincrement=True),
    Column("username", String(64), unique=True, nullable=False),
    Column("password", LargeBinary(256), nullable=False),
)


class DbUserModel(UserModel, DbModel):
    def create_user(self, username, hashed_password):
        query = insert(USER_TABLE).values(username=username, password=hashed_password)
        result = self._session.execute(query)
        mark_changed(self._session)
        return BoundUser(
            id_=result.inserted_primary_key[0],
            user=User(
                username=username,
                hashed_password=hashed_password,
            ),
        )

    def get_user(self, username: str) -> Optional[BoundUser]:
        query = select([USER_TABLE]).where(USER_TABLE.c.username == username)
        result = self._session.execute(query).fetchone()
        if result is None:
            return None
        return BoundUser(
            id_=result["id"],
            user=User(
                username=result["username"],
                hashed_password=result["password"]
            )
        )
