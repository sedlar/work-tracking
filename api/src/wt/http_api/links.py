from flask_injector import inject

from wt.http_api._common import handle_errors
from wt.ids import EntityId
from wt.links import EntityLinksApi


@inject
@handle_errors
def put_link(links_api: EntityLinksApi, object_id, other_object_id):
    links_api.create_link(EntityId(object_id), EntityId(other_object_id))
    return {}, 201


@inject
@handle_errors
def delete_link(links_api: EntityLinksApi, object_id, other_object_id):
    links_api.delete_link(EntityId(object_id), EntityId(other_object_id))
    return {}, 200
