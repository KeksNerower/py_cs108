import pandas as pd
import requests
import textwrap

from pandas.io.json import json_normalize
from string import Template
from tqdm import tqdm

from vkapi.config import VK_CONFIG


def get_wall_execute(
    owner_id: str = "",
    domain: str = "",
    offset: int = 0,
    count: int = 10,
    filter: str = "owner",
    extended: str = "",
    fields: str = "",
    v: str = "5.126",
    progress=None,
) -> pd.DataFrame:
    """
    Возвращает список записей со стены пользователя или сообщества.

    @see: https://vk.com/dev/wall.get 

    :param owner_id: Идентификатор пользователя или сообщества, со стены которого необходимо получить записи.
    :param domain: Короткий адрес пользователя или сообщества.
    :param offset: Смещение, необходимое для выборки определенного подмножества записей.
    :param count: Количество записей, которое необходимо получить (0 - все записи).
    :param filter: Определяет, какие типы записей на стене необходимо получить.
    :param extended: 1 — в ответе будут возвращены дополнительные поля profiles и groups, содержащие информацию о пользователях и сообществах.
    :param fields: Список дополнительных полей для профилей и сообществ, которые необходимо вернуть.
    :param v: Версия API.
    :param progress: Callback для отображения прогресса.
    """
    
    # Some data for query
    base_domain = VK_CONFIG["domain"]
    access_token = VK_CONFIG["access_token"]
    v = VK_CONFIG["version"]

    # Params
    params = f'''
    "owner_id": {owner_id},
    "domain": {domain},
    "offset": {offset},
    "count": {count},
    "filter": {filter},
    "extended": {extended},
    "fields": {fields},
    "v": {v},
    '''

    # Code field for request
    code = "return API.wall.get({" + params + "});"

    # Post request with execute method
    response = requests.post(
    url=f"{base_domain}/execute",
        data={
            "code": code,
            "access_token": access_token,
            "v": v,
        }
    )