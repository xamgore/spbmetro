from yargy import or_, rule
from yargy.interpretation import attribute, fact
import yargy.interpretation as meaning
from yargy.predicates import eq, in_, normalized

from .common import Array
from .literal import LIST_OF_NUMERALS
from .station_title import STATION_TITLE

Station = fact('Station', ['name', attribute('num', default=[])])

STATION_WORD = or_(
    rule('ст', '.'),
    rule(normalized('станция')),
)

METRO_WORD = or_(
    rule('м', '.'),
    rule(normalized('метро')),
)

STATION = rule(
    STATION_WORD.optional(),
    METRO_WORD.optional(),
    STATION_TITLE
        .interpretation(meaning.custom(lambda p: p.value))
        .interpretation(Station.name),
    rule(
        eq('-').optional(),
        LIST_OF_NUMERALS.interpretation(Station.num),
    ).optional(),
).interpretation(Station)

LIST_OF_STATIONS = rule(
    STATION.means(Array.element),
    rule(
        in_('и,-'),
        STATION.means(Array.element),
    ).repeatable().optional(),
).interpretation(Array).interpretation(meaning.custom(lambda p: p.element))

FROM_STATION_TO_STATION = rule(
    or_(eq('с'), eq('со')),
    STATION.means(Array.element),
    eq('на'),
    STATION.means(Array.element),  # todo LIST_OF_STATIONS: со спасской на садовую и сенную
).interpretation(Array).interpretation(meaning.custom(lambda p: p.element))
