import transaction
from flask_injector import inject

from wt.entities.deliverables import DeliverableSerializer, DeliverableDeserializer, DeliverablesApi
from wt.http_api._common import handle_errors
from wt.ids import EntityId
from wt.statistics import StatisticsSerializer, StatisticsApi


@inject
@handle_errors
def get_deliverables(
        deliverables_api: DeliverablesApi,
        serializer: DeliverableSerializer,
        offset,
        limit,
):
    # pylint: disable=too-many-arguments
    with transaction.manager:
        deliverables = deliverables_api.get_deliverables(
            project_id=None,
            related_entity_id=None,
            offset=offset,
            limit=limit
        )
    return {"deliverables": serializer.serialize_deliverables(deliverables)}, 200


@inject
@handle_errors
def get_deliverable(
        deliverables_api: DeliverablesApi,
        statistics_api: StatisticsApi,
        serializer: DeliverableSerializer,
        statistics_serializer: StatisticsSerializer,
        deliverable_id,
):
    deliverable_id = EntityId(deliverable_id)
    with transaction.manager:
        deliverable = deliverables_api.get_deliverable(deliverable_id)
        statistics = statistics_api.get_deliverable_statistics(deliverable_id)

    return {
        "deliverable": serializer.serialize_deliverable(deliverable),
        "stats": statistics_serializer.serialize_statistics(statistics),
    }, 200


@inject
@handle_errors
def put_deliverable(
        deliverables_api: DeliverablesApi,
        deserializer: DeliverableDeserializer,
        deliverable_id,
        body,
):
    deliverable = deserializer.deserialize_bound_deliverable(
        deliverable_id,
        body["deliverable"]
    )
    with transaction.manager:
        deliverables_api.edit_deliverable(deliverable)
    return {}, 200


@inject
@handle_errors
def delete_deliverable(
        deliverables_api: DeliverablesApi,
        deliverable_id
):
    with transaction.manager:
        deliverables_api.delete_deliverable(EntityId(deliverable_id))
    return {}, 200
