"""Important constants."""
import types

VK_TOKEN = '*******'
DIR_FRIENDS = 'friends'
CANT_GET_FRIENDS_ERROR_CODES = types.MappingProxyType({
    30: 'private_profile',
    15: 'deleted profile',
})
