from urllib.parse import urlparse
import tldextract


def parse(data, format_name):
    subdomain = tldextract.extract(data).subdomain
    if format_name == 'url':
        return subdomain, urlparse(data)
    raise ValueError(f'Unknown format: {format_name}')


def is_subdomain(first_url, second_url):
    if get_subdomain(first_url) == get_subdomain(second_url):
        if get_domain(first_url) == get_domain(second_url):
            return True
    else:
        return False


def get_subdomain(url):
    return tldextract.extract(url).subdomain


def get_domain(url):
    return tldextract.extract(url).domain
