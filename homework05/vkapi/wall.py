import textwrap
import typing as tp
from math import ceil
from string import Template
from time import sleep

import pandas as pd  # type: ignore
from pandas import json_normalize
from vkapi.config import VK_CONFIG
from vkapi.exceptions import APIError
from vkapi.session import Session


def get_posts_2500(
    owner_id: str = "",
    domain: str = "",
    offset: int = 0,
    count: int = 10,
    max_count: int = 2500,
    filter: str = "owner",
    extended: int = 0,
    fields: tp.Optional[tp.List[str]] = None,
) -> tp.Dict[str, tp.Any]:
    """
    Возвращает 2500 записей состены пользователи или сообщества.
    """
    # Some data for query
    base_domain = VK_CONFIG["domain"]
    access_token = VK_CONFIG["access_token"]
    v = VK_CONFIG["version"]

    # New session
    session = Session(base_url=base_domain)

    # Max count couldn't be more than 2500
    if max_count > 2500:
        max_count = 2500

    # If should get count less than max_count
    if max_count > count:
        max_count = count

    # VKScript code
    code = f"""
    var shift = {offset};
    var posts = [];
    var count = {ceil(max_count / 25)}; 

    while(shift - {offset} < {max_count}) {{
        posts.push(API.wall.get({{
            "owner_id": "{owner_id}",
            "domain": "{domain}",
            "offset": shift,
            "count": count,
            "filter": "{filter}",
            "extended": {extended},
            "fields": "{fields}",
            "v": {v},
        }}));

        shift = shift + count;
    }}

    return posts;
    """

    # Post request with execute method
    response = session.post(
        "execute",
        data={
            "code": code,
            "access_token": access_token,
            "v": v,
        }
    )
    data = response.json()

    # Check the response contains correct data
    if "response" not in data:
        # Throw exception
        raise APIError(data)

    # Result posts list
    result_posts = []

    # Return response data
    for posts in data['response']:
        result_posts.extend(posts['items'])

    return result_posts #type: ignore


def get_wall_execute(
    owner_id: str = "",
    domain: str = "",
    offset: int = 0,
    count: int = 10,
    max_count: int = 2500,
    filter: str = "owner",
    extended: int = 0,
    fields: tp.Optional[tp.List[str]] = None,
    progress=None,
) -> pd.DataFrame:
    """
    Возвращает список записей со стены пользователя или сообщества.

    @see: https://vk.com/dev/wall.get

    :param owner_id: Идентификатор пользователя или сообщества, со стены которого необходимо получить записи.
    :param domain: Короткий адрес пользователя или сообщества.
    :param offset: Смещение, необходимое для выборки определенного подмножества записей.
    :param count: Количество записей, которое необходимо получить (0 - все записи).
    :param max_count: Максимальное число записей, которое может быть получено за один запрос.
    :param filter: Определяет, какие типы записей на стене необходимо получить.
    :param extended: 1 — в ответе будут возвращены дополнительные поля profiles и groups, содержащие информацию о пользователях и сообществах.
    :param fields: Список дополнительных полей для профилей и сообществ, которые необходимо вернуть.
    :param progress: Callback для отображения прогресса.
    """
    # Some data for query
    base_domain = VK_CONFIG["domain"]
    access_token = VK_CONFIG["access_token"]
    v = VK_CONFIG["version"]

    # First request query
    code = f"""
    return API.wall.get({{
        "owner_id": "{owner_id}",
        "domain": "{domain}",
        "offset": {offset},
        "count": 1,
        "filter": "{filter}",
        "extended": {extended},
        "v": {v}
    }});
    """

    # New session
    session = Session(base_url=base_domain)

    # Post request with execute method
    response = session.post(
        url="execute",
        data={
            "code": code,
            "access_token": access_token,
            "v": v,
        },
    ).json()

    # Check the response contains correct data
    if "response" not in response:
        # Throw exception
        raise APIError(response)

    all_posts_count = response['response']['count']

    # If count is 0 method should return all posts
    if count == 0 or count > all_posts_count:
        count = all_posts_count

    # Counter for loopping
    counter = range(ceil(count / max_count))

    # Wrap with progress handler
    if progress != None:
        counter = progress(counter)

    # Result posts list
    posts =[] #type: ignore
    
    # Next count to get_posts_2500 func
    next_count = count
    
    for i in counter:
        # Wait 1 second between each 3 requests
        if (i % 3 == 0):
            sleep(1)

        # Try to get data
        try:
            next_posts = get_posts_2500(
                owner_id=owner_id,
                domain=domain,
                offset=offset + len(posts),
                count=next_count,
                max_count=max_count,
                filter=filter,
                extended=extended,  
                fields=fields,
            )
            # Add to result list
            posts.extend(next_posts)
            # Sub posts that were getted
            next_count -= max_count

        except Exception as e:
            APIError(str(e))
    
    # JSON data into a flat table
    return json_normalize(posts)
