import os
import requests
from urllib.parse import urlparse


def build_html_name(url):
    parsed_url = urlparse(url)
    original_path = os.path.splitext(parsed_url.path)[0]
    source = parsed_url.netloc + original_path
    file_name = ''
    for item in source:
        if item.isalpha() or item.isnumeric():
            file_name += item
        else:
            file_name += '-'
    return file_name + '.html'


def write(fp, data):
    with open(fp, 'w') as f:
        f.write(data)


def download(url, output=os.getcwd()):
    if not os.path.exists(output) or not os.path.isdir(output):
        raise NotADirectoryError("Directory not exist")
    target_file_name = build_html_name(url)
    target_path = os.path.join(output, target_file_name)
    get = requests.get(url)
    write(target_path, get.text)
    return target_path

# print(download('https://ru.hexlet.io/courses', '/var/tmp'))
