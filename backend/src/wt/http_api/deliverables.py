import transaction
from flask_injector import inject

from wt.http_api._common import DUMMY_STATS
from wt.http_api._common import handle_errors
from wt.entities.deliverables import DeliverableSerializer, DeliverableDeserializer, DeliverablesApi
from wt.ids import EntityId


@inject
@handle_errors
def get_deliverable(
        deliverables_api: DeliverablesApi,
        serializer: DeliverableSerializer,
        deliverable_id,
):
    with transaction.manager:
        deliverable = deliverables_api.get_deliverable(EntityId(deliverable_id))

    return {
        "deliverable": serializer.serialize_deliverable(deliverable),
        "stats": DUMMY_STATS,
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
