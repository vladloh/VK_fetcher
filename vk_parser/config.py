"""Important constants."""
import types

VK_TOKEN = '662f0d39662f0d39662f0d39bf664121a36662f662f0d393bf5264d2dffbae81b0a5917'
DATABASE_PATH = 'friendlists.db'
DATABASE_NAME = 'friends'
CANT_GET_FRIENDS_ERROR_CODES = types.MappingProxyType({
    30: 'private_profile',
    15: 'deleted profile',
})
