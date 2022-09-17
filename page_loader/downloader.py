from page_loader.fs_handlers import write, read, check_write_permission
from page_loader.request_handler import handle_requests, is_valid_url
from page_loader.name_editors import build_dashed_name
from page_loader.resources import edit_html
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
    downloaded_html_name = build_dashed_name(url, '.html')
    html_path = os.path.join(output, downloaded_html_name)
    logging.info(f"write html file: {html_path}")

    files_dir_name = build_dashed_name(url, '_files')
    files_dir_path = os.path.join(output, files_dir_name)

    #  check if html already exists
    if not os.path.exists(html_path):
        logger.info("Creating html webpage")
        write(html_path, get.text, 'w')

    resource_list, downloaded_html = edit_html(
        read(html_path),
        url,
        files_dir_name
    )

    write(html_path, downloaded_html, 'w')

    if resource_list:
        bar = IncrementalBar("Downloading:", max=len(resource_list))
        if not os.path.exists(files_dir_path):
            os.mkdir(files_dir_path)
        for resource_url, path_to_save in resource_list:
            local_path_to_save = os.path.join(output, path_to_save)
            content = requests.get(resource_url).content
            write(local_path_to_save, content, 'wb')
            bar.next()
            time.sleep(0.1)
        bar.finish()
    else:
        logger.info("No possible resources to download")
    logger.info(f"Page was downloaded as: '{html_path}'")

    return html_path
