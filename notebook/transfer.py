from yargy import or_, rule
from yargy.interpretation import attribute, fact
import yargy.interpretation as meaning
from yargy.predicates import eq, gram, in_, normalized

from .station import FROM_STATION_TO_STATION, LIST_OF_STATIONS, STATION

Transfer = fact('Transfer', [attribute('to', default=[])])

TRANSFER = rule(
    gram('ADJF').optional(),  # пешеходный
    normalized('переход'),
    or_(
        FROM_STATION_TO_STATION.interpretation(Transfer.to),
        rule(
            or_(eq('на'), eq('между'), eq('с')).optional(),
            LIST_OF_STATIONS.interpretation(Transfer.to)
        ),
    ).optional(),
).interpretation(Transfer)

StationAndTransfer = fact('StationAndTransfer', ['station', 'transfer'])

STATION_AND_TRANSFER = rule(
    STATION.interpretation(StationAndTransfer.station),
    rule(
        in_('и,'),
        TRANSFER
            .interpretation(meaning.custom(lambda p: p.to))
            .interpretation(StationAndTransfer.transfer),
    ).optional()
).interpretation(StationAndTransfer)
