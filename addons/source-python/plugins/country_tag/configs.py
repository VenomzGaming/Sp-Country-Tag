## IMPORTS

from config.manager import ConfigManager
from translations.strings import LangStrings


from .info import info

## ALL DECLARATION

__all__ = (
    '_configs',
)

## GLOBALS

_configs = dict()

with ConfigManager(info.name) as _config:

    #
    #   Tags
    #
    _config.section('Tags')

    _configs['player_tag'] = _config.cvar(
        'player_tag', 1,
        '1 - Remove player tag | 0 - Don\'t remove player tag')

    _configs['country_tag'] = _config.cvar(
        'country_tag', 1,
        '1 - Enable country tag | 0 - Disable country tag')

    #
    #   Connection announce
    #
    _config.section('Announce Message')

    _configs['connection_announce'] = _config.cvar(
        'connection_announce', 0,
        '1 - Enable country announce on connection | 0 - Disable country announce on connection')

    _configs['connection_announce_steamid'] = _config.cvar(
        'connection_announce_steamid', 1,
        '1 - Enable steamid showing | 0 - Disable steamid showing')
