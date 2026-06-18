MIXIN_REGISTRY = {}
_ID_COUNTER = 0


def _get_next_id():
    global _ID_COUNTER
    _ID_COUNTER += 1
    return _ID_COUNTER
