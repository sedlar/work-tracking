from tests.integration.factories.objs import create_project, create_deliverable
from wt.entities.ids import EntityId


def test_project_recreate_resets_object_ids(projects_api, deliverables_api):
    project = create_project()
    projects_api.put_project(project)
    deliverable = deliverables_api.create_deliverable(project.project_id, create_deliverable())

    deliverables_api.delete_deliverable(deliverable.object_id)
    projects_api.delete_project(project.project_id)

    projects_api.put_project(project)
    deliverable = deliverables_api.create_deliverable(project.project_id, create_deliverable())
    assert deliverable.object_id == EntityId.from_parts(project.project_id, 1)
