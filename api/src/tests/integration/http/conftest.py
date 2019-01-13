import base64
import json

from pytest import fixture
from werkzeug.datastructures import Headers


@fixture
def api_request(client):
    def func(method, url, body=None, auth=None):
        headers = Headers()
        if auth:
            data_input = "{username}:{password}".format(**auth)
            encoded_auth = base64.b64encode(data_input.encode("utf-8"))
            headers.add("Authorization", "Basic " + encoded_auth.decode("ascii"))

        return client.open(
            "/v1" + url,
            data=json.dumps(body),
            content_type='application/json',
            headers=headers,
            method=method,
        )
    return func


@fixture
def authorized_api_request(api_request, user):
    def func(method, url, body=None):
        return api_request(
            method,
            url,
            body,
            auth={"username": user.username, "password": "password"}
        )
    return func


EMPTY_STATS = {
    "progress": 0,
    "bilance_cost": {
        "amount": 0,
        "currency": "CZK"
    },
    "bilance_duration": 0,
}