from urllib.parse import urlparse
import tldextract


def parse(data, format_name):
    if format_name == 'url':
        return urlparse(data)
    raise ValueError(f'Unknown format: {format_name}')


def is_subdomain(first_url, second_url):
    tld_first = tldextract.TLDExtract(suffix_list_urls=())
    tld_second = tldextract.TLDExtract(suffix_list_urls=())

    if tld_first(first_url).subdomain == tld_second(second_url).subdomain:
        if tld_first(first_url).domain == tld_second(second_url).domain:
            return True
    return False
