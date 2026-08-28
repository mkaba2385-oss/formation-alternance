import asyncio

import pytest
from httpx import ASGITransport, AsyncClient

from main import app


@pytest.mark.asyncio
async def test_concurrent_requests_have_different_request_ids():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        response_1, response_2 = await asyncio.gather(
            client.get("/test"),
            client.get("/test"),
        )

    request_id_1 = response_1.headers["X-Request-ID"]
    request_id_2 = response_2.headers["X-Request-ID"]

    assert request_id_1 != request_id_2