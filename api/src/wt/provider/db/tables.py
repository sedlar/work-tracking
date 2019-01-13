from copy import deepcopy

from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    DateTime,
    UniqueConstraint,
    DECIMAL,
    LargeBinary,
    Boolean,
)

from wt.common import Currency
from wt.entities.deliverables import DeliverableStatus
from wt.ids import ObjectType
from wt.entities.issues import IssueType
from wt.entities.projects import ProjectStatus
from wt.provider.db import METADATA
from wt.provider.db._columns import (
    ID_COLUMN_TYPE,
    PROJECT_ID_COLUMN_REFERENCE,
    PROJECT_ID_COLUMN_TYPE,
    OBJECT_ID_COLUMN_REFERENCE,
    PARENT_ID_COLUMN_REFERENCE,
)
from wt.provider.db._utils import get_enum_length

FILES_TABLE = Table(
    "files",
    METADATA,
    Column("id", Integer(), primary_key=True, autoincrement=True),
    deepcopy(PARENT_ID_COLUMN_REFERENCE),
    Column("uri", String(2048), index=True, nullable=False),
    Column("created_on", DateTime(), nullable=False),
    UniqueConstraint("parent_id", "uri")
)
LINKS_TABLE = Table(
    "links",
    METADATA,
    Column("id", Integer(), primary_key=True, autoincrement=True),
    deepcopy(PARENT_ID_COLUMN_REFERENCE),
    Column("uri", String(2048), nullable=False),
    Column("title", String(126), nullable=False),
    Column("description", String(4096), nullable=False),
    Column("created_on", DateTime(), nullable=False),
    UniqueConstraint("parent_id", "uri")
)
TASKS_TABLE = Table(
    "tasks",
    METADATA,
    Column("id", Integer(), primary_key=True, autoincrement=True),
    deepcopy(PARENT_ID_COLUMN_REFERENCE),
    Column("task", String(1024), nullable=False),
    Column("completed", Boolean(), nullable=False),
    Column("created_on", DateTime(), nullable=False),
    UniqueConstraint("parent_id", "task")
)
TAGS_TABLE = Table(
    "tags",
    METADATA,
    Column("id", Integer(), primary_key=True, autoincrement=True),
    deepcopy(PARENT_ID_COLUMN_REFERENCE),
    Column("tag", String(50), index=True, nullable=False),
    Column("created_on", DateTime(), nullable=False),
    UniqueConstraint("parent_id", "tag")
)
DELIVERABLES_TABLE = Table(
    "deliverables",
    METADATA,
    deepcopy(OBJECT_ID_COLUMN_REFERENCE),
    deepcopy(PROJECT_ID_COLUMN_REFERENCE),
    Column("name", String(128), nullable=False),
    Column("status", String(get_enum_length(DeliverableStatus)), nullable=False),
    Column("description", String(), nullable=False),
    Column("date_opened", DateTime(), nullable=False),
    Column("date_closed", DateTime(), nullable=True),
    Column("deadline", DateTime(), nullable=True),
    Column("created_on", DateTime(), nullable=False),
)
IDS_COUNTER_TABLE = Table(
    "ids_counter",
    METADATA,
    Column("project_id", ID_COLUMN_TYPE, primary_key=True),
    Column("next_id", Integer(), nullable=False),
)
OBJECTS_TRACKER_TABLE = Table(
    "objects_tracker",
    METADATA,
    Column("id", ID_COLUMN_TYPE, primary_key=True),
    deepcopy(PROJECT_ID_COLUMN_REFERENCE),
    Column("type", String(get_enum_length(ObjectType)), nullable=False),
)
PROJECTS_TABLE = Table(
    "projects",
    METADATA,
    Column("project_id", PROJECT_ID_COLUMN_TYPE, primary_key=True),
    Column("name", String(128), nullable=False),
    Column("status", String(get_enum_length(ProjectStatus)), nullable=False),
    Column("date_opened", DateTime(), nullable=False),
    Column("date_closed", DateTime(), nullable=True),
    Column("deadline", DateTime(), nullable=True),
    Column("hour_rate_amount", DECIMAL(), nullable=True),
    Column("hour_rate_currency", String(get_enum_length(Currency)), nullable=True),
    Column("description", String(), nullable=False),
    Column("limitations_and_restrictions", String(), nullable=False),
    Column("goals_and_metrics", String(), nullable=False),
    Column("primary_color", String(7), nullable=False),
    Column("secondary_color", String(7), nullable=False),
    Column("created_on", DateTime(), nullable=False),
)
ISSUES_TABLE = Table(
    "issues",
    METADATA,
    deepcopy(OBJECT_ID_COLUMN_REFERENCE),
    deepcopy(PROJECT_ID_COLUMN_REFERENCE),
    Column("name", String(128), nullable=False),
    Column("description", String(), nullable=False),
    Column("external_type", String(256), nullable=False),
    Column("status", String(get_enum_length(IssueType)), nullable=False),
    Column("priority", String(get_enum_length(IssueType)), nullable=False),
    Column("type", String(get_enum_length(IssueType)), nullable=False),
    Column("date_opened", DateTime(), nullable=False),
    Column("date_closed", DateTime(), nullable=True),
    Column("deadline", DateTime(), nullable=True),
    Column("hour_rate_amount", DECIMAL(), nullable=True),
    Column("hour_rate_currency", String(get_enum_length(Currency)), nullable=True),
    Column("estimated_duration", DECIMAL(), nullable=True),
    Column("created_on", DateTime(), nullable=False),
)
USER_TABLE = Table(
    "users",
    METADATA,
    Column("id", Integer(), primary_key=True, autoincrement=True),
    Column("username", String(64), unique=True, nullable=False),
    Column("password", LargeBinary(256), nullable=False),
)