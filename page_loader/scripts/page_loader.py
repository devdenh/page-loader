import logging
import sys
from page_loader.cli import parse_args
from page_loader import download
from page_loader.request_handler import RedirectError, ClientError, ServerError


def main():
    exit_code = 0
    args = parse_args()
    logging.basicConfig(level=logging.INFO)
    logging.root.addHandler(logging.FileHandler("logs.log"))
    try:
        download(args.url, args.output)
    except Exception as ex:
        exit_code = 1
        if isinstance(ex, ValueError):
            logging.critical(f"{ex.args[0]}")
        if isinstance(ex, FileExistsError):
            logging.critical(f"{ex.args[0]}")
        if isinstance(ex, PermissionError):
            logging.critical(f"{ex.args[0]}")
        if isinstance(ex, RedirectError):
            logging.warning(f"{RedirectError.args[0]}"
                            f" url: {RedirectError.args[1]}")
        if isinstance(ex, ClientError):
            logging.critical(f"{ClientError.args[0]}"
                             f" url: {ClientError.args[1]}")
        if isinstance(ex, ServerError):
            logging.critical(f"{ServerError.args[0]}"
                             f" url: {ServerError.args[1]}")
    finally:
        sys.exit(exit_code)


if __name__ == '__main__':
    main()
