from urllib.parse import urlparse
import os


def dashify(url):
    parsed_url = urlparse(url)
    target_name = parsed_url.netloc + parsed_url.path
    url_no_extension = os.path.splitext(target_name)[0]
    result = ""
    for item in url_no_extension:
        if item.isalpha() or item.isnumeric():
            result += item
        else:
            result += '-'
    return result


def dashify_file_name(url):
    extension = os.path.splitext(url)[-1]
    if not extension:
        extension = ".html"
    result = dashify(url) + extension
    return result


def dashify_files_dir(url):
    result = dashify(url) + '_files'
    return result
