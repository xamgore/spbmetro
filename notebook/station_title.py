from yargy import interpretation as meaning, or_, rule
from yargy.interpretation import attribute, fact
from yargy.predicates import normalized
from yargy.rule import Rule

from notebook.stations import abbreviations as Abbrs, synonyms as Synonyms
from notebook.stations.restore import Restore
from structure import Subway

Phrase = fact('Phrase', [attribute('words').repeatable()])

Station = fact('Station', ['title'])


# todo: fix error
# 'гостиный':                 ['гостинный'],
# 'ладожская':                ['ладожскская'],


def make_rule_from_station(title: str) -> Rule:
    title = title.replace('1', '').replace('2', '').lower().strip()
    phrase = []

    for token in title.split(' '):
        word = Abbrs.get(token) if Abbrs.is_abbr(token) \
            else normalized(token).interpretation(meaning.const(token))
        phrase.append(word.interpretation(Phrase.words))

    phrase = rule(*phrase).means(Phrase).interpretation(meaning.custom(
        lambda p: Restore.get(' '.join(p.words))
    )).means(Station.title)

    if Synonyms.has(title):
        synonym = Synonyms.get(title).interpretation(
            meaning.custom(lambda p: Restore.get(p))).means(Station.title)
        return or_(synonym, phrase)

    return phrase


STATION_TITLE = or_(
    *map(make_rule_from_station, Subway.load().stations.keys())
).means(Station)

# nums_rule = connect(ONE_OR_TWO.means(Station.num), CONJ_NUMS).optional()


# LITERAL = dictionary(PROSPECT_WORDS).means(
#     interpretation.normalized().custom(LITERALS.get)
# )

# STATION = rule(
#     VESTIBULE.optional(),
#     or_(
#         rule(
#             STATION_WORD.optional(),
#             METRO_WORD.optional(),
#             STATION_TITLE,
#         ),
#         #         rule(
#         #             STATION_WORD,
#         #             METRO_WORD.optional(),
#         #             or_(
#         #                 rule(gram('NOUN')),
#         #                 rule(gram('ADJF')),
#         #                 STREET_WORD,
#         #                 PROSPECT_WORD
#         #             ).repeatable(max=3)
#         #         ),
#     ),
#     rule(
#         eq('-').optional(),
#         rule(
#             type('INT'),
#             in_('-,и'),
#         ).optional(),
#         type('INT'),
#     ).optional(),
# ).named('STATION')
