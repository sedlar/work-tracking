from typing import Optional

from sqlalchemy import Table, Column, Integer, String, Binary, insert, select

from wt.auth import AuthModel, BoundUser, User
from wt.provider.db.provider import METADATA

AUTH_TABLE = Table(
    "auth",
    METADATA,
    Column("id", Integer(), primary_key=True, autoincrement=True),
    Column("username", String(64), unique=True),
    Column("password", Binary(256)),
)


class DbAuthModel(AuthModel):
    def __init__(self, engine):
        self._engine = engine.connect()

    def create_user(self, username, hashed_password):
        query = insert(AUTH_TABLE).values(username=username, password=hashed_password)
        result = self._engine.execute(query)
        return BoundUser(
            id_=result.inserted_primary_key[0],
            user=User(
                username=username,
                hashed_password=hashed_password,
            ),
        )

    def get_user(self, username: str) -> Optional[BoundUser]:
        query = select([AUTH_TABLE]).where(AUTH_TABLE.c.username == username)
        result = self._engine.execute(query).fetchone()
        if result is None:
            return None
        return BoundUser(
            id_=result["id"],
            user=User(
                username=result["username"],
                hashed_password=result["password"]
            )
        )