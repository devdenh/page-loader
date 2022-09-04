import os
import requests
from page_loader.parser import parse
from page_loader.DOM import make_dom
from page_loader.DOM import replace_content_link
from urllib.parse import urljoin


def read(file_path):
    with open(file_path, 'r') as f:
        result = f.read()
    return result


def build_dashed_name(url, ending):
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
        #  we need only exists dirs
    target_html_name = build_dashed_name(url, '.html')
    target_path = os.path.join(output, target_html_name)
    session = requests.Session()
    session.get(url)
    get = session.get(url)
    files_dir = build_dashed_name(url, '_files')

    if not os.path.exists(target_path):
        write(target_path, get.text)
        #  check if html already exists

    dom = make_dom(read(target_path))
    possible_resourses = ['img', 'link', 'script']
    res_list = dom.findAll(possible_resourses)

    if res_list:
        target_dir = os.path.join(output, files_dir)
        new_dom = download_resources(res_list, target_dir,
                                     files_dir, url, dom)
        write(target_path, new_dom.prettify())
    if output:
        return target_path


def download_resources(res_list, target_dir, files_dir, url, dom):
    parsed_url = parse(url, 'url')
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)

    for item in res_list:
        #  "/assets/application.css"
        #  or "https://ru.hexlet.io/packs/js/runtime.js"

        resource_link = item.get('src') \
            if item.get('src') else item.get('href')
        if not resource_link:
            raise ValueError('No src or href')
        #  'https://ru.hexlet.io/courses/assets/application.css'
        abs_res_link = resource_link \
            if parsed_url.netloc in resource_link\
            else urljoin(url, resource_link)
        if parsed_url.netloc in abs_res_link and \
                len(os.listdir(target_dir)) < len(res_list):
            #  "https://ru.hexlet.io/packs/js/runtime.js"
            #  or 'ru.hexlet.io/assets/application.css'
            local_src_name = resource_link\
                if parsed_url.netloc in resource_link\
                else parsed_url.netloc + resource_link
            #  'ru-hexlet-io-packs-js-runtime.js'
            #  or 'ru-hexlet-io-assets-application.css'
            dashed_name = build_dashed_name(local_src_name,
                                            get_extension(
                                                local_src_name,
                                                item))
            write_content(abs_res_link, dashed_name, target_dir)
            replace_content_link(item, os.path.join(files_dir, dashed_name))
    return dom


def write_content(link, target_name, files_dir):
    content_data = requests.get(link).content
    file_name = os.path.join(files_dir, target_name)
    with open(file_name, 'wb') as handler:
        handler.write(content_data)


def get_extension(name, tag):
    if tag.get('rel') == ['canonical']:
        return '.html'
    return os.path.splitext(name)[-1]
