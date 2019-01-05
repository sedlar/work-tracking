from sqlalchemy import Table, Column, Integer, String, Binary

from wt.provider.db.provider import METADATA

AUTH_TABLE = Table(
    "auth",
    METADATA,
    Column("id", Integer(), primary_key=True, autoincrement=True),
    Column("user", String(64), unique=True),
    Column("password", Binary(256)),
)


class DbAuthModel():
    def create_user(self):
        pass

    def authorize_user(self, username, password):
        pass
