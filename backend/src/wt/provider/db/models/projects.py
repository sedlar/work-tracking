from sqlalchemy import Table, Column, Integer

from wt.provider.db.provider import METADATA

PROJECTS_TABLE = Table(
    "projects",
    METADATA,
    Column("id", Integer(), primary_key=True, autoincrement=True),
)


class DbProjectModel():
    def create_project(self):
        pass
