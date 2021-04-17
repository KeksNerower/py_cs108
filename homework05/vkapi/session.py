import requests
import typing as tp
from time import sleep

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
        self.base_url = base_url + '/'
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor

    def get(self, url, **kwargs: tp.Any) -> requests.Response:
        delay = self.timeout

        for i in range(self.max_retries):
            try:
                response = requests.get(self.base_url + url)
                return response
            except requests.exceptions.RequestException:
                sleep(delay)
                print(delay)
                delay = self.backoff_factor * delay

        return None        

    def post(self, url, data=None, json=None, **kwargs: tp.Any) -> requests.Response:
        delay = self.timeout

        for i in range(self.max_retries):
            try:
                response = requests.post(self.base_url + url, data = data, json = json)
                return response
            except requests.exceptions.RequestException:
                sleep(delay)
                delay = self.backoff_factor * delay

        return None