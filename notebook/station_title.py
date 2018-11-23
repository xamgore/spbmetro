from yargy import interpretation as meaning, or_, rule
from yargy.interpretation import fact
from yargy.predicates import normalized
from yargy.rule import Rule

from .common import Array
from .stations import abbreviations as Abbrs, synonyms as Synonyms
from .stations.restore import Restore
from structure import Subway

StationTitle = fact('StationTitle', ['value'])


# todo: fix error
# 'гостиный':                 ['гостинный'],
# 'ладожская':                ['ладожскская'],


def make_rule_from_station(title: str) -> Rule:
    title = title.replace('1', '').replace('2', '').lower().strip()
    phrase = []

    for token in title.split(' '):
        word = Abbrs.get(token) if Abbrs.is_abbr(token) \
            else normalized(token).interpretation(meaning.const(token))
        phrase.append(word.interpretation(Array.element))

    phrase = rule(*phrase).means(Array).interpretation(meaning.custom(
        lambda p: Restore.get(' '.join(p.element))
    )).means(StationTitle.value)

    if Synonyms.has(title):
        synonym = Synonyms.get(title).interpretation(
            meaning.custom(lambda p: Restore.get(p))).means(StationTitle.value)
        return or_(synonym, phrase)

    return phrase


STATION_TITLE = or_(
    *map(make_rule_from_station, Subway.load().stations.keys())
).means(StationTitle)
