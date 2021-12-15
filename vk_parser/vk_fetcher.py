"""Fetch and store some data from vk."""
import json
import os

import vk_api

from vk_parser.config import CANT_GET_FRIENDS, DIR_FRIENDS, VK_TOKEN


def create_dir_if_not_exists(directory):
    """Create directory if not exists."""
    os.makedirs(directory, exist_ok=True)


def get_friends_no_cache(user_id):
    """Fetch friends with VK API."""
    vk_session = vk_api.VkApi(token=VK_TOKEN)
    try:
        response = vk_session.method(
            method='friends.get',
            values={'user_id': user_id},
        )
    except vk_api.ApiError as ex:
        return [] if ex.code in CANT_GET_FRIENDS_ERROR_CODES else None
    except Exception:
        return None

    return response['items'] if 'items' in response else None


def load_friends(user_id):
    """Load friend-list from file."""
    path = '{0}/{1}.json'.format(DIR_FRIENDS, user_id)
    try:
        with open(path, 'r') as input_file:
            return json.loads(input_file.read())
    except Exception:
        return None


def cache_friends(user_id, user_friends):
    """Cache friend-list to file."""
    if user_friends is None:
        return False

    path = '{0}/{1}.json'.format(DIR_FRIENDS, user_id)
    create_dir_if_not_exists(DIR_FRIENDS)
    try:
        with open(path, 'w') as out_file:
            out_file.write(json.dumps(user_friends))
    except Exception:
        return False

    return True


def get_friends(user_id, ignore_cache=False):
    """Get friends for user with id=user_id."""
    if ignore_cache:
        user_friends = get_friends_no_cache(user_id)
        cache_friends(user_id, user_friends)
        return user_friends if user_friends else []

    cached_friends = load_friends(user_id)

    if cached_friends is None:
        user_friends = get_friends_no_cache(user_id)
        cache_friends(user_id, user_friends)
        return user_friends if user_friends else []

    return cached_friends
