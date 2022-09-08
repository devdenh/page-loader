import validators


class RedirectError(Exception):
    def __init__(self, text, url):
        self.txt = text
        self.url = url


class ClientError(Exception):
    def __init__(self, text, url):
        self.txt = text
        self.url = url


class ServerError(Exception):
    def __init__(self, text, url):
        self.txt = text
        self.url = url


def is_valid_url(url):
    if not validators.url(url):
        raise ValueError(f"Invalid url: {url}")


def handle_requests(status_code, url):
    if 300 <= status_code < 400:
        raise RedirectError(
            "Need further action to complete the request",
            url
        )
    if 400 <= status_code < 500:
        raise ClientError(
            "the request contains bad syntax or cannot be fulfilled",
            url
        )
    if 500 <= status_code < 600:
        raise ServerError(
            "the server failed to fulfil an apparently valid request",
            url
        )
