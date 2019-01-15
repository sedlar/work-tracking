from tests.integration.factories.objs import create_expenditure
from wt.costs.expenditures import BoundExpenditure
from wt.ids import EntityId

ENTITY_ID = EntityId("ABC-1")
OTHER_PROJECT_ENTITY_ID = EntityId("BBB-1")


def test_create_minimal_expenditure(expenditures_model):
    expenditure = create_expenditure(date_closed=None, deadline=None, files=[])
    bound_expenditure = expenditures_model.create_expenditure(ENTITY_ID, expenditure)

    assert bound_expenditure == BoundExpenditure(bound_expenditure.simple_id, expenditure)


def test_create_full_expenditure(expenditures_model):
    expenditure = create_expenditure()
    bound_expenditure = expenditures_model.create_expenditure(ENTITY_ID, expenditure)

    assert bound_expenditure == BoundExpenditure(bound_expenditure.simple_id, expenditure)


def test_get_expenditures(expenditures_model):
    full_expenditure = create_expenditure()
    minimal_expenditure = create_expenditure(date_closed=None, deadline=None, files=[])
    full_bound_expenditure = expenditures_model.create_expenditure(ENTITY_ID, full_expenditure)
    minimal_bound_expenditure = expenditures_model.create_expenditure(
        ENTITY_ID,
        minimal_expenditure
    )

    loaded_expenditures = expenditures_model.get_expenditures(ENTITY_ID, 0, 2)
    assert loaded_expenditures == [full_bound_expenditure, minimal_bound_expenditure]


def test_delete_expenditure(expenditures_model):
    expenditure = create_expenditure()
    bound_expenditure = expenditures_model.create_expenditure(ENTITY_ID, expenditure)
    expenditures_model.delete_expenditure(bound_expenditure.simple_id)

    assert not expenditures_model.get_expenditures(ENTITY_ID, 0, 1)


def test_delete_entity_expenditures(expenditures_model):
    expenditure = create_expenditure()
    expenditures_model.create_expenditure(ENTITY_ID, expenditure)
    expenditures_model.delete_entity_expenditures(ENTITY_ID)

    assert not expenditures_model.get_expenditures(ENTITY_ID, 0, 1)


def test_list_expenditures_offset(expenditures_model):
    expenditure = create_expenditure()
    expenditures_model.create_expenditure(ENTITY_ID, expenditure)
    bound_expenditure = expenditures_model.create_expenditure(ENTITY_ID, expenditure)

    assert expenditures_model.get_expenditures(ENTITY_ID, 1, 1) == [bound_expenditure]


def test_expenditures_limit(expenditures_model):
    expenditure = create_expenditure()
    bound_expenditure = expenditures_model.create_expenditure(ENTITY_ID, expenditure)
    expenditures_model.create_expenditure(ENTITY_ID, expenditure)

    assert expenditures_model.get_expenditures(ENTITY_ID, 0, 1) == [bound_expenditure]
