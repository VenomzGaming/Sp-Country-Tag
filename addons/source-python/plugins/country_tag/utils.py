## IMPORTS
from configobj import ConfigObj
from paths import DATA_PATH, PLUGIN_DATA_PATH
from steam import SteamID
from messages import SayText2

import geoip2.database

from .configs import g_configs

__all__ = (
    'g_country_tags',
    'check_vip',
    'check_admin',
    'get_country',
    'update_tag',
)


## GLOBALS

g_vips = ConfigObj(PLUGIN_DATA_PATH  / 'players.ini', unrepr=True)

g_client_preferences = dict()
g_country_tags = dict()


## UTILS


def check_vip(player):
    if player.steamid != 'BOT':
        try:
            steamid64 = SteamID.parse(player.steamid).to_uint64()
            return bool(g_vips[str(steamid64)]['vip']) if str(steamid64) in g_vips else False
        except:
            return False
    else:
        return False


def check_admin(player):
    if player.steamid != 'BOT':
        try:
            steamid64 = SteamID.parse(player.steamid).to_uint64()
            return bool(g_vips[str(steamid64)]['admin']) if str(steamid64) in g_vips else False
        except:
            return False
    else:
        return False


def get_country(ip):
    if len(ip) == 0:
        return ''
    reader = geoip2.database.Reader(DATA_PATH / 'custom/GeoLite2-City.mmdb')
    response = reader.city(ip)
    return response.country.iso_code


def update_tag(player):
    tag = ''
    if g_configs['admin_tag'].get_int() and check_admin(player):
        tag = g_configs['admin_tag_value'].get_string()
    elif g_configs['vip_tag'].get_int() and check_admin(player):
        tag = g_configs['vip_tag_value'].get_string()
    elif g_configs['country_tag'].get_int():
        tag = g_country_tags[player.userid]
    elif g_configs['player_tag'].get_int() == 0:
        return

    player.clan_tag = tag
