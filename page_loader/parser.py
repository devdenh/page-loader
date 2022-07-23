from urllib.parse import urlparse
# from bs4 import BeautifulSoup


def parse(data, format_name):
    if format_name == 'url':
        return urlparse(data)
    raise ValueError(f'Unknown format: {format_name}')
