import os
import requests
from page_loader.parser import parse
from page_loader.DOM import make_dom
from page_loader.DOM import replace_pic_link
from urllib.parse import urljoin
from tests.fixtures.expected import read


# def get_extention(url):
#     parsed = parse(url, 'url')
#     return os.path.splitext(parsed.path)[-1]


def build_name(url, ending):
    parsed_url = parse(url, 'url')
    target_name = parsed_url.netloc + parsed_url.path
    url_no_extention = os.path.splitext(target_name)[0]
    file_name = ''
    for item in url_no_extention:
        if item.isalpha() or item.isnumeric():
            file_name += item
        else:
            file_name += '-'
    return file_name + f'{ending}'


def write(fp, data):
    with open(fp, 'w') as f:
        f.write(data)


def download(url, output=os.getcwd()):
    if not os.path.exists(output) or not os.path.isdir(output):
        raise NotADirectoryError("Directory not exist")
    target_html_name = build_name(url, '.html')
    target_path = os.path.join(output, target_html_name)
    get = requests.get(url)
    files_dir = build_name(url, '_files')

    if not os.path.exists(target_path):
        write(target_path, get.text)

    dom = make_dom(read(target_path))
    pic_list = dom.findAll('img')

    if pic_list:
        target_dir = os.path.join(output, files_dir)
        if not os.path.exists(target_dir):
            os.mkdir(target_dir)
        src_list = list(map(lambda x: x['src'], pic_list))
        for src in src_list:
            picture_name = download_pictures(urljoin(url, src), target_dir)
            new_link = os.path.join(files_dir, picture_name)
            replace_pic_link(dom, src, new_link)
        write(target_path, dom.prettify())
    if output:
        return target_path


def download_pictures(url, dir):
    pic_name = build_name(url, os.path.splitext(url)[-1])
    img_data = requests.get(url).content
    file_name = os.path.join(dir, pic_name)
    with open(file_name, 'wb') as handler:
        handler.write(img_data)
    return pic_name
