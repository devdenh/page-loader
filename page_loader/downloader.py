from page_loader.url import dashify_file_name, dashify_files_dir
from page_loader.response import raise_for_status
from page_loader.resources import collect_resources
from progress.bar import IncrementalBar
import validators
import requests
import logging
import time
import os


logger = logging.getLogger("root")


def download(url, output=os.getcwd()):
    files_dir_name = dashify_files_dir(url)
    files_dir_path = os.path.join(output, files_dir_name)

    #  we need existed dirs
    if not os.path.exists(output) or not os.path.isdir(output):
        os.mkdir(output)
        logger.info(f"creating output directory: {output}")

    if not validators.url(url):
        raise ValueError(f"Invalid url: {url}")

    if not os.access(output, os.W_OK):
        raise PermissionError(f"Need permission to write in: {output}")

    session = requests.Session()
    response = session.get(url)

    raise_for_status(response.status_code, url)

    logger.info(f"requested url: {url}")
    logger.info(f"output path: {output}")
    downloaded_html_name = dashify_file_name(url)
    html_path = os.path.join(output, downloaded_html_name)

    resource_list, downloaded_html = collect_resources(
        response.text,
        url,
        files_dir_name
    )

    with open(html_path, 'w') as html:
        html.write(downloaded_html)
    logger.info(f"Creating html webpage{html_path}")

    if resource_list:
        if not os.path.exists(files_dir_path):
            os.mkdir(files_dir_path)
        with IncrementalBar("Downloading:", max=len(resource_list)) as bar:
            for resource_url, path_to_save in resource_list:
                local_path_to_save = os.path.join(output, path_to_save)
                download_resources(resource_url, local_path_to_save)
                bar.next()
                time.sleep(0.1)
    else:
        logger.info("No possible resources to download")
    logger.info(f"Page was downloaded as: '{html_path}'")

    return html_path


def download_resources(url, path):
    content = requests.get(url).content
    with open(path, 'wb') as f:
        f.write(content)
