import pytest
from fastapi.testclient import TestClient

from iris.service.app import app


def make_good_row():
    return {
        "sepal_length": 5.5,
        "sepal_width": 2.4,
        "petal_length": 3.7,
        "petal_width": 1
    }


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture()
def good_row():
    return make_good_row()