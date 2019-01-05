from wt.provider.db.provider import metadata
from sqlalchemy import Table, Column, Integer, String, Binary


auth_table = Table(
    "auth",
    metadata,
    Column("id", Integer(), primary_key=True, autoincrement=True),
    Column("user", String(64), unique=True),
    Column("password", Binary(256)),
)


class DbAuthModel():
    def create_user(self):
        return


    def authorize_user(self, username, password):
        pass
