from yargy import or_, rule
from yargy.interpretation import attribute, fact
from yargy.pipelines import morph_pipeline
import yargy.interpretation as meaning

from common import connect
from literal import CONJ_NUMS, ONE_OR_TWO, LITERAL

Vestibule = fact('Vestibules', [attribute('num').repeatable()])

VESTIBULE_WORD = morph_pipeline(['вестибюль'])

VESTIBULE = rule(or_(
    # вестибюль 1 и 2
    rule(
        VESTIBULE_WORD,
        connect(ONE_OR_TWO.means(Vestibule.num), CONJ_NUMS).optional(),
    ),
    # первый и второй вестибюли
    rule(
        connect(LITERAL.means(Vestibule.num), CONJ_NUMS),
        VESTIBULE_WORD,
    ),
)).means(Vestibule).means(meaning.custom(lambda p: list(sorted(p.num))))

# todo: sort numbers
# todo: павильон
