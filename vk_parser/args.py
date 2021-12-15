"""Creating parser."""
import argparse


def initialize_parser():
    """Initialize parser for CLI."""
    parser = argparse.ArgumentParser(
        usage='vk_parser [command] [parameters]',
    )
    subparsers = parser.add_subparsers(
        dest='command',
        title='Commands',
        metavar='<command>',
    )

    fetch = subparsers.add_parser('fetch', help='Fetch friends')
    fetch.add_argument('id', type=int, help='user id')
    fetch.add_argument('-d', '--depth', type=int, default=2, help='max depth')
    fetch.add_argument('--ignore-cache', action='store_true')

    dist = subparsers.add_parser('dist', help='Find minimal distance')
    dist.add_argument('id1', type=int, help='user_from id')
    dist.add_argument('id2', type=int, help='user_to id')
    dist.add_argument('-d', '--depth', type=int, default=2, help='path limit')
    dist.add_argument('--ignore-cache', action='store_true')

    return parser
