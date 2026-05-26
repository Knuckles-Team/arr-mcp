import pytest
from unittest.mock import patch, MagicMock
import os


class DictListMock:
    """A highly flexible mock helper that satisfies both dict and list protocols.
    It returns itself when indexed with integers or queried for properties, preventing MRO conflicts.
    """

    def __init__(self):
        self.data = {
            "id": 1,
            "title": "test",
            "tvdbId": 123,
            "tmdbId": 123,
            "year": 2020,
            "titleSlug": "test",
            "images": [{"url": "http://test"}],
            "results": [{"id": 1}],
        }

    def __getitem__(self, key):
        if isinstance(key, int):
            return self
        return self.data[key]

    def get(self, key, default=None):
        return self.data.get(key, default)

    def __len__(self):
        return 1

    def __bool__(self):
        return True

    def __iter__(self):
        return iter([self])

    def keys(self):
        return self.data.keys()

    def values(self):
        return self.data.values()

    def items(self):
        return self.data.items()


@pytest.fixture
def mock_session():
    """Fixture to patch requests.Session for REST client isolation."""
    with patch("requests.Session") as mock_s:
        session = mock_s.return_value
        response = MagicMock()
        response.status_code = 200
        response.json.return_value = DictListMock()
        response.text = '{"id": 1}'
        session.get.return_value = response
        session.post.return_value = response
        session.put.return_value = response
        session.delete.return_value = response
        session.patch.return_value = response
        session.request.return_value = response
        yield session


@pytest.fixture
def mock_env():
    """Fixture to manage OS environment manipulation during tests."""
    original_env = os.environ.copy()
    yield os.environ
    os.environ.clear()
    os.environ.update(original_env)
