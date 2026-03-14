def ok(data=None, msg="success", code=200):
    return {"code": code, "data": data, "msg": msg}, code


def fail(msg="error", code=500, data=None):
    return {"code": code, "data": data, "msg": msg}, code
