import pytest
from tests.fixtures.expected import get_fixture_path
import requests_mock


@pytest.fixture(scope='module')
def html_fixture():
    with open(get_fixture_path('hexlet.html'), 'r') as f:
        result = f.read()
    return result


@pytest.fixture(scope='module')
def image_fixture():
    with open(get_fixture_path('picture.jpg'), "rb") as image:
        pic = image.read()
    return pic


@pytest.fixture(scope='module')
def mock_fixture(html_fixture, image_fixture):
    with requests_mock.Mocker() as m:
        m.get('https://ru.hexlet.io/courses', text=html_fixture)
        m.get('/assets/professions/nodejs.png', content=image_fixture)
        yield m
