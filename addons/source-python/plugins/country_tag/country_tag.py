## IMPORTS

import geoip2.database

from events import Event
from paths import DATA_PATH
from players.entity import Player
from messages import SayText2


from .info import info
from .strings import ANNOUNCE_MESSAGE
from .strings import CONNECT_STEAMID_ANNOUNCE
from .configs import _configs


## GLOBALS

_country_tags = dict()


## GAME EVENT

@Event('player_activate')
def _on_player_activate(event_data):
    player = Player.from_userid(event_data['userid'])
    if not player.steamid == 'BOT':
        return

    if player.userid not in _country_tags:
        _country_tags[player.userid] = get_country(player.address.split(':', 1)[0])

    update_tag(player)


@Event('player_connect_full')
def _on_player_connect(event_data):
    if event_data['index'] == 0:
        return

    player = Player(event_data['index'].get_int())

    if _configs['connection_announce_steamid'].get_int():
        SayText2(CONNECT_STEAMID_ANNOUNCE.format(name=player.name, steamid=player.steamid, country=_country_tags[player.userid].name)).send()

    if _configs['connection_announce'].get_int():
        SayText2(ANNOUNCE_MESSAGE.format(name=player.name, country=_country_tags[player.userid].name)).send()


@Event('player_spawn')
def _on_player_spawn(event_data):
    player = Player.from_userid(event_data['userid'])
    if player.steamid == 'BOT':
        return

    update_tag(player)


## UTILS

def get_country(ip):
    if len(ip) == 0:
        return ''

    reader = geoip2.database.Reader(DATA_PATH / 'custom/GeoLite2-City.mmdb')
    response = reader.city(ip)
    return response.country


def update_tag(player):
    tag = ''
    if _configs['country_tag'].get_int():
        tag = _country_tags[player.userid].iso_code
    elif not _configs['player_tag'].get_int():
        return

    player.clan_tag = tag
