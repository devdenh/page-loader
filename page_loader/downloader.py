from page_loader.parser import parse, is_subdomain
from page_loader.DOM_editors import make_dom, replace_content_link
from urllib.parse import urljoin
from page_loader.fs_handlers import write, write_content, read, \
    check_write_permission
from page_loader.name_editors import build_dashed_name, get_extension
from page_loader.request_handler import handle_requests, is_valid_url
from progress.bar import IncrementalBar
import requests
import logging
import time
import os


logger = logging.getLogger("root")


def download(url, output=os.getcwd()):
    #  we need existed dirs
    if not os.path.exists(output) or not os.path.isdir(output):
        raise FileExistsError("Directory not exists")
    is_valid_url(url)
    session = requests.Session()
    get = session.get(url)

    handle_requests(get.status_code, url)
    check_write_permission(output)

    logger.info(f"requested url: {url}")
    logger.info(f"output path: {output}")
    target_html_name = build_dashed_name(url, '.html')
    target_path = os.path.join(output, target_html_name)
    logging.info(f"write html file: {target_path}")

    files_dir = build_dashed_name(url, '_files')

    #  check if html already exists
    if not os.path.exists(target_path):
        logger.info("Creating html webpage")
        write(target_path, get.text)

    dom = make_dom(read(target_path))
    possible_resources = ['img', 'link', 'script']
    res_list = dom.findAll(possible_resources)

    if res_list:
        selected_dir = os.path.join(output, files_dir)
        new_dom = download_resources(res_list, selected_dir,
                                     files_dir, url, dom)
        write(target_path, new_dom.prettify())
    else:
        logger.info("No possible resources to download")
    logger.info(f"Page was downloaded as: '{target_path}'")

    return target_path


def download_resources(res_list, target_dir, files_dir, url, dom):
    parsed_url = parse(url, 'url')
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)

    bar = IncrementalBar("Downloading:", max=len(res_list))

    for item in res_list:
        bar.next()
        time.sleep(0.1)
        #  "/assets/application.css"
        #  or "https://ru.hexlet.io/packs/js/runtime.js"

        resource_link = item.get('src') \
            if item.get('src') else item.get('href')
        if resource_link:
            #  'https://ru.hexlet.io/courses/assets/application.css'
            abs_res_link = resource_link \
                if parsed_url.netloc in resource_link \
                else urljoin(url, resource_link)
            if is_subdomain(url, abs_res_link) and \
                    len(os.listdir(target_dir)) < len(res_list):
                #  "https://ru.hexlet.io/packs/js/runtime.js"
                #  or 'ru.hexlet.io/assets/application.css'
                local_src_name = resource_link \
                    if parsed_url.netloc in resource_link \
                    else parsed_url.netloc + resource_link
                #  'ru-hexlet-io-packs-js-runtime.js'
                #  or 'ru-hexlet-io-assets-application.css'
                dashed_name = build_dashed_name(local_src_name,
                                                get_extension(
                                                    local_src_name,
                                                    item))
                write_content(abs_res_link, dashed_name, target_dir)
                replace_content_link(item, os.path.join(files_dir,
                                                        dashed_name))
        else:
            logger.info("No src or href can't download resource")
    bar.finish()
    return dom
