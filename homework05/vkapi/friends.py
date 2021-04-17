import typing as tp
import dataclasses

from datetime import datetime
from statistics import median
from math import ceil
from time import sleep

from vkapi.config import VK_CONFIG
from vkapi.session import Session


@dataclasses.dataclass(frozen=True)
class FriendsResponse:
    """
    Ответ на вызов метода `friends.get`.

    :param count: Количество пользователей.
    :param items: Список идентификаторов друзей пользователя или список пользователей.
    """
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
    :return: Объект класса FriendsResponse.
    """
    # Some data for query
    domain = VK_CONFIG["domain"]
    access_token = VK_CONFIG["access_token"]
    v = VK_CONFIG["version"]

    # Query to get user friends
    query = f"friends.get?\
        access_token={access_token}&\
        user_id={user_id}&\
        fields={'' if (fields == None) else ','.join(fields)}&\
        count={count}&\
        offset={offset}&\
        v={v}".replace(" ", "")

    # New session
    session = Session(base_url=domain)

    # Get response
    response = session.get(query)

    # Check response status
    if (response.status_code != 200):
        return FriendsResponse(count=0, items=[])

    # Get friends data from response
    items = response.json()['response']['items']

    # Return friends data
    return FriendsResponse(count=len(items), items=items)


def age_predict(user_id: int) -> tp.Optional[float]:
    """
    Наивный прогноз возраста пользователя по возрасту его друзей.

    Возраст считается как медиана среди возраста всех друзей пользователя.

    :param user_id: Идентификатор пользователя.
    :return: Медианный возраст пользователя.
    """
    # List of friends' ages
    ages = []

    # Get friends data with birthday field
    friends = get_friends(user_id=user_id, fields=['bdate'])

    # For each friend in list
    for friend in friends.items:
        # Try to get birthday date from friend data
        try:
            date = datetime.strptime(friend['bdate'], '%d.%m.%Y')
            ages.append(date.year)
        except:
            pass
    
    # Return median age
    return median(ages)

##############################################################################
##############################################################################

class MutualFriends(tp.TypedDict):
    id: int
    common_friends: tp.List[int]
    common_count: int


# This function faild if target has private profile
def get_mutual(
    source_uid: tp.Optional[int] = None,
    target_uid: tp.Optional[int] = None,
    target_uids: tp.Optional[tp.List[int]] = None,
    order: str = "",
    count: tp.Optional[int] = None,
    offset: int = 0,
    progress=lambda x : x,
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

    # Process each handred of friends with process handler
    for i in progress(range(ceil(len(targets) / 100))):
        query = f"friends.getMutual?\
            access_token={access_token}&\
            source_uid={'' if (source_uid == None) else source_uid}&\
            target_uids={'' if (targets == None or targets == []) else ','.join(map(str, targets[i*100:(i+1)*100]))}&\
            order={order}&\
            count={'' if (count == None) else count}&\
            offset={offset}&\
            v={v}".replace(" ", "")

        # Wait 1 second between each 3 requests
        if (i % 3 == 0):
            sleep(1)

        # Get response
        response = session.get(query)

        # Check response status
        if (response.status_code != 200):
            continue
                
        # For each target in response 
        for target in response.json()['response']:
            # Append target data to items list
            items.append(MutualFriends(
                    id=target['id'], 
                    common_friends=target['common_friends'], 
                    common_count=target['common_count']))

    # If items contains friends of only one target
    if len(items) == 1:
        return items[0]['common_friends']

    # Return items list
    return items