from datetime import datetime
from decimal import Decimal

import pytest

from tests.integration.factories.objs import create_project, create_money
from wt.common import Currency
from wt.ids import EntityId
from wt.entities.projects import ProjectStatus, ProjectDoesNotExist


def test_create_project(projects_model):
    project = create_project()
    projects_model.put_project(project)
    saved_project = projects_model.get_project(project.project_id)
    assert project == saved_project


def test_update_project(projects_model):
    project = create_project()
    projects_model.put_project(project)

    updated_project = create_project(
        name="Test",
        status=ProjectStatus.completed,
        description="DESC",
        limitations_and_restrictions="Limitations and Restrictions2",
        goals_and_metrics="Goals and Metrics2",
        hour_rate=create_money(Decimal("800"), Currency.eur),
        primary_color="#343435",
        secondary_color="#a1a1a2",
        files=[],
        date_opened=datetime(year=2020, month=1, day=1, hour=10, minute=30),
        date_closed=datetime(year=2020, month=1, day=2, hour=10, minute=30),
        deadline=datetime(year=2020, month=1, day=3, hour=10, minute=30),
    )
    projects_model.put_project(updated_project)

    saved_project = projects_model.get_project(project.project_id)
    assert updated_project == saved_project


def test_get_projects(projects_model):
    project1 = create_project()
    projects_model.put_project(project1)

    project2 = create_project(project_id="ZZZZZ", name="Other project")
    projects_model.put_project(project2)

    projects = projects_model.get_projects(0, 2)
    assert projects == [project1, project2]


def test_delete_project(projects_model):
    project = create_project()
    projects_model.put_project(project)

    projects_model.delete_project(project.project_id)
    assert not projects_model.get_projects(0, 1)


def test_delete_project_files(projects_model, files_model):
    project = create_project()
    projects_model.put_project(project)

    projects_model.delete_project(project.project_id)
    assert not files_model.get_entity_files(project.project_id)


def test_get_no_project(projects_model):
    with pytest.raises(ProjectDoesNotExist):
        projects_model.get_project(EntityId("ABC"))


def test_delete_no_project(projects_model):
    with pytest.raises(ProjectDoesNotExist):
        projects_model.delete_project(EntityId("ABC"))
