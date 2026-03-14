from app.utils.timeutil import now_iso


def get_bulk_status(tag_keys):
    data = {}
    for key in tag_keys:
        data[key] = {"value": False, "quality": "good", "ts": now_iso()}
    return data
