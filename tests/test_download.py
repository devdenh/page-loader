import pook
import requests
import pytest
import os
from page_loader import download


@pook.on
def test_get_request():
    url = 'https://ru.hexlet.io/courses'
    pook.get(
        url,
        reply=200,
    )
    response = requests.get(url)
    assert response.status_code == 200


@pytest.fixture
def fake_dir(tmpdir_factory):
    base_dir = tmpdir_factory.mktemp('base')
    os.mkdir(os.path.join(base_dir, 'inner_dir'))
    return base_dir


def test_create_file(fake_dir):
    file = download('https://ru.hexlet.io/courses', fake_dir)
    assert os.path.exists(file)
