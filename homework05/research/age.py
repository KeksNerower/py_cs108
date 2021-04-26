import typing as tp
from datetime import datetime as dt
from statistics import median

from vkapi.friends import get_friends


def age_predict(user_id: int) -> tp.Optional[float]:
    """
    Наивный прогноз возраста пользователя по возрасту его друзей.

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: Идентификатор пользователя.
    :return: Медианный возраст пользователя.
    """
    # List of friends' ages
    ages = []

    # Get friends data with birthday field
    friends = get_friends(user_id=user_id, fields=["bdate"])

    # For each friend in list
    for friend in friends.items:
        # Try to get birthday date from friend data
        try:
            date = dt.strptime(friend["bdate"], "%d.%m.%Y")  # type: ignore
            ages.append(date.year)
        except:
            pass

    if not ages:
        return None

    # Return median age
    return dt.today().year - median(ages)
