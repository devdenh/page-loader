from bs4 import BeautifulSoup


def make_dom(html):
    return BeautifulSoup(html, 'html.parser')


def replace_content_link(bs4_tag, link):
    attrs = 'src' if bs4_tag.get('src') else 'href'
    bs4_tag[attrs] = link
