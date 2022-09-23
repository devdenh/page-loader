import stat
from page_loader import download
import os
import requests
from bs4 import BeautifulSoup
import pook
import pytest


URL = "https://site.com/blog/about"
FIXTURES_FOLDER = 'fixtures'


def read(file_path):
    with open(file_path, 'r') as f:
        result = f.read()
    return result


def read_pic(file_path):
    with open(get_fixture_path(file_path), "rb") as image:
        pic = image.read()
    return pic


def get_fixture_path(file_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, FIXTURES_FOLDER, file_name)


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
    file = download('https://site.com/blog/about', tmpdir)
    assert os.path.exists(file)


def test_download_pic(tmpdir, mock_html):
    download(URL, tmpdir)
    files_dir = os.path.join(tmpdir, "site-com-blog-about_files")
    pic_path = os.path.join(
        files_dir,
        "site-com-photos-me.jpg"
    )
    pic_content = read_pic(pic_path)
    assert os.path.isdir(files_dir)
    assert os.path.exists(pic_path)
    assert type(pic_content) == bytes


def test_change_links(tmpdir, fake_jpg, mock_html, fake_downloaded_html):
    downloaded = download(URL, tmpdir)
    dom = BeautifulSoup(read(downloaded), features="html.parser")
    new_dom = BeautifulSoup(fake_downloaded_html, features="html.parser")
    assert dom.prettify() == new_dom.prettify()


def test_permission_exception(tmpdir, mock_html):
    os.chmod(tmpdir, stat.S_IRUSR)
    ex_msg = "Need permission to write in:"
    with pytest.raises(PermissionError) as ex:
        download(URL, tmpdir)
    assert ex_msg in str(ex.value)


# def test_nonexistent_dir(mock_html):
#     with pytest.raises(FileExistsError):
#         download(URL, "Fake_dir")
