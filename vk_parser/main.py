"""Script that parse vk friends and friends of frends and ..."""
import sys
from queue import Queue

from vk_parser.args import initialize_parser
from vk_parser.vk_fetcher import get_friends


def process_user(user_id, max_depth, ignore_cache=False):
    """Bfs through social graph of user."""
    que = Queue()
    que.put(user_id)
    depth = {}
    depth[user_id] = 0
    parent = {}
    parent[user_id] = -1
    while not que.empty():
        cur_id = que.get()
        if depth[cur_id] == max_depth:
            break
        neighbours = get_friends(cur_id, ignore_cache=ignore_cache)
        for new_id in neighbours:
            if new_id not in depth:
                depth[new_id] = depth[cur_id] + 1
                parent[new_id] = cur_id
                que.put(new_id)
    return depth, parent


def fetch(user_id, max_depth, ignore_cache):
    """Fetch friends for user and print its size."""
    social_graph, _ = process_user(
        user_id=user_id,
        max_depth=max_depth,
        ignore_cache=ignore_cache,
    )
    sys.stdout.write('{0} users by dist <= {1}\n'.format(
        len(social_graph),
        max_depth,
    ))


def get_path(vertex, parent):
    """Get path to start from vertex."""
    path = []
    vertex = parent[vertex]

    while vertex != -1:
        path.append(vertex)
        vertex = parent[vertex]

    return path[::-1]


def calculate_dist(user_id1, user_id2, max_depth, ignore_cache):
    """Calculate dist and path between two users."""
    max_depth1 = max_depth // 2
    max_depth2 = max_depth - max_depth1

    social_graph1, parent1 = process_user(
        user_id=user_id1,
        max_depth=max_depth1,
        ignore_cache=ignore_cache,
    )

    social_graph2, parent2 = process_user(
        user_id=user_id2,
        max_depth=max_depth2,
        ignore_cache=ignore_cache,
    )

    dist = None
    best_path = None
    for (connector, dist1) in social_graph1.items():
        if connector in social_graph2:
            new_dist = dist1 + social_graph2.get(connector)
            if dist is None or new_dist < dist:
                dist = new_dist
                path1 = get_path(connector, parent1)
                path2 = get_path(connector, parent2)
                best_path = path1 + [connector] + path2[::-1]

    sys.stdout.write('Shortest path have {0} edges:\n'.format(dist))

    if best_path:
        sys.stdout.write('{0}\n'.format(
            ' -> '.join(map(str, best_path)),
        ))


def main():
    """Point of entry, prints some data about social graph."""
    parser = initialize_parser()
    args = parser.parse_args()

    if args.command == 'fetch':
        fetch(args.id, args.depth, args.ignore_cache)

    if args.command == 'dist':
        calculate_dist(args.id1, args.id2, args.depth, args.ignore_cache)


if __name__ == '__main__':
    main()
