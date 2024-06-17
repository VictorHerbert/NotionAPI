import pytest

def pytest_addoption(parser):
    parser.addoption("--token", action="store")
    parser.addoption("--database_id", action="store")

@pytest.fixture
def token(request):
    token = request.config.option.token
    if token is None:
        raise ValueError('Token must be provided')
    return token