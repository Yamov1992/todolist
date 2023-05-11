from django.conf import settings
from bot.tg.schemas import GetUpdatesResponse, SendMessageResponse
from pydantic import ValidationError

import requests


class TgClient:
    def __init__(self, token: str = settings.BOT_TOKEN):
        self.token = token

    def get_url(self, method: str) -> str:
        return f"https://api.telegram.org/bot{self.token}/{method}"

    def get_updates(self, offset: int = 0, timeout: int = 60) -> GetUpdatesResponse:
        data = self._get(method='getUpdates', offset=offset, timeout=timeout)
        try:
            return GetUpdatesResponse(**data)
        except ValidationError as e:
            print(e)
            print(data)
            return GetUpdatesResponse(ok=False, result=[])

    def send_message(self, chat_id: int, text: str) -> SendMessageResponse:
        data = self._get(method='sendMessage', chat_id=chat_id, text=text)
        return SendMessageResponse(**data)

    def _get(self, method: str, **params) -> dict:
        url: str = self.get_url(method)
        response = requests.get(url, params=params)
        if not response.ok:
            print(f'Status code: {response.status_code}\nBody: {response.content}')
            raise RuntimeError
        return response.json()