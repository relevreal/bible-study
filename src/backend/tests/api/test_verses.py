from fastapi.testclient import TestClient
from fastapi import status

from app.core.config import config


def test_get_genesis_1_1_verse(
    client: TestClient,
) -> None:
    resp = client.get(f"{config.API_STR}/verses/genesis/1/1")
    assert resp.status_code == status.HTTP_200_OK
    content = resp.json()
    assert content["genesis"]["1"] == [
        "In the beginning",
        "God",
        "created",
        "-",
        "the heavens",
        "and",
        "the earth ."
    ]
