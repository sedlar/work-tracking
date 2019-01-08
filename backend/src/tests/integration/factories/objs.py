from wt.projects import Project, ProjectStatus
from datetime import datetime
from wt.files import File
from decimal import Decimal
from wt.common import Money, Currency


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
        project_id=project_id,
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