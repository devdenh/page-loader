import stat

from page_loader import download
import os
import requests
from page_loader.DOM_editors import make_dom
from tests.fixtures.expected import read_pic
import pook
from page_loader.downloader import read
import pytest


URL = 'https://ru.hexlet.io/courses'


@pook.on
def test_get_request():
    pook.get(
        URL,
        reply=200,
    )
    response = requests.get(URL)
    assert response.status_code == 200


@pook.on
def test_redirect(tmpdir):
    pook.get(
        URL,
        reply=300
    )
    warning_msg = "Need further action to complete the request"
    with pytest.raises(Exception) as excinfo:
        download(URL, tmpdir)
    assert warning_msg in str(excinfo.value)


@pook.on
def test_client_error(tmpdir):
    pook.get(
        URL,
        reply=400
    )
    critical_msg = "the request contains bad syntax or cannot be fulfilled"
    with pytest.raises(Exception) as excinfo:
        download(URL, tmpdir)
    assert critical_msg in str(excinfo.value)


@pook.on
def test_server_error(tmpdir):
    pook.get(
        URL,
        reply=500
    )
    critical_msg = "the server failed to fulfil an apparently valid request"
    with pytest.raises(Exception) as excinfo:
        download(URL, tmpdir)
    assert critical_msg in str(excinfo.value)


def test_create_file(tmpdir, mock_html):
    file = download('https://ru.hexlet.io/courses', tmpdir)
    assert os.path.exists(file)


def test_download_pic(tmpdir, mock_html):
    download(URL, tmpdir)
    files_dir = os.path.join(tmpdir, 'ru-hexlet-io-courses_files')
    pic_path = os.path.join(files_dir,
                            'ru-hexlet-io-assets-professions-nodejs.png')
    pic_content = read_pic(pic_path)
    assert os.path.isdir(files_dir)
    assert os.path.exists(pic_path)
    assert type(pic_content) == bytes


def test_change_links(tmpdir, fake_jpg, mock_html, fake_downloaded_html):
    downloaded = download(URL, tmpdir)
    dom = make_dom(read(downloaded))
    new_dom = make_dom(fake_downloaded_html)
    assert dom.prettify() == new_dom.prettify()


def test_permission_exception(tmpdir, mock_html):
    os.chmod(tmpdir, stat.S_IRUSR)
    with pytest.raises(PermissionError):
        download(URL, tmpdir)


def test_nonexistent_dir(tmpdir, mock_html):
    with pytest.raises(FileExistsError):
        download(URL, "Fake_dir")
