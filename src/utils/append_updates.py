def append_updates(origin, updates):
    for k, v in updates.dict(exclude_unset=True):
        setattr(origin, k, v)

    return origin
