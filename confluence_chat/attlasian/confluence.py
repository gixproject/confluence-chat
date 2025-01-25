from http import HTTPMethod
from typing import Any

import httpx

from confluence_chat.attlasian.enums import ConfluenceItemStatus
from confluence_chat.attlasian.schemas import ConfluenceWorkSpaceSchema, ConfluencePageSchema
from confluence_chat.conf.settings import settings


class ConfluenceAPI:
    API_V1_PATH = "/wiki/rest/api"
    API_V2_PATH = "/wiki/api/v2"
    DEFAULT_LIMIT = 250

    def __init__(self, host: str, email: str, token: str):
        self.host = host
        self.email = email

        self.auth = httpx.BasicAuth(username=email, password=token)
        self.http_client = httpx.AsyncClient(auth=self.auth, base_url=host, timeout=5)

    async def _call(
        self,
        method: HTTPMethod,
        path: str,
        data: dict[str, Any] | list[Any] | None = None,
    ) -> Any:
        response = await self.http_client.request(
            method=method,
            url=path,
            auth=self.auth,
            json=data if method != HTTPMethod.GET else None,
            params=data if method == HTTPMethod.GET else None,
        )

        response.raise_for_status()

        result = None
        if len(response.content) > 0:
            result = response.json()

        return result

    async def get_spaces(self, keys: list[str] | None = None) -> list[ConfluenceWorkSpaceSchema]:
        data = {
            "limit": self.DEFAULT_LIMIT,
            "status": ConfluenceItemStatus.CURRENT.value,
            "sort": "name",
            "include-icon": True,
        }

        if keys:
            data["keys"] = keys

        response = await self._call(
            method=HTTPMethod.GET,
            path=f"{self.API_V2_PATH}/spaces",
            data=data,
        )

        return [ConfluenceWorkSpaceSchema(**item) for item in response["results"]]

    async def get_pages(self, space_id: int) -> list[ConfluencePageSchema]:
        response = await self._call(
            method=HTTPMethod.GET,
            path=f"{self.API_V2_PATH}/pages",
            data={
                "space-id": space_id,
                "limit": 10,
                "status": ConfluenceItemStatus.CURRENT.value,
                "sort": "-modified-date",
                "body-format": "storage",
            },
        )

        return [ConfluencePageSchema(**item) for item in response["results"]]

    async def get_user(self, account_id: str):
        response = await self._call(
            method=HTTPMethod.GET,
            path=f"{self.API_V1_PATH}/user/",
            data={"accountId": account_id},
        )

        return response


confluence_client = ConfluenceAPI(
    host=str(settings.confluence.host),
    email=settings.confluence.email,
    token=settings.confluence.token,
)
