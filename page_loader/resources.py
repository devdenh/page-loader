import os.path

from page_loader.name_editors import build_dashed_name, get_extension
from urllib.parse import urlparse
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import tldextract
import logging


logger = logging.getLogger("root")


def replace_content_link(bs4_tag, link):
    attrs = 'src' if bs4_tag.get('src') else 'href'
    bs4_tag[attrs] = link


def edit_html(html, url, files_dir_name):

    parsed_url = urlparse(url)
    dom = BeautifulSoup(html, 'html.parser')
    possible_resources = ['img', 'link', 'script']
    possible_resource_list = dom.findAll(possible_resources)
    resource_list = []
    for resource in possible_resource_list:
        #  "/assets/application.css"
        #  or "https://ru.hexlet.io/packs/js/runtime.js"

        resource_url = resource.get('src') \
            if resource.get('src') else resource.get('href')
        if resource_url:
            #  'https://ru.hexlet.io/courses/assets/application.css'
            #  or "/blog/about"
            abs_resource_url = resource_url \
                if parsed_url.netloc in resource_url and\
                parsed_url.scheme in resource_url \
                else urljoin(url, resource_url)
            if is_subdomain(url, abs_resource_url):
                path_to_save = os.path.join(files_dir_name, build_dashed_name(
                    abs_resource_url,
                    get_extension(abs_resource_url, resource)
                ))
                resource_list.append((abs_resource_url, path_to_save))
                replace_content_link(resource, path_to_save)
    return resource_list, dom.prettify()


def is_subdomain(first_url, second_url):
    tld_first = tldextract.TLDExtract(suffix_list_urls=())
    tld_second = tldextract.TLDExtract(suffix_list_urls=())

    if tld_first(first_url).subdomain == tld_second(second_url).subdomain:
        return tld_first(first_url).domain == tld_second(second_url).domain
