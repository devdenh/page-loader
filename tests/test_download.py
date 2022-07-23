from page_loader import download
import os
import requests
from page_loader.DOM import make_dom
import requests_mock
from tests.fixtures.expected import read_pic
from page_loader.downloader import build_name
import pook
from tests.fixtures.expected import read


@pook.on
def test_get_request():
    url = 'https://ru.hexlet.io/courses'
    pook.get(
        url,
        reply=200,
    )
    response = requests.get(url)
    assert response.status_code == 200


def test_create_file(tmpdir, html_fixture, image_fixture):
    with requests_mock.Mocker() as m:
        m.get('https://ru.hexlet.io/courses', text=html_fixture)
        m.get('/assets/professions/nodejs.png', content=image_fixture)
        file = download('https://ru.hexlet.io/courses', tmpdir)
        assert os.path.exists(file)


def test_download_pic(tmpdir, image_fixture, html_fixture, mock_fixture):
    url = 'https://ru.hexlet.io/courses'
    download(url, tmpdir)
    files_dir = os.path.join(tmpdir, 'ru-hexlet-io-courses_files')
    pic_path = os.path.join(files_dir,
                            'ru-hexlet-io-assets-professions-nodejs.png')
    assert os.path.isdir(files_dir)
    assert os.path.exists(pic_path)
    pic_content = read_pic(pic_path)
    assert type(pic_content) == bytes


def test_change_pic_link(tmpdir, html_fixture, image_fixture, mock_fixture):
    url = 'https://ru.hexlet.io/courses'
    downloaded = download(url, tmpdir)
    target_dir = 'ru-hexlet-io-courses_files'
    target_file = 'ru-hexlet-io-assets-professions-nodejs.png'
    target_name = os.path.join(target_dir, target_file)
    dom = make_dom(read(os.path.join(downloaded)))
    pic = dom.findAll('img')
    assert pic[0]['src'] == target_name
    assert os.path.exists(os.path.join(tmpdir, target_name))
