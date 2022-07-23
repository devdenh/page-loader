import os


def read(file_path):
    with open(file_path, 'r') as f:
        result = f.read()
    return result


def read_pic(file_path):
    with open(get_fixture_path(file_path), "rb") as image:
        pic = image.read()
    return pic


def get_fixture_path(file_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, file_name)
