from more_itertools import intersperse, partition
from typing import Dict, List
from yargy import interpretation, or_, rule
from yargy.predicates import caseless, eq, normalized
from yargy.rule import Rule

abbreviations = {
    'александра':      ['ал'],
    'владимирская':    ['влад'],
    'гостиный':        ['г', 'гост'],
    'двор':            ['дв'],
    'деревня':         ['дер'],
    'институт':        ['и-т', 'ин-т', 'инст'],
    'остров':          ['о-в'],
    'площадь':         ['пл'],
    'проспект':        ['пр'],
    'старая':          ['ст'],
    'технологический': ['тн', 'техн', 'технолог', 'технологич'],  # тех - FP
    'улица':           ['ул'],
}

# words, that can be missed in a text without loss of meaning
optional = {'двор', 'институт', 'проспект', 'площадь', 'улица'}


def _abbreviate(word: str, abbrs: List[str], opt=False):
    abbrs, dashed = partition(lambda abbr: '-' in abbr, abbrs)
    dashed = map(lambda a: rule(*map(caseless, intersperse('-', a.split('-')))), dashed)

    original_word = rule(normalized(word))
    dashed_sequence = rule(or_(*dashed))
    abbr_with_dot = rule(
        or_(*map(caseless, abbrs)),
        eq('.').optional(),
    )

    result = or_(original_word, dashed_sequence, abbr_with_dot) \
        .interpretation(interpretation.const(word))

    return result.optional() if opt else result


def _rules() -> Dict[str, Rule]:
    return {k: _abbreviate(k, v, opt=k in optional) for k, v in abbreviations.items()}


def get(token) -> Rule:
    return _rules()[token]


def is_abbr(token: str) -> bool:
    return token in abbreviations
