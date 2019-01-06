from wt.auth._manage import authenticate
from wt.auth._model import AuthModel
from wt.global_injector import INJECTOR


# FIXME: @inject doesn't work here. Fix it and remove global injector completely
def basic_auth(username, password, **_):
    auth_model = INJECTOR.get(AuthModel)
    user = authenticate(auth_model, username, password)
    if user:
        return {"sub": user}
    return None
