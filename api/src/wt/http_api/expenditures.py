import transaction

from wt.costs.expenditures import (
    ExpendituresSerializer,
    ExpendituresDeserializer,
    ExpendituresApi,
)
from wt.ids import SimpleEntityType, SimpleId, EntityId
from wt.http_api._common import handle_errors


@handle_errors
def post_expenditure(
        deserializer: ExpendituresDeserializer,
        expenditures_api: ExpendituresApi,
        body
):
    expenditure = deserializer.deserialize_expenditure(body["expenditure"])
    entity_id = EntityId(body["expenditure"]["parent_id"])
    with transaction.manager:
        bound_expenditure = expenditures_api.create_expenditure(entity_id, expenditure)
    return {"id": bound_expenditure.simple_id.simple_id}, 201


@handle_errors
def delete_expenditure(expenditures_api: ExpendituresApi, expenditure_id):
    with transaction.manager:
        expenditures_api.delete_expenditure(SimpleId(SimpleEntityType.expenditure, expenditure_id))
    return {}, 200


@handle_errors
def get_expenditures(
        expenditures_api: ExpendituresApi,
        serializer: ExpendituresSerializer,
        object_id,
        offset,
        limit
):
    with transaction.manager:
        expenditures = expenditures_api.get_expenditures(EntityId(object_id), offset, limit)
    serialized_expenditures = serializer.serialize_expenditures(expenditures)
    return {"expenditures": serialized_expenditures}, 200
