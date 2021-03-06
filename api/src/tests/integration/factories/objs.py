from wt.entities.projects import Project, ProjectStatus
from wt.entities.deliverables import BoundDeliverable, DeliverableStatus, Deliverable
from wt.entities.issues import BoundIssue, IssuePriority, IssueType, IssueStatus, Issue
from wt.ids import EntityId
from datetime import datetime
from wt.fields.files import File
from decimal import Decimal
from wt.common import Money, Currency
from wt.fields.links import Link
from wt.fields.tasks import Task
from wt.fields.tags import Tag
from wt.costs.timesheets import Timesheet
from wt.costs.expenditures import Expenditure, ExpenditureStatus, ExpenditureType


def create_project(
        project_id="PRJ",
        name="Dummy project",
        status=ProjectStatus.open,
        description="Description",
        limitations_and_restrictions="Limitations and Restrictions",
        goals_and_metrics="Goals and Metrics",
        hour_rate=None,
        primary_color="#343434",
        secondary_color="#a1a1a1",
        files=None,
        date_opened=datetime(year=2019, month=1, day=1, hour=10, minute=30, second=5),
        date_closed=datetime(year=2019, month=1, day=2, hour=10, minute=30, second=5),
        deadline=datetime(year=2019, month=1, day=3, hour=10, minute=30, second=5),
):
    if not hour_rate:
        hour_rate = create_money()
    if files is None:
        files = [File("File1"), File("File2")]

    return Project(
        project_id=EntityId(project_id),
        name=name,
        status=status,
        description=description,
        limitations_and_restrictions=limitations_and_restrictions,
        goals_and_metrics=goals_and_metrics,
        hour_rate=hour_rate,
        primary_color=primary_color,
        secondary_color=secondary_color,
        files=files,
        date_opened=date_opened,
        date_closed=date_closed,
        deadline=deadline,
    )


def create_money(amount: Decimal=Decimal("600.50"), currency: Currency=Currency.czk):
    return Money(
        amount=amount,
        currency=currency,
    )


def create_bound_deliverable(
        object_id="PRJ-1",
        name="Dummy project",
        status=DeliverableStatus.open,
        description="Description",
        date_opened=datetime(year=2019, month=1, day=1, hour=10, minute=30, second=5),
        date_closed=datetime(year=2019, month=1, day=2, hour=10, minute=30, second=5),
        deadline=datetime(year=2019, month=1, day=3, hour=10, minute=30, second=5),
):
    return BoundDeliverable(
        object_id=EntityId(object_id),
        deliverable=create_deliverable(
            name=name,
            status=status,
            description=description,
            date_opened=date_opened,
            date_closed=date_closed,
            deadline=deadline,
        )
    )


def create_deliverable(
        name="Dummy deliverable",
        status=DeliverableStatus.open,
        description="Description deliverable",
        date_opened=datetime(year=2019, month=1, day=1, hour=10, minute=30, second=5),
        date_closed=datetime(year=2019, month=1, day=2, hour=10, minute=30, second=5),
        deadline=datetime(year=2019, month=1, day=3, hour=10, minute=30, second=5),
):
    return Deliverable(
        name=name,
        status=status,
        description=description,
        date_opened=date_opened,
        date_closed=date_closed,
        deadline=deadline,
    )


def create_bound_issue(
        object_id="PRJ-1",
        name="Dummy issue",
        status=IssueStatus.open,
        type=IssueType.bug,
        priority=IssuePriority.critical,
        description="Description issue",
        date_opened=datetime(year=2019, month=1, day=1, hour=10, minute=30, second=5),
        date_closed=datetime(year=2019, month=1, day=2, hour=10, minute=30, second=5),
        deadline=datetime(year=2019, month=1, day=3, hour=10, minute=30, second=5),
        estimated_duration=Decimal(10),
        external_type="external_type",
        files=None,
        links=None,
        tags=None,
        tasks=None,
        hour_rate=None
):
    return BoundIssue(
        object_id=EntityId(object_id),
        issue=create_issue(
            name=name,
            status=status,
            type=type,
            priority=priority,
            description=description,
            date_opened=date_opened,
            date_closed=date_closed,
            deadline=deadline,
            estimated_duration=estimated_duration,
            external_type=external_type,
            files=files,
            links=links,
            tags=tags,
            tasks=tasks,
            hour_rate=hour_rate,
        )
    )


def create_issue(
        name="Dummy issue",
        status=IssueStatus.open,
        type=IssueType.bug,
        priority=IssuePriority.critical,
        description="Description issue",
        date_opened=datetime(year=2019, month=1, day=1, hour=10, minute=30, second=5),
        date_closed=datetime(year=2019, month=1, day=2, hour=10, minute=30, second=5),
        deadline=datetime(year=2019, month=1, day=3, hour=10, minute=30, second=5),
        estimated_duration=Decimal(10),
        external_type="external_type",
        files=None,
        links=None,
        tags=None,
        tasks=None,
        hour_rate=None
):
    if files is None:
        files = [File("File1"), File("File2")]
    if links is None:
        links = [create_link(), create_link("www.zoho.cz", "zoho", "zoho")]
    if tags is None:
        tags = [Tag("X"), Tag("Y")]
    if tasks is None:
        tasks = [create_task(), create_task("Task", True)]
    return Issue(
        name=name,
        status=status,
        type_=type,
        priority=priority,
        description=description,
        date_opened=date_opened,
        date_closed=date_closed,
        deadline=deadline,
        estimated_duration=estimated_duration,
        external_type=external_type,
        files=files,
        links=links,
        tags=tags,
        tasks=tasks,
        hour_rate=hour_rate,
    )


def create_link(
        uri="www.google.com",
        name="Google",
        description="Google link",
):
    return Link(
        uri=uri,
        title=name,
        description=description,
    )


def create_task(
        task="Implement work tracking api",
        completed=False,
):
    return Task(
        task=task,
        completed=completed,
    )


def create_file(
        uri="www.seznam.cz"
):
    return File(uri)


def create_tag(tag):
    return Tag(tag)


def create_timesheet(
        description="Timesheet description",
        date_opened=datetime(year=2002, month=3, day=13),
        duration=Decimal(15.5),

):
    return Timesheet(
        description=description,
        date_opened=date_opened,
        duration=duration,
    )


def create_expenditure(
        name="Expenditure name",
        description="Expenditure description",
        status=ExpenditureStatus.approved,
        type_=ExpenditureType.freelance,
        date_opened=datetime(2005, 4, 8),
        date_closed=datetime(2005, 4, 9),
        deadline=datetime(2005, 4, 10),
        files=None,
        cost=None,
):
    if files is None:
        files = [create_file("ExpFile1"), create_file("ExpFile2")]
    if not cost:
        cost = create_money()

    return Expenditure(
        name=name,
        description=description,
        status=status,
        type_=type_,
        date_opened=date_opened,
        date_closed=date_closed,
        deadline=deadline,
        files=files,
        cost=cost,
    )
