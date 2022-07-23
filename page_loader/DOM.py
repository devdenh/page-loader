from bs4 import BeautifulSoup


def make_dom(html):
    return BeautifulSoup(html, 'html.parser')


def replace_pic_link(dom, old, new):
    image = dom.select(f'img[src="{old}"]')
    image[0]['src'] = new
