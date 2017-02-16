import pytest

from examples.random_user import demonstrate, RandomUser


@pytest.fixture
def api():
    return RandomUser()


def test_endpoint_url(api):
    assert api.user.url == 'https://randomuser.me/api/'


def test_get(api):
    user = api.user.get().results[0]
    assert isinstance(user.gender, str)
    assert isinstance(user.name.first, str)


def test_demo():
    demonstrate()
