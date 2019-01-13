from functools import wraps

from wt.common.errors import ObjectDoesNotExist, BadRequest


def get_error_response(ex):
    return {
        "code": ex.error_code.value,
        "message": ex.message
    }


def handle_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ObjectDoesNotExist as ex:
            return get_error_response(ex), 404
        except BadRequest as ex:
            return get_error_response(ex), 400

    return wrapper


DUMMY_STATS = {
    "progress": 0,
    "bilance_duration": 0,
    "bilance_cost": {
        "amount": 0,
        "currency": "CZK",
    },
}
