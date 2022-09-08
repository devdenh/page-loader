import os
import requests


def read(file_path):
    with open(file_path, 'r') as f:
        result = f.read()
    return result


def write(fp, data):
    with open(fp, 'w') as f:
        f.write(data)


def write_content(link, target_name, files_dir):
    content_data = requests.get(link).content
    file_name = os.path.join(files_dir, target_name)
    with open(file_name, 'wb') as handler:
        handler.write(content_data)


def check_write_permission(path):
    if not os.access(path, os.W_OK):
        raise PermissionError(f"Need permission to write in: {path}")
