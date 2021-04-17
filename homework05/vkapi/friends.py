import typing as tp
import dataclasses
from datetime import datetime
from statistics import median
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
    domain = VK_CONFIG["domain"]
    access_token = VK_CONFIG["access_token"]
    v = VK_CONFIG["version"]

    query = f"friends.get?access_token={access_token}&user_id={user_id}&fields={'' if (fields == None) else ''.join(fields)}&v={v}"

    session = Session(base_url=domain)
    response = session.get(query)

    if (response.status_code != 200):
        return FriendsResponse(count=0, items=[])

    amount = response.json()['response']['count']
    items = response.json()['response']['items']

    items = [items[i] for i in range(0, max(amount, count * offset), 1+offset)]

    return FriendsResponse(count=len(items), items=items)


def age_predict(user_id: int) -> tp.Optional[float]:
    """
    Наивный прогноз возраста пользователя по возрасту его друзей.

    Возраст считается как медиана среди возраста всех друзей пользователя.

    :param user_id: Идентификатор пользователя.
    :return: Медианный возраст пользователя.
    """
    ages = []
    friends = get_friends(user_id=user_id, fields=['bdate'])
    for friend in friends.items:
        try:
            date = datetime.strptime(friend['bdate'], '%d.%m.%Y')
            ages.append(date.year)
        except:
            pass
    
    return median(ages)
