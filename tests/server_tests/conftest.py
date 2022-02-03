import pytest
from server import app


@pytest.fixture
def client():
    app.testing = True
    yield app.test_client()
