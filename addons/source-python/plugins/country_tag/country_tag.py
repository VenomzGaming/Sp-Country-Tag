## IMPORTS

import geoip2.database

from core import GAME_NAME
from events import Event
from paths import DATA_PATH
from filters.players import PlayerIter
from messages import SayText2
from players.entity import Player


from .info import info
from .strings import CONNECT_ANNOUNCE
from .strings import CONNECT_STEAMID_ANNOUNCE
from .configs import _configs


## GLOBALS

_country_tags = dict()
_human_players = PlayerIter('human')

## GAME MANAGEMENT

EVENT_CONNECT_GAME = 'player_connect_client'

if GAME_NAME in ('csgo', 'left4dead', 'left4dead2', ):
    EVENT_CONNECT_GAME = 'player_connect_full'


HAS_CLAN_TAG = False

if GAME_NAME in ('csgo', 'cstrike', ):
    HAS_CLAN_TAG = True


## GAME EVENT

@Event(EVENT_CONNECT_GAME)
def _on_player_connect_full(event_data):
    if event_data['userid'] == 0:
        return

    player = Player.from_userid(event_data['userid'])

    if player.steamid == 'BOT':
        return

    if player.userid not in _country_tags:
        _country_tags[player.userid] = get_country(player.address.split(':', 1)[0])

    if HAS_CLAN_TAG:
        update_tag(player)

    if _configs['connection_announce_steamid'].get_int():
        CONNECT_STEAMID_ANNOUNCE.send(
            _human_players,
            name=player.name,
            steamid=player.steamid,
            country=_country_tags[player.userid].name,
        )

    if _configs['connection_announce'].get_int():
        CONNECT_ANNOUNCE.send(
            _human_players,
            name=player.name,
            country=_country_tags[player.userid].name,
        )


@Event('player_disconnect')
def _on_player_disconnect(event_data):
    player = Player.from_userid(event_data['userid'])

    if player.userid in _country_tags:
        del _country_tags[player.userid]


@Event('player_spawn')
def _on_player_spawn(event_data):
    player = Player.from_userid(event_data['userid'])
    if player.steamid == 'BOT' or player.userid not in _country_tags:
        return

    if HAS_CLAN_TAG:
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
