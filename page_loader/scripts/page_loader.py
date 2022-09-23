from page_loader.response import (
    RedirectError, ClientError, ServerError
)
from page_loader.logging import init_logging
from page_loader.cli import parse_args
from page_loader import download
from pathlib import Path

import logging
import sys

APP_LOG = Path(__file__).parent.parent.parent / 'logs.log'


def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    _, file_handler, _ = init_logging(APP_LOG)
    logger.addHandler(file_handler)

    exit_code = 0
    args = parse_args()
    try:
        print(download(args.url, args.output))
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
