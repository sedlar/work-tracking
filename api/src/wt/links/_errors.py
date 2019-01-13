from wt.common.errors import BadRequest, ErrorCodes


class LinkAlreadyExists(BadRequest):
    error_code = ErrorCodes.link_already_exists
    message = "This link already exists."


class LinkDoesNotExist(BadRequest):
    error_code = ErrorCodes.link_does_not_exist
    message = "This link does not exist."


class InvalidLinkToItself(BadRequest):
    error_code = ErrorCodes.invalid_link_to_itself
    message = "Link of entity to itself can't be created."


class InvalidLinkedEntities(BadRequest):
    error_code = ErrorCodes.invalid_linked_entities

    def __init__(self, entity, other_entity):
        super().__init__()
        self.message = "It is not possible to link {entity} with {other_entity}".format(
            entity=entity.value,
            other_entity=other_entity.value,
        )


class InvalidLinkBetweenProjects(BadRequest):
    error_code = ErrorCodes.invalid_link_between_projects
    message = "Links between entities in different projects can't be created."
