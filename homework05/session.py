import requests
from asyncio.tasks import sleep

class Session(requests.Session):
    """
    Сессия.

    :param base_url: Базовый адрес, на который будут выполняться запросы.
    :param timeout: Максимальное время ожидания ответа от сервера.
    :param max_retries: Максимальное число повторных запросов.
    :param backoff_factor: Коэффициент экспоненциального нарастания задержки.
    """

    def __init__(
        self,
        base_url: str,
        timeout: float = 5.0,
        max_retries: int = 3,
        backoff_factor: float = 0.3,
    ) -> None:
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor

    def get(self, url, **kwargs: tp.Any) -> requests.Response:
        delay = self.timeout

        while True:
            try:
                response = requests.get(self.base_url + url)
                break
            except requests.exceptions.RequestException:
                sleep(delay)
                delay = min(self.backoff_factor * delay, self.max_retries)

        return response

    def post(self, url, data=None, json=None, **kwargs: tp.Any) -> requests.Response:
        delay = self.timeout

        while True:
            try:
                response = requests.post(self.base_url + url, data = data, json = json)
                break
            except requests.exceptions.RequestException:
                sleep(delay)
                delay = min(self.backoff_factor * delay, self.max_retries)

        return response