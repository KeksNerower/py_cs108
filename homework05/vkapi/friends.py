import dataclasses
from math import ceil
from time import sleep
import typing as tp

from vkapi.config import VK_CONFIG
from vkapi.session import Session
from vkapi.exceptions import APIError

QueryParams = tp.Optional[tp.Dict[str, tp.Union[str, int]]]


@dataclasses.dataclass(frozen=True)
class FriendsResponse:
    count: int
    items: tp.Union[tp.List[int], tp.List[tp.Dict[str, tp.Any]]]


def get_friends(
    user_id: int, count: int = 5000, offset: int = 0, fields: tp.Optional[tp.List[str]] = None
) -> FriendsResponse:
    """
    Получить список идентификаторов друзей пользователя или расширенную информацию
    о друзьях пользователя (при использовании параметра fields).

    :param user_id: Идентификатор пользователя, список друзей для которого нужно получить.
    :param count: Количество друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества друзей.
    :param fields: Список полей, которые нужно получить для каждого пользователя.
    :return: Список идентификаторов друзей пользователя или список пользователей.
    """
    # Some data for query
    domain = VK_CONFIG["domain"]
    access_token = VK_CONFIG["access_token"]
    v = VK_CONFIG["version"]

    # New session
    session = Session(base_url=domain)

    # Get response
    response = session.get(
        "friends.get",
        params={
            "access_token": access_token,
            "user_id": user_id,
            "count": count,
            "offset": offset,
            "fields": fields,
            "v": v,
        },
    ).json()

    # Check the response contains correct data
    if "response" not in response:
        # Throw exception
        raise APIError(response)

    # Get friends data from response
    items = response['response']['items']

    # Return friends data
    return FriendsResponse(count=len(items), items=items)


class MutualFriends(tp.TypedDict):
    id: int
    common_friends: tp.List[int]
    common_count: int


# This function fails if target has private profile
def get_mutual(
    source_uid: tp.Optional[int] = None,
    target_uid: tp.Optional[int] = None,
    target_uids: tp.Optional[tp.List[int]] = None,
    order: str = "",
    count: tp.Optional[int] = None,
    offset: int = 0,
    progress=None,
) -> tp.Union[tp.List[int], tp.List[MutualFriends]]:
    """
    Получить список идентификаторов общих друзей между парой пользователей.

    :param source_uid: Идентификатор пользователя, чьи друзья пересекаются с друзьями пользователя с идентификатором target_uid.
    :param target_uid: Идентификатор пользователя, с которым необходимо искать общих друзей.
    :param target_uids: Cписок идентификаторов пользователей, с которыми необходимо искать общих друзей.
    :param order: Порядок, в котором нужно вернуть список общих друзей.
    :param count: Количество общих друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества общих друзей.
    :param progress: Callback для отображения прогресса.
    """
    # Some data for query
    domain = VK_CONFIG["domain"]
    access_token = VK_CONFIG["access_token"]
    v = VK_CONFIG["version"]
    
    # New session
    session = Session(base_url=domain)

    # If target_uid not None will work just with it
    if (target_uid != None):
        targets = [target_uid]
    else:
        targets = target_uids

    # Found items list
    items = []

    # Counter for loopping
    counter = range(0, len(targets), 100)

    # Wrap with progress handler
    if progress != None:
        counter = progress(counter)

    # Process each handred of friends
    for i in counter:
        # Wait 1 second between each 3 requests
        if (i % 3 == 0):
            sleep(1)

        # Get response
        response = session.get(
            "friends.getMutual",
            params={
                "access_token": access_token,
                "source_uid": source_uid,
                "target_uids": ','.join(map(str, targets[i:i+100])),
                "order": order,
                "count": count,
                "offset": offset,
                "v": v,
            },
        ).json()

        # Check the response contains correct data
        if "response" not in response:
            # Throw exception
            raise APIError(response)
                
        # For each target in response 
        for target in response['response']:
            # Append target data to items list
            items.append(MutualFriends(
                    id=target['id'], 
                    common_friends=target['common_friends'], 
                    common_count=target['common_count']))

    # If items contains friends of only one target
    if target_uid != None:
        return items[0]['common_friends']

    # Return items list
    return items
