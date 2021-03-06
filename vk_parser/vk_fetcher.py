"""Fetch and store some data from vk."""
import vk_api

from vk_parser.config import CANT_GET_FRIENDS_ERROR_CODES, VK_TOKEN
from vk_parser.db_worker import add_friendlist, get_user_friends


def get_friends_no_cache(user_id):
    """Fetch friends with VK API."""
    if not VK_TOKEN:
        return None

    vk_session = vk_api.VkApi(token=VK_TOKEN)
    try:
        response = vk_session.method(
            method='friends.get',
            values={'user_id': user_id},
        )
    except vk_api.VkApiError as ex:
        return [] if ex.code in CANT_GET_FRIENDS_ERROR_CODES else None
    except Exception:
       return None

    return response['items'] if 'items' in response else None


def load_friends(user_id):
    """Load friend-list from file."""
    return get_user_friends(user_id)


def cache_friends(user_id, user_friends):
    """Cache friend-list to file."""
    if user_friends is None:
        return False
    add_friendlist(user_id, user_friends)
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
