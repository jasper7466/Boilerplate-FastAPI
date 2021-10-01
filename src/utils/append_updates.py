"""
Утилита append_updates. Модифицирует выбранные ключи словаря
"""


def append_updates(origin, updates):
    """
    Утилита для изменения выбранных ключей словаря
    :param origin: исходный словарь
    :param updates: словарь с обновлениями
    :return: модифицированный словарь
    """
    for key, value in updates.dict(exclude_unset=True):
        setattr(origin, key, value)

    return origin
