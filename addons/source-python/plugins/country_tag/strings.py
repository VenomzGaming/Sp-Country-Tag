## IMPORTS

from messages import SayText2
from translations.strings import LangStrings


## ALL DECLARATION

__all__ = (
	'CONNECT_ANNOUNCE',
	'CONNECT_STEAMID_ANNOUNCE',
)

## GLOBALS

strings = LangStrings('country_tag')

CONNECT_ANNOUNCE = SayText2(message=strings['Connect Announce'])

CONNECT_STEAMID_ANNOUNCE = SayText2(message=strings['Connect Announce Steamid'])
