import os
from page_loader.parser import parse


def build_dashed_name(url, ending):
    _, parsed_url = parse(url, 'url')
    target_name = parsed_url.netloc + parsed_url.path
    url_no_extention = os.path.splitext(target_name)[0]
    file_name = ''
    for item in url_no_extention:
        if item.isalpha() or item.isnumeric():
            file_name += item
        else:
            file_name += '-'
    return file_name + f'{ending}'


def get_extension(name, tag):
    if tag.get('rel') == ['canonical']:
        return '.html'
    return os.path.splitext(name)[-1]
