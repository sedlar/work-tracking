import transaction

from wt.costs.timesheets import TimesheetsSerializer, TimesheetsDeserializer, TimesheetsApi
from wt.ids import SimpleEntityType, SimpleId, EntityId
from wt.http_api._common import handle_errors


@handle_errors
def post_timesheet(deserializer: TimesheetsDeserializer, timesheets_api: TimesheetsApi, body):
    timesheet = deserializer.deserialize_timesheet(body["timesheet"])
    entity_id = EntityId(body["timesheet"]["parent_id"])
    with transaction.manager:
        bound_timesheet = timesheets_api.create_timesheet(entity_id, timesheet)
    return {"id": bound_timesheet.simple_id.simple_id}, 201


@handle_errors
def delete_timesheet(timesheets_api: TimesheetsApi, timesheet_id):
    with transaction.manager:
        timesheets_api.delete_timesheet(SimpleId(SimpleEntityType.timesheet, timesheet_id))
    return {}, 200


@handle_errors
def get_timesheets(
        serializer: TimesheetsSerializer,
        timesheets_api: TimesheetsApi,
        object_id,
        offset,
        limit
):
    with transaction.manager:
        timesheets = timesheets_api.get_timesheets(EntityId(object_id), offset, limit)
    serialized_timesheets = serializer.serialize_timesheets(timesheets)
    return {"timesheets": serialized_timesheets}, 200
