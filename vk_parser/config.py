"""Important constants."""
import configparser
import types

DATABASE_PATH = 'friendlists.db'
DATABASE_NAME = 'friends'
CANT_GET_FRIENDS_ERROR_CODES = types.MappingProxyType({
    30: 'private_profile',
    15: 'deleted profile',
})

TOKEN_PATH = 'token.cfg'

config = configparser.ConfigParser()
config.read(TOKEN_PATH)

try:
    VK_TOKEN = config['VK_API']['VK_TOKEN']
except Exception:
    print('No VK_TOKEN found. Please add VK_TOKEN to VK_API section in setup.cfg')
    VK_TOKEN = None
