import logging
import sys
from page_loader.my_logging import file_handler
from page_loader.cli import parse_args
from page_loader import download
from page_loader.request_handler import (
    RedirectError, ClientError, ServerError
)


def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.addHandler(file_handler)
    exit_code = 0
    args = parse_args()
    try:
        download(args.url, args.output)
    except Exception as ex:
        exit_code = 1
        if isinstance(ex, ValueError):
            logger.critical(f"{ex.args[0]}")
        if isinstance(ex, FileExistsError):
            logger.critical(f"{ex.args[0]}")
        if isinstance(ex, PermissionError):
            logger.critical(f"{ex.args[0]}")
        if isinstance(ex, RedirectError):
            logger.warning(f"{RedirectError.args[0]}"
                           f" url: {RedirectError.args[1]}")
        if isinstance(ex, ClientError):
            logger.critical(f"{ClientError.args[0]}"
                            f" url: {ClientError.args[1]}")
        if isinstance(ex, ServerError):
            logger.critical(f"{ServerError.args[0]}"
                            f" url: {ServerError.args[1]}")
    finally:
        sys.exit(exit_code)


if __name__ == '__main__':
    main()
