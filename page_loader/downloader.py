import os
import requests
from page_loader.parser import parse
from page_loader.DOM import make_dom
from page_loader.DOM import replace_pic_link
from urllib.parse import urljoin


def read(file_path):
    with open(file_path, 'r') as f:
        result = f.read()
    return result


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
    parsed_url = parse(url, 'url')

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
            full_pic_name = urljoin(url, src)
            if parsed_url.scheme in full_pic_name and\
                    len(os.listdir(target_dir)) < len(pic_list):
                picture_name = download_pictures(full_pic_name, target_dir)
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
