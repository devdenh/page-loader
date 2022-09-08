import pytest
from tests.fixtures.expected import get_fixture_path
import requests_mock


@pytest.fixture(scope='module')
def fake_html():
    with open(get_fixture_path('final.html'), 'r') as f:
        result = f.read()
    return result


@pytest.fixture(scope='module')
def fake_jpg():
    with open(get_fixture_path('picture.jpg'), "rb") as image:
        pic = image.read()
    return pic


@pytest.fixture(scope='module')
def fake_downloaded_html():
    with open(get_fixture_path('final_expected.html'), 'r') as f:
        result = f.read()
    return result


@pytest.fixture(scope='module')
def mock_html(fake_html, fake_jpg):
    with requests_mock.Mocker() as m:
        m.get('https://site.com/blog/about', text=fake_html)
        m.get('/assets/professions/nodejs.png', content=fake_jpg)
        m.get('/assets/application.css')
        m.get('https://ru.hexlet.io/packs/js/runtime.js')
        m.get('https://site.com/blog/about/assets/styles.css')
        m.get('https://getbootstrap.com/docs/4.5')
        m.get('https://site.com/photos/me.jpg', content=fake_jpg)
        m.get('https://site.com/assets/scripts.js')
        m.get('https://publicsuffix.org/list/public_suffix_list.dat')
        yield m
