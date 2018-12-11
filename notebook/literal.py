from typing import Union
from yargy import interpretation as interp, or_, rule
from yargy.interpretation import attribute, fact
import yargy.interpretation as meaning
from yargy.predicates import Predicate, dictionary, eq, in_caseless, type
from yargy.rule import Rule


def connect(operand: Union[Rule, type], operation: Predicate):
    return rule(
        rule(operand.optional(), operation).optional(),
        operand,
    )


Nums = fact('Nums', [attribute('values').repeatable()])

__literals = {
    'один':   1,
    'два':    2,
    'три':    3,
    'четыре': 4,
    'пять':   5,
    'шесть':  6,
    'семь':   7,
    'восемь': 8,
    'девять': 9,
}

LITERAL = dictionary(__literals).means(
    interp.normalized().custom(__literals.get))

CONJ_NUMS = in_caseless('-и,')

NUMERAL = or_(*[eq(str(i)) for i in __literals.values()]).means(interp.custom(int))

# вестибюль 1 и 2
LIST_OF_NUMERALS = connect(NUMERAL.means(Nums.values), CONJ_NUMS) \
    .means(Nums).means(meaning.custom(lambda p: list(sorted(set(p.values)))))

# первый и второй вестибюли
LIST_OF_LITERALS = connect(LITERAL.means(Nums.values), CONJ_NUMS) \
    .means(Nums).means(meaning.custom(lambda p: list(sorted(set(p.values)))))
