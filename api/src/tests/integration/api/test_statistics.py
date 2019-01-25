from tests.integration.factories.objs import (
    create_project,
    create_issue,
    create_deliverable,
    create_timesheet,
    create_expenditure,
)
from decimal import Decimal
from wt.common import Money, Currency
from wt.costs.expenditures import ExpenditureStatus


def test_project_progress_empty(statistics_api):
    project = create_project()

    statistics = statistics_api.get_project_statistics(project.project_id)
    assert statistics.progress is None


def test_project_progress(statistics_api, put_project, post_issue, post_timesheet):
    project = create_project()
    put_project(project)
    # Issue with several timesheets
    bound_issue = post_issue(project.project_id, create_issue(estimated_duration=Decimal(5)))
    post_timesheet(bound_issue.object_id, create_timesheet(duration=Decimal(2)))
    post_timesheet(bound_issue.object_id, create_timesheet(duration=Decimal(1)))
    post_timesheet(bound_issue.object_id, create_timesheet(duration=Decimal(1)))
    # Issue with overtime
    bound_issue = post_issue(project.project_id, create_issue(estimated_duration=Decimal(2)))
    post_timesheet(bound_issue.object_id, create_timesheet(duration=Decimal(10)))
    # Estimated issue without timesheet
    post_issue(project.project_id, create_issue(estimated_duration=Decimal(3)))
    # Unestimated issue with timesheet
    bound_issue = post_issue(project.project_id, create_issue(estimated_duration=None))
    post_timesheet(bound_issue.object_id, create_timesheet(duration=Decimal(10)))
    # Issue estimated to zero
    post_issue(project.project_id, create_issue(estimated_duration=Decimal(0)))
    bound_issue = post_issue(project.project_id, create_issue(estimated_duration=Decimal(0)))
    post_timesheet(bound_issue.object_id, create_timesheet(duration=Decimal(10)))

    statistics = statistics_api.get_project_statistics(project.project_id)
    assert statistics.progress == Decimal("0.6")


def test_deliverable_progress_no_entities(statistics_api, put_project, post_deliverable):
    project = create_project()
    put_project(project)
    bound_deliverable = post_deliverable(project.project_id, create_deliverable())

    statistics = statistics_api.get_deliverable_statistics(bound_deliverable.object_id)
    assert statistics.progress is None


def test_deliverable_progress(
        statistics_api,
        put_project,
        post_issue,
        post_timesheet,
        post_deliverable,
        put_link
):
    project = create_project()
    put_project(project)
    bound_deliverable = post_deliverable(project.project_id, create_deliverable())

    # Issue with several timesheets
    bound_issue = post_issue(project.project_id, create_issue(estimated_duration=Decimal(5)))
    put_link(bound_deliverable.object_id, bound_issue.object_id)
    post_timesheet(bound_issue.object_id, create_timesheet(duration=Decimal(2)))
    post_timesheet(bound_issue.object_id, create_timesheet(duration=Decimal(1)))
    post_timesheet(bound_issue.object_id, create_timesheet(duration=Decimal(1)))
    # Issue with overtime
    bound_issue = post_issue(project.project_id, create_issue(estimated_duration=Decimal(2)))
    put_link(bound_deliverable.object_id, bound_issue.object_id)
    post_timesheet(bound_issue.object_id, create_timesheet(duration=Decimal(10)))
    # Estimated issue without timesheet
    bound_issue = post_issue(project.project_id, create_issue(estimated_duration=Decimal(3)))
    put_link(bound_deliverable.object_id, bound_issue.object_id)
    # Unestimated issue with timesheet
    bound_issue = post_issue(project.project_id, create_issue(estimated_duration=None))
    put_link(bound_deliverable.object_id, bound_issue.object_id)
    post_timesheet(bound_issue.object_id, create_timesheet(duration=Decimal(10)))
    # Issue estimated to zero
    bound_issue = post_issue(project.project_id, create_issue(estimated_duration=Decimal(0)))
    put_link(bound_deliverable.object_id, bound_issue.object_id)
    bound_issue = post_issue(project.project_id, create_issue(estimated_duration=Decimal(0)))
    put_link(bound_deliverable.object_id, bound_issue.object_id)
    post_timesheet(bound_issue.object_id, create_timesheet(duration=Decimal(10)))

    statistics = statistics_api.get_deliverable_statistics(bound_deliverable.object_id)
    assert statistics.progress == Decimal("0.6")


def test_issue_progress_issue(statistics_api, put_project, post_issue, post_timesheet):
    project = create_project()
    put_project(project)

    # Issue with several timesheets
    bound_issue = post_issue(project.project_id, create_issue(estimated_duration=Decimal(5)))
    post_timesheet(bound_issue.object_id, create_timesheet(duration=Decimal(2)))
    post_timesheet(bound_issue.object_id, create_timesheet(duration=Decimal(1)))
    post_timesheet(bound_issue.object_id, create_timesheet(duration=Decimal(1)))

    statistics = statistics_api.get_entity_statistics(bound_issue.object_id)
    assert statistics.progress == Decimal("0.8")


def test_issue_progress_issue_no_timesheets(statistics_api, put_project, post_issue):
    project = create_project()
    put_project(project)

    # Issue without timesheets
    bound_issue = post_issue(project.project_id, create_issue(estimated_duration=Decimal(5)))

    statistics = statistics_api.get_entity_statistics(bound_issue.object_id)
    assert statistics.progress == Decimal(0)


def test_project_overall_progress_empty(statistics_api):
    project = create_project()

    statistics = statistics_api.get_project_statistics(project.project_id)
    assert statistics.overall_progress is None


def test_project_overall_progress(statistics_api, put_project, post_issue, post_timesheet):
    project = create_project()
    put_project(project)
    # Issue with several timesheets
    bound_issue = post_issue(project.project_id, create_issue(estimated_duration=Decimal(5)))
    post_timesheet(bound_issue.object_id, create_timesheet(duration=Decimal(2)))
    post_timesheet(bound_issue.object_id, create_timesheet(duration=Decimal(1)))
    post_timesheet(bound_issue.object_id, create_timesheet(duration=Decimal(1)))
    # Issue with overtime
    bound_issue = post_issue(project.project_id, create_issue(estimated_duration=Decimal(2)))
    post_timesheet(bound_issue.object_id, create_timesheet(duration=Decimal(10)))
    # Estimated issue without timesheet
    post_issue(project.project_id, create_issue(estimated_duration=Decimal(3)))
    # Unestimated issue with timesheet
    bound_issue = post_issue(project.project_id, create_issue(estimated_duration=None))
    post_timesheet(bound_issue.object_id, create_timesheet(duration=Decimal(10)))
    # Issue estimated to zero
    post_issue(project.project_id, create_issue(estimated_duration=Decimal(0)))

    statistics = statistics_api.get_project_statistics(project.project_id)
    assert statistics.overall_progress == Decimal("2.4")


def test_deliverable_overall_progress(
    statistics_api,
    put_project,
    post_issue,
    post_timesheet,
    post_deliverable,
    put_link
):
    project = create_project()
    put_project(project)
    bound_deliverable = post_deliverable(project.project_id, create_deliverable())

    # Issue with several timesheets
    bound_issue = post_issue(project.project_id, create_issue(estimated_duration=Decimal(5)))
    put_link(bound_deliverable.object_id, bound_issue.object_id)
    post_timesheet(bound_issue.object_id, create_timesheet(duration=Decimal(2)))
    post_timesheet(bound_issue.object_id, create_timesheet(duration=Decimal(1)))
    post_timesheet(bound_issue.object_id, create_timesheet(duration=Decimal(1)))
    # Issue with overtime
    bound_issue = post_issue(project.project_id, create_issue(estimated_duration=Decimal(2)))
    put_link(bound_deliverable.object_id, bound_issue.object_id)
    post_timesheet(bound_issue.object_id, create_timesheet(duration=Decimal(10)))
    # Estimated issue without timesheet
    bound_issue = post_issue(project.project_id, create_issue(estimated_duration=Decimal(3)))
    put_link(bound_deliverable.object_id, bound_issue.object_id)
    # Unestimated issue with timesheet
    bound_issue = post_issue(project.project_id, create_issue(estimated_duration=None))
    put_link(bound_deliverable.object_id, bound_issue.object_id)
    post_timesheet(bound_issue.object_id, create_timesheet(duration=Decimal(10)))
    # Issue estimated to zero
    bound_issue = post_issue(project.project_id, create_issue(estimated_duration=Decimal(0)))
    put_link(bound_deliverable.object_id, bound_issue.object_id)
    bound_issue = post_issue(project.project_id, create_issue(estimated_duration=Decimal(0)))
    put_link(bound_deliverable.object_id, bound_issue.object_id)
    post_timesheet(bound_issue.object_id, create_timesheet(duration=Decimal(10)))

    statistics = statistics_api.get_deliverable_statistics(bound_deliverable.object_id)
    assert statistics.overall_progress == Decimal("3.4")


def test_issue_overall_progress_issue(statistics_api, put_project, post_issue, post_timesheet):
    project = create_project()
    put_project(project)

    # Issue with several timesheets
    bound_issue = post_issue(project.project_id, create_issue(estimated_duration=Decimal(5)))
    post_timesheet(bound_issue.object_id, create_timesheet(duration=Decimal(2)))

    statistics = statistics_api.get_entity_statistics(bound_issue.object_id)
    assert statistics.overall_progress == Decimal("0.4")


def test_issue_overall_progress_issue_overtime(
        statistics_api,
        put_project,
        post_issue,
        post_timesheet
):
    project = create_project()
    put_project(project)

    # Issue with several timesheets
    bound_issue = post_issue(project.project_id, create_issue(estimated_duration=Decimal(5)))
    post_timesheet(bound_issue.object_id, create_timesheet(duration=Decimal(2)))
    post_timesheet(bound_issue.object_id, create_timesheet(duration=Decimal(1)))
    post_timesheet(bound_issue.object_id, create_timesheet(duration=Decimal("4.5")))

    statistics = statistics_api.get_entity_statistics(bound_issue.object_id)
    assert statistics.overall_progress == Decimal("1.5")


def test_issue_overall_progress_issue_no_timesheets(
        statistics_api,
        put_project,
        post_issue,
):
    project = create_project()
    put_project(project)

    # Issue with several timesheets
    bound_issue = post_issue(project.project_id, create_issue(estimated_duration=Decimal(5)))

    statistics = statistics_api.get_entity_statistics(bound_issue.object_id)
    assert statistics.overall_progress == Decimal(0)


def test_issue_overall_progress_issue_unestimated(
        statistics_api,
        put_project,
        post_issue,
):
    project = create_project()
    put_project(project)

    # Issue with several timesheets
    bound_issue = post_issue(project.project_id, create_issue(estimated_duration=None))

    statistics = statistics_api.get_entity_statistics(bound_issue.object_id)
    assert statistics.overall_progress is None


def test_project_estimated_duration_no_entities(statistics_api, put_project):
    project = create_project()
    put_project(project)

    statistics = statistics_api.get_project_statistics(project.project_id)
    assert statistics.estimated_duration == Decimal(0)


def test_project_estimated_duration(statistics_api, put_project, post_issue):
    project = create_project()
    put_project(project)
    post_issue(project.project_id, create_issue(estimated_duration=Decimal(5)))
    post_issue(project.project_id, create_issue(estimated_duration=Decimal(2)))
    post_issue(project.project_id, create_issue(estimated_duration=Decimal(3)))
    post_issue(project.project_id, create_issue(estimated_duration=None))
    post_issue(project.project_id, create_issue(estimated_duration=Decimal(0)))

    statistics = statistics_api.get_project_statistics(project.project_id)
    assert statistics.estimated_duration == Decimal(10)


def test_deliverable_estimated_duration(
    statistics_api,
    put_project,
    post_issue,
    put_link,
    post_deliverable
):
    project = create_project()
    put_project(project)
    bound_deliverable = post_deliverable(project.project_id, create_deliverable())
    bound_issue = post_issue(project.project_id, create_issue(estimated_duration=Decimal(5)))
    put_link(bound_deliverable.object_id, bound_issue.object_id)
    bound_issue = post_issue(project.project_id, create_issue(estimated_duration=Decimal(2)))
    put_link(bound_deliverable.object_id, bound_issue.object_id)
    bound_issue = post_issue(project.project_id, create_issue(estimated_duration=Decimal(3)))
    put_link(bound_deliverable.object_id, bound_issue.object_id)
    bound_issue = post_issue(project.project_id, create_issue(estimated_duration=None))
    put_link(bound_deliverable.object_id, bound_issue.object_id)
    bound_issue = post_issue(project.project_id, create_issue(estimated_duration=Decimal(0)))
    put_link(bound_deliverable.object_id, bound_issue.object_id)

    statistics = statistics_api.get_deliverable_statistics(bound_deliverable.object_id)
    assert statistics.estimated_duration == Decimal(10)


def test_issue_estimated_duration(
    statistics_api,
    put_project,
    post_issue,

):
    project = create_project()
    put_project(project)
    bound_issue = post_issue(project.project_id, create_issue(estimated_duration=Decimal(5)))

    statistics = statistics_api.get_entity_statistics(bound_issue.object_id)
    assert statistics.estimated_duration == Decimal(5)


def test_issue_estimated_duration_no_estimate(
        statistics_api,
        put_project,
        post_issue,

):
    project = create_project()
    put_project(project)
    bound_issue = post_issue(project.project_id, create_issue(estimated_duration=None))

    statistics = statistics_api.get_entity_statistics(bound_issue.object_id)
    assert statistics.estimated_duration == Decimal(0)


def test_project_burned_duration_no_entities(statistics_api, put_project):
    project = create_project()
    put_project(project)

    statistics = statistics_api.get_project_statistics(project.project_id)
    assert statistics.burned_duration == Decimal(0)


def test_project_burned_duration_no_timesheets(statistics_api, put_project, post_issue):
    project = create_project()
    put_project(project)
    post_issue(project.project_id, create_issue(estimated_duration=Decimal(5)))

    statistics = statistics_api.get_project_statistics(project.project_id)
    assert statistics.burned_duration == Decimal(0)


def test_project_burned_duration(statistics_api, put_project, post_issue, post_timesheet):
    project = create_project()
    put_project(project)
    # Issue with several timesheets
    bound_issue = post_issue(project.project_id, create_issue(estimated_duration=Decimal(5)))
    post_timesheet(bound_issue.object_id, create_timesheet(duration=Decimal(2)))
    post_timesheet(bound_issue.object_id, create_timesheet(duration=Decimal(1)))
    post_timesheet(bound_issue.object_id, create_timesheet(duration=Decimal(1)))
    # Issue with overtime
    bound_issue = post_issue(project.project_id, create_issue(estimated_duration=Decimal(2)))
    post_timesheet(bound_issue.object_id, create_timesheet(duration=Decimal(10)))
    # Estimated issue without timesheet
    post_issue(project.project_id, create_issue(estimated_duration=Decimal(3)))
    # Unestimated issue with timesheet
    bound_issue = post_issue(project.project_id, create_issue(estimated_duration=None))
    post_timesheet(bound_issue.object_id, create_timesheet(duration=Decimal(10)))
    # Issue estimated to zero
    post_issue(project.project_id, create_issue(estimated_duration=Decimal(0)))

    statistics = statistics_api.get_project_statistics(project.project_id)
    assert statistics.burned_duration == Decimal(24)


def test_deliverable_burned_duration(
    statistics_api,
    put_project,
    post_issue,
    post_timesheet,
    post_deliverable,
    put_link
):
    project = create_project()
    put_project(project)
    bound_deliverable = post_deliverable(project.project_id, create_deliverable())

    # Issue with several timesheets
    bound_issue = post_issue(project.project_id, create_issue(estimated_duration=Decimal(5)))
    put_link(bound_deliverable.object_id, bound_issue.object_id)
    post_timesheet(bound_issue.object_id, create_timesheet(duration=Decimal(2)))
    post_timesheet(bound_issue.object_id, create_timesheet(duration=Decimal(1)))
    post_timesheet(bound_issue.object_id, create_timesheet(duration=Decimal(1)))
    # Issue with overtime
    bound_issue = post_issue(project.project_id, create_issue(estimated_duration=Decimal(2)))
    put_link(bound_deliverable.object_id, bound_issue.object_id)
    post_timesheet(bound_issue.object_id, create_timesheet(duration=Decimal(10)))
    # Estimated issue without timesheet
    bound_issue = post_issue(project.project_id, create_issue(estimated_duration=Decimal(3)))
    put_link(bound_deliverable.object_id, bound_issue.object_id)
    # Unestimated issue with timesheet
    bound_issue = post_issue(project.project_id, create_issue(estimated_duration=None))
    put_link(bound_deliverable.object_id, bound_issue.object_id)
    post_timesheet(bound_issue.object_id, create_timesheet(duration=Decimal(10)))
    # Issue estimated to zero
    bound_issue = post_issue(project.project_id, create_issue(estimated_duration=Decimal(0)))
    put_link(bound_deliverable.object_id, bound_issue.object_id)

    statistics = statistics_api.get_deliverable_statistics(bound_deliverable.object_id)
    assert statistics.burned_duration == Decimal(24)


def test_issue_burned_duration(
    statistics_api,
    put_project,
    post_issue,
    post_timesheet,
):
    project = create_project()
    put_project(project)

    # Issue with several timesheets
    bound_issue = post_issue(project.project_id, create_issue(estimated_duration=Decimal(5)))
    post_timesheet(bound_issue.object_id, create_timesheet(duration=Decimal(2)))
    post_timesheet(bound_issue.object_id, create_timesheet(duration=Decimal(1)))
    post_timesheet(bound_issue.object_id, create_timesheet(duration=Decimal(1)))

    statistics = statistics_api.get_entity_statistics(bound_issue.object_id)
    assert statistics.burned_duration == Decimal(4)


def test_issue_burned_duration_no_timesheets(
        statistics_api,
        put_project,
        post_issue,
):
    project = create_project()
    put_project(project)

    # Issue without timesheets
    bound_issue = post_issue(project.project_id, create_issue(estimated_duration=Decimal(5)))

    statistics = statistics_api.get_entity_statistics(bound_issue.object_id)
    assert statistics.burned_duration == Decimal(0)


def test_project_estimated_cost_no_entities(statistics_api, put_project):
    project = create_project()
    put_project(project)

    statistics = statistics_api.get_project_statistics(project.project_id)
    assert statistics.estimated_cost == Money(Decimal(0), Currency.czk)


def test_project_estimated_cost(statistics_api, put_project, post_issue):
    project = create_project()
    put_project(project)
    # Issue with default project currency
    post_issue(project.project_id, create_issue(estimated_duration=Decimal(5)))
    # Issue with overriden currency
    post_issue(
        project.project_id,
        create_issue(
            estimated_duration=Decimal(2),
            hour_rate=Money(amount=Decimal(1000), currency=Currency.czk)
        )
    )
    # Issue without estimated duration
    post_issue(project.project_id, create_issue(estimated_duration=None))

    statistics = statistics_api.get_project_statistics(project.project_id)
    assert statistics.estimated_cost == Money(amount=Decimal("5002.5"), currency=Currency.czk)


def test_deliverable_estimated_cost(
        statistics_api,
        put_project,
        post_issue,
        put_link,
        post_deliverable
):
    project = create_project()
    put_project(project)
    bound_deliverable = post_deliverable(project.project_id, create_deliverable())

    # Issue with default project currency
    bound_issue = post_issue(project.project_id, create_issue(estimated_duration=Decimal(5)))
    put_link(bound_deliverable.object_id, bound_issue.object_id)
    # Issue with overriden currency
    bound_issue = post_issue(
        project.project_id,
        create_issue(
            estimated_duration=Decimal(2),
            hour_rate=Money(amount=Decimal(1000), currency=Currency.czk)
        )
    )
    put_link(bound_deliverable.object_id, bound_issue.object_id)
    # Issue without estimated duration
    bound_issue = post_issue(project.project_id, create_issue(estimated_duration=None))
    put_link(bound_deliverable.object_id, bound_issue.object_id)

    statistics = statistics_api.get_deliverable_statistics(bound_deliverable.object_id)
    assert statistics.estimated_cost == Money(amount=Decimal("5002.5"), currency=Currency.czk)


def test_issue_estimated_cost_default_currency(
    statistics_api,
    put_project,
    post_issue,
):
    project = create_project()
    put_project(project)

    # Issue with default project currency
    bound_issue = post_issue(project.project_id, create_issue(estimated_duration=Decimal(5)))

    statistics = statistics_api.get_entity_statistics(bound_issue.object_id)
    assert statistics.estimated_cost == Money(amount=Decimal("3002.5"), currency=Currency.czk)


def test_issue_estimated_cost_overriden_currency(
        statistics_api,
        put_project,
        post_issue,
):
    project = create_project()
    put_project(project)

    # Issue with overriden currency
    bound_issue = post_issue(
        project.project_id,
        create_issue(
            estimated_duration=Decimal(2),
            hour_rate=Money(amount=Decimal(1000), currency=Currency.czk)
        )
    )

    statistics = statistics_api.get_entity_statistics(bound_issue.object_id)
    assert statistics.estimated_cost == Money(amount=Decimal("2000"), currency=Currency.czk)


def test_issue_estimated_cost_no_estimate(
        statistics_api,
        put_project,
        post_issue,
):
    project = create_project()
    put_project(project)

    # Issue without estimated duration
    bound_issue = post_issue(project.project_id, create_issue(estimated_duration=None))

    statistics = statistics_api.get_entity_statistics(bound_issue.object_id)
    assert statistics.estimated_cost == Money(amount=Decimal(0), currency=Currency.czk)


def test_project_burned_cost(statistics_api, put_project, post_issue, post_timesheet):
    project = create_project()
    put_project(project)
    # Issue with default project currency
    bound_issue = post_issue(project.project_id, create_issue())
    post_timesheet(bound_issue.object_id, create_timesheet(duration=Decimal(2)))
    post_timesheet(bound_issue.object_id, create_timesheet(duration=Decimal(1)))
    post_timesheet(bound_issue.object_id, create_timesheet(duration=Decimal(1)))
    # Issue with overriden currency
    bound_issue = post_issue(
        project.project_id,
        create_issue(
            hour_rate=Money(Decimal(1000), currency=Currency.czk)
        )
    )
    post_timesheet(bound_issue.object_id, create_timesheet(duration=Decimal(10)))
    # Issue without timesheet
    post_issue(project.project_id, create_issue())

    statistics = statistics_api.get_project_statistics(project.project_id)
    assert statistics.burned_cost == Money(Decimal(12402), Currency.czk)


def test_deliverable_burned_cost(
    statistics_api,
    put_project,
    post_issue,
    post_timesheet,
    post_deliverable,
    put_link
):
    project = create_project()
    put_project(project)
    bound_deliverable = post_deliverable(project.project_id, create_deliverable())

    # Issue with default project currency
    bound_issue = post_issue(project.project_id, create_issue())
    put_link(bound_deliverable.object_id, bound_issue.object_id)
    post_timesheet(bound_issue.object_id, create_timesheet(duration=Decimal(2)))
    post_timesheet(bound_issue.object_id, create_timesheet(duration=Decimal(1)))
    post_timesheet(bound_issue.object_id, create_timesheet(duration=Decimal(1)))
    # Issue with overriden currency
    bound_issue = post_issue(
        project.project_id,
        create_issue(
            hour_rate=Money(Decimal(1000), currency=Currency.czk)
        )
    )
    put_link(bound_deliverable.object_id, bound_issue.object_id)
    post_timesheet(bound_issue.object_id, create_timesheet(duration=Decimal(10)))
    # Issue without timesheet
    bound_issue = post_issue(project.project_id, create_issue())
    put_link(bound_deliverable.object_id, bound_issue.object_id)

    statistics = statistics_api.get_deliverable_statistics(bound_deliverable.object_id)
    assert statistics.burned_cost == Money(Decimal(12402), Currency.czk)


def test_issue_burned_cost_default_currency(
    statistics_api,
    put_project,
    post_issue,
    post_timesheet,
):
    project = create_project()
    put_project(project)

    # Issue with default project currency
    bound_issue = post_issue(project.project_id, create_issue())
    post_timesheet(bound_issue.object_id, create_timesheet(duration=Decimal(2)))
    post_timesheet(bound_issue.object_id, create_timesheet(duration=Decimal(1)))
    post_timesheet(bound_issue.object_id, create_timesheet(duration=Decimal(1)))

    statistics = statistics_api.get_entity_statistics(bound_issue.object_id)
    assert statistics.burned_cost == Money(Decimal(2402), Currency.czk)


def test_issue_burned_cost_overriden_currency(
        statistics_api,
        put_project,
        post_issue,
        post_timesheet,
        post_deliverable,
        put_link
):
    project = create_project()
    put_project(project)

    # Issue with overriden currency
    bound_issue = post_issue(
        project.project_id,
        create_issue(
            hour_rate=Money(Decimal(1000), currency=Currency.czk)
        )
    )
    post_timesheet(bound_issue.object_id, create_timesheet(duration=Decimal(10)))

    statistics = statistics_api.get_entity_statistics(bound_issue.object_id)
    assert statistics.burned_cost == Money(Decimal(10000), Currency.czk)


def test_issue_burned_cost_no_timesheets(
        statistics_api,
        put_project,
        post_issue,
):
    project = create_project()
    put_project(project)

    # Issue without timesheet
    bound_issue = post_issue(project.project_id, create_issue())

    statistics = statistics_api.get_entity_statistics(bound_issue.object_id)
    assert statistics.burned_cost == Money(Decimal(0), Currency.czk)


def test_project_expenditures_cost_no_entities(statistics_api, put_project):
    project = create_project()
    put_project(project)

    statistics = statistics_api.get_project_statistics(project.project_id)
    assert statistics.burned_expenditures_cost == Money(Decimal(0), Currency.czk)


def test_project_expenditures_cost_no_expenditures(statistics_api, put_project, post_issue, post_expenditure):
    project = create_project()
    put_project(project)
    post_issue(project.project_id, create_issue())

    statistics = statistics_api.get_project_statistics(project.project_id)
    assert statistics.burned_expenditures_cost == Money(Decimal(0), Currency.czk)


def test_project_expenditures_cost(statistics_api, put_project, post_issue, post_expenditure):
    project = create_project()
    put_project(project)
    bound_issue = post_issue(project.project_id, create_issue(estimated_duration=Decimal(5)))
    post_expenditure(
        bound_issue.object_id,
        create_expenditure(cost=Money(Decimal(10), currency=Currency.czk))
    )
    post_expenditure(bound_issue.object_id, create_expenditure(status=ExpenditureStatus.submitted))
    post_expenditure(bound_issue.object_id, create_expenditure(status=ExpenditureStatus.refund))
    post_expenditure(
        bound_issue.object_id,
        create_expenditure(cost=Money(Decimal(100), currency=Currency.czk))
    )
    bound_issue = post_issue(project.project_id, create_issue())
    post_expenditure(
        bound_issue.object_id,
        create_expenditure(cost=Money(Decimal(1000), currency=Currency.czk))
    )
    post_issue(project.project_id, create_issue(estimated_duration=Decimal(3)))

    statistics = statistics_api.get_project_statistics(project.project_id)
    assert statistics.burned_expenditures_cost == Money(Decimal(1110), Currency.czk)


def test_deliverable_expenditures_cost(
        statistics_api,
        put_project,
        post_issue,
        post_expenditure,
        post_deliverable,
        put_link
):
    project = create_project()
    put_project(project)
    bound_deliverable = post_deliverable(project.project_id, create_deliverable())

    bound_issue = post_issue(project.project_id, create_issue(estimated_duration=Decimal(5)))
    put_link(bound_deliverable.object_id, bound_issue.object_id)
    post_expenditure(
        bound_issue.object_id,
        create_expenditure(cost=Money(Decimal(10), currency=Currency.czk))
    )
    post_expenditure(bound_issue.object_id, create_expenditure(status=ExpenditureStatus.submitted))
    post_expenditure(bound_issue.object_id, create_expenditure(status=ExpenditureStatus.refund))
    post_expenditure(
        bound_issue.object_id,
        create_expenditure(cost=Money(Decimal(100), currency=Currency.czk))
    )
    bound_issue = post_issue(project.project_id, create_issue())
    put_link(bound_deliverable.object_id, bound_issue.object_id)
    post_expenditure(
        bound_issue.object_id,
        create_expenditure(cost=Money(Decimal(1000), currency=Currency.czk))
    )
    bound_issue = post_issue(project.project_id, create_issue(estimated_duration=Decimal(3)))
    put_link(bound_deliverable.object_id, bound_issue.object_id)

    statistics = statistics_api.get_deliverable_statistics(bound_deliverable.object_id)
    assert statistics.burned_expenditures_cost == Money(Decimal(1110), Currency.czk)


def test_issue_expenditures_cost(
    statistics_api,
    put_project,
    post_issue,
    post_expenditure,
):
    project = create_project()
    put_project(project)

    bound_issue = post_issue(project.project_id, create_issue(estimated_duration=Decimal(5)))
    post_expenditure(
        bound_issue.object_id,
        create_expenditure(cost=Money(Decimal(10), currency=Currency.czk))
    )
    post_expenditure(bound_issue.object_id, create_expenditure(status=ExpenditureStatus.submitted))
    post_expenditure(bound_issue.object_id, create_expenditure(status=ExpenditureStatus.refund))
    post_expenditure(
        bound_issue.object_id,
        create_expenditure(cost=Money(Decimal(100), currency=Currency.czk))
    )

    statistics = statistics_api.get_entity_statistics(bound_issue.object_id)
    assert statistics.burned_expenditures_cost == Money(Decimal(110), Currency.czk)


def test_issue_expenditures_cost_no_expenditures(
        statistics_api,
        put_project,
        post_issue,
):
    project = create_project()
    put_project(project)

    bound_issue = post_issue(project.project_id, create_issue(estimated_duration=Decimal(5)))

    statistics = statistics_api.get_entity_statistics(bound_issue.object_id)
    assert statistics.burned_expenditures_cost == Money(Decimal(0), Currency.czk)
