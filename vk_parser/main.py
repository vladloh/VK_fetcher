"""Script that parse vk friends and friends of frends and ..."""
import argparse
import sys
from queue import Queue

from vk_parser.db_worker import create_db_if_not_exists
from vk_parser.vk_fetcher import get_friends


def initialize_parser():
    """Initialize parser for CLI."""
    parser = argparse.ArgumentParser(
        usage='vk_parser [command] [parameters]',
    )
    parser.set_defaults(func=lambda args: parser.print_help())
    subparsers = parser.add_subparsers(
        dest='command',
        title='Commands',
        metavar='<command>',
    )

    fetch = subparsers.add_parser('fetch', help='Fetch friends')
    fetch.add_argument('user_id', type=int, help='user id')
    fetch.add_argument('-d', '--max_depth', type=int, default=2, help='depth')
    fetch.add_argument('--ignore-cache', action='store_true')
    fetch.set_defaults(func=fetch_user)

    dist = subparsers.add_parser('dist', help='Find minimal distance')
    dist.add_argument('user_id1', type=int, help='user_from id')
    dist.add_argument('user_id2', type=int, help='user_to id')
    dist.add_argument('-d', '--max_depth', type=int, default=2, help='limit')
    dist.add_argument('--ignore-cache', action='store_true')
    dist.set_defaults(func=calculate_dist)

    return parser


def show_progress(user_id, remain):
    """Show progress of bfs."""
    sys.stdout.write(f'\rGetting friends for id={user_id}, remains {remain}. ')
    sys.stdout.flush()


def bfs_from_user(user_id, max_depth, ignore_cache=False, stop_vertices={}):
    """Bfs through social graph of user."""
    queue = Queue()
    queue.put(user_id)
    depth = {}
    depth[user_id] = 0
    parents = {}
    parents[user_id] = None
    while not queue.empty():
        cur_id = queue.get()
        show_progress(cur_id, queue.qsize())
        if depth[cur_id] == max_depth:
            break
            
        neighbours = get_friends(cur_id, ignore_cache=ignore_cache)

        for new_id in neighbours:
            if new_id not in depth:
                depth[new_id] = depth[cur_id] + 1
                parents[new_id] = cur_id
                if depth[new_id] < max_depth:
                    queue.put(new_id)
                if new_id in stop_vertices:
                    queue.queue.clear()
                    break

    sys.stdout.write('\nBfs completed!\n')
    return depth, parents


def fetch_user(args):
    """Fetch friends for user and print its size."""
    social_graph, _ = bfs_from_user(
        user_id=args.user_id,
        max_depth=args.max_depth,
        ignore_cache=args.ignore_cache,
    )
    sys.stdout.write('{0} users by dist <= {1}\n'.format(
        len(social_graph),
        args.max_depth,
    ))


def get_path(vertex, parents):
    """Get path to start from vertex."""
    path = []
    vertex = parents[vertex]

    while vertex is not None:
        path.append(vertex)
        vertex = parents[vertex]

    return path[::-1]


def calculate_dist(args):
    """Calculate dist and path between two users (MITM)."""
    max_depth = args.max_depth
    max_depth1 = max_depth // 2
    max_depth2 = max_depth - max_depth1

    social_graph1, parent1 = bfs_from_user(
        user_id=args.user_id1,
        max_depth=max_depth1,
        ignore_cache=args.ignore_cache,
        stop_vertices={args.user_id2: 0},
    )

    social_graph2, parent2 = bfs_from_user(
        user_id=args.user_id2,
        max_depth=max_depth2,
        ignore_cache=args.ignore_cache,
        stop_vertices=social_graph1,
    )

    dist = 10 ** 18
    best_path = None
    for (connector, dist1) in social_graph1.items():
        if connector in social_graph2:
            new_dist = dist1 + social_graph2.get(connector)
            if dist is None or new_dist < dist:
                dist = new_dist
                path1 = get_path(connector, parent1)
                path2 = get_path(connector, parent2)
                best_path = path1 + [connector] + path2[::-1]

    if best_path:
        sys.stdout.write('Shortest path have {0} edges:\n'.format(dist))
        sys.stdout.write('{0}\n'.format(
            ' -> '.join(map(str, best_path)),
        ))
    else:
        sys.stdout.write('No path with length <= {0} found\n'.format(max_depth))


def main():
    """Point of entry, prints some data about social graph."""
    create_db_if_not_exists()

    parser = initialize_parser()
    args = parser.parse_args()

    args.func(args)


if __name__ == '__main__':
    main()
