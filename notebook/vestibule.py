from yargy import or_, rule
from yargy.interpretation import fact
from yargy.pipelines import morph_pipeline

from .literal import LIST_OF_LITERALS, LIST_OF_NUMERALS

Vestibule = fact('Vestibules', ['num'])

VESTIBULE_WORD = morph_pipeline(['вестибюль'])

VESTIBULE = rule(or_(
    # вестибюль 1 и 2
    rule(
        VESTIBULE_WORD,
        LIST_OF_NUMERALS.means(Vestibule.num).optional(),
    ),
    # первый и второй вестибюли
    rule(
        LIST_OF_LITERALS.means(Vestibule.num),
        VESTIBULE_WORD,
    ),
)).means(Vestibule)

# todo: sort numbers
# todo: павильон
