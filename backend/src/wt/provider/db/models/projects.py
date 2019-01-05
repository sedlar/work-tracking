from wt.provider.db.provider import metadata
from sqlalchemy import Table, Column, Integer


projects_table = Table(
    "projects",
    metadata,
    Column("id", Integer(), primary_key=True, autoincrement=True),
)


class DbProjectModel():
    def create_project(self):
        return
