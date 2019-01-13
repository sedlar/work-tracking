from sqlalchemy import String, Column, ForeignKey

COLOR_COLUMN_TYPE = String(7)
PROJECT_ID_COLUMN_TYPE = String(5)
PROJECT_ID_COLUMN_REFERENCE = Column(
    "project_id",
    PROJECT_ID_COLUMN_TYPE,
    ForeignKey("projects.project_id", ondelete="RESTRICT"),
    index=True,
    nullable=False,
)
ID_COLUMN_TYPE = String(15)
PARENT_ID_COLUMN_REFERENCE = Column(
    "parent_id",
    ID_COLUMN_TYPE,
    index=True,
    nullable=False,
)
OBJECT_ID_COLUMN_REFERENCE = Column(
    "object_id",
    ID_COLUMN_TYPE,
    primary_key=True,
    nullable=False,
)
