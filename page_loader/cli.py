import argparse
import os


def parse_args():
    parser = argparse.ArgumentParser(
        description='Download web page_loader',
        usage='[options] <dir path> <url>')
    parser.add_argument('url', help=argparse.SUPPRESS)
    parser.add_argument('-o', '--output',
                        help='target directory (default: cwd)',
                        metavar="",
                        default=os.getcwd())
    return parser.parse_args()
