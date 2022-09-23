import os.path

from page_loader.url import dashify_file_name
from urllib.parse import urlparse
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger("root")


def collect_resources(html, url, files_dir_name):
    parsed_url = urlparse(url)
    dom = BeautifulSoup(html, 'html.parser')
    target_tags = ['img', 'link', 'script']
    tags_resources = {
        'img': 'src',
        'link': 'href',
        'script': 'src'
    }
    tags = dom.findAll(target_tags)
    resource_list = []
    for resource in tags:
        #  "/assets/application.css"
        #  or "https://ru.hexlet.io/packs/js/runtime.js"

        resource_url = resource.get(tags_resources.get(resource.name))
        if not resource_url:
            continue

        #  'https://ru.hexlet.io/courses/assets/application.css'
        #  or "/blog/about"
        abs_resource_url = urljoin(url + '/', resource_url)

        if urlparse(abs_resource_url).netloc != parsed_url.netloc:
            continue

        path_to_save = os.path.join(
            files_dir_name,
            dashify_file_name(abs_resource_url)
        )
        resource_list.append((abs_resource_url, path_to_save))
        resource[tags_resources.get(resource.name)] = path_to_save
    return resource_list, dom.prettify()
