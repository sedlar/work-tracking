from wt.common.errors import BadRequest


class LinkAlreadyExists(BadRequest):
    error_code = "link_already_exists"
    message = "This link already exists."


class LinkDoesNotExist(BadRequest):
    error_code = "link_does_not_exist"
    message = "This link does not exist."
