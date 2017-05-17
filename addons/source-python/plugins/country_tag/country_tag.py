## IMPORTS

import geoip2.database
from geoip2.errors import AddressNotFoundError

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


## LOAD
def load():
    for player in _human_players:
        init_player_clan_tag(player)
        update_clan_tag(player)


## GAME EVENT

@Event('player_activate')
def _on_player_activate(event_data):
    player = Player.from_userid(event_data['userid'])

    if player.is_bot():
        return

    if player.userid not in _country_tags:
        try:
            tag = init_player_clan_tag(player)
        except AddressNotFoundError:
            # TODO: Log a warning?
            return

        if _configs['connection_announce_steamid'].get_int():
            CONNECT_STEAMID_ANNOUNCE.send(
                _human_players,
                name=player.name,
                steamid=player.steamid,
                country=tag.name,
            )

        if _configs['connection_announce'].get_int():
            CONNECT_ANNOUNCE.send(
                _human_players,
                name=player.name,
                country=tag.name,
            )

    update_clan_tag(player)

@Event('player_disconnect')
def _on_player_disconnect(event_data):
    _country_tags.pop(event_data['userid'], 0)


@Event('player_spawn')
def _on_player_spawn(event_data):
    update_clan_tag(Player.from_userid(event_data['userid']))


## UTILS

def get_country(ip):
    if len(ip) == 0:
        return ''

    reader = geoip2.database.Reader(DATA_PATH / 'custom/GeoLite2-City.mmdb')
    response = reader.city(ip)
    return response.country


def update_clan_tag(player):
    if player.userid not in _country_tags:
        return

    tag = ''
    if _configs['country_tag'].get_int():
        tag = _country_tags[player.userid].iso_code
    elif not _configs['player_tag'].get_int():
        return

    try:
        player.clan_tag = tag
    except AttributeError:
        pass


def init_player_clan_tag(player):
    result = _country_tags[player.userid] = get_country(
        player.address.split(':', 1)[0])
    return result
