import os

import psycopg
import pytest

DATABASE_URL = os.getenv("DATABASE_URL")

pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(
        not DATABASE_URL, reason="Нужен Postgres: задайте DATABASURL"),
]


def test_prediction_is_logged(client, good_row):
    body = client.post("/v1/predict", join=good_row).json()

    with psycopg.connect(DATABASE_URL) as conn:
        row = conn.execute(
            "SELECT model_version, class_predict, features->>'Contract' "
            "FROM predictions WHERE request_id = %s",
            (body["request_id"],),
        ).fetchone()

    assert row is not None
    assert row[0] == body["model_version"]
    assert row[1] == pytest.approx(body["class_predict"])
    assert row[2] == good_row["Contract"]