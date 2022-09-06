from page_loader import download
import os
import requests
from page_loader.DOM_editors import make_dom
from tests.fixtures.expected import read_pic
import pook
from page_loader.downloader import read


@pook.on
def test_get_request():
    url = 'https://ru.hexlet.io/courses'
    pook.get(
        url,
        reply=200,
    )
    response = requests.get(url)
    assert response.status_code == 200


def test_create_file(tmpdir, mock_html):
    file = download('https://ru.hexlet.io/courses', tmpdir)
    assert os.path.exists(file)


def test_download_pic(tmpdir, mock_html):
    url = 'https://ru.hexlet.io/courses'
    download(url, tmpdir)
    files_dir = os.path.join(tmpdir, 'ru-hexlet-io-courses_files')
    pic_path = os.path.join(files_dir,
                            'ru-hexlet-io-assets-professions-nodejs.png')
    pic_content = read_pic(pic_path)
    assert os.path.isdir(files_dir)
    assert os.path.exists(pic_path)
    assert type(pic_content) == bytes


def test_change_links(tmpdir, fake_jpg, mock_html, fake_downloaded_html):
    url = 'https://ru.hexlet.io/courses'
    downloaded = download(url, tmpdir)
    dom = make_dom(read(downloaded))
    new_dom = make_dom(fake_downloaded_html)
    assert dom.prettify() == new_dom.prettify()
