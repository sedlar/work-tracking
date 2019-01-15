from tests.integration.factories.objs import create_timesheet
from wt.costs.timesheets import BoundTimesheet
from wt.ids import EntityId

ENTITY_ID = EntityId("ABC-1")
OTHER_PROJECT_ENTITY_ID = EntityId("BBB-1")


def test_create_timesheet(timesheets_model):
    timesheet = create_timesheet()
    bound_timesheet = timesheets_model.create_timesheet(ENTITY_ID, timesheet)

    assert bound_timesheet == BoundTimesheet(bound_timesheet.simple_id, timesheet)
    assert timesheets_model.get_timesheets(ENTITY_ID, 0, 1)


def test_get_timesheets(timesheets_model):
    timesheet = create_timesheet()
    bound_timesheet = timesheets_model.create_timesheet(ENTITY_ID, timesheet)
    timesheets_model.create_timesheet(OTHER_PROJECT_ENTITY_ID, timesheet)

    assert timesheets_model.get_timesheets(ENTITY_ID, 0, 1) == [bound_timesheet]


def test_delete_timesheet(timesheets_model):
    timesheet = create_timesheet()
    bound_timesheet = timesheets_model.create_timesheet(ENTITY_ID, timesheet)
    timesheets_model.delete_timesheet(bound_timesheet.simple_id)

    assert not timesheets_model.get_timesheets(ENTITY_ID, 0, 1)


def test_delete_entity_timesheets(timesheets_model):
    timesheet = create_timesheet()
    timesheets_model.create_timesheet(ENTITY_ID, timesheet)
    timesheets_model.delete_entity_timesheets(ENTITY_ID)

    assert not timesheets_model.get_timesheets(ENTITY_ID, 0, 1)


def test_list_timesheets_offset(timesheets_model):
    timesheet = create_timesheet()
    timesheets_model.create_timesheet(ENTITY_ID, timesheet)
    bound_timesheet = timesheets_model.create_timesheet(ENTITY_ID, timesheet)

    assert timesheets_model.get_timesheets(ENTITY_ID, 1, 1) == [bound_timesheet]


def test_timesheets_limit(timesheets_model):
    timesheet = create_timesheet()
    bound_timesheet = timesheets_model.create_timesheet(ENTITY_ID, timesheet)
    timesheets_model.create_timesheet(ENTITY_ID, timesheet)

    assert timesheets_model.get_timesheets(ENTITY_ID, 0, 1) == [bound_timesheet]
