from yargy import or_, rule
from yargy.interpretation import attribute, fact
import yargy.interpretation as meaning
from yargy.pipelines import morph_pipeline
from yargy.predicates import caseless, gram, normalized

from .common import Array

# Working = fact('Working', [attribute('to', default=[])])

Type = fact('Type', [attribute('value', default=[]), 'status', attribute('inversed', default=False)])

ENTER_EXIT_WORD = rule(
    or_(caseless('на'), caseless('для')).optional(),
    morph_pipeline(['вход', 'выход']).interpretation(Type.value),
).interpretation(Type)

# и на вход и на выход
ON_ENTER_AND_EXIT = rule(
    caseless('и').optional(),
    ENTER_EXIT_WORD
        .interpretation(meaning.custom(lambda p: p.value))
        .interpretation(Array.element),
    # caution: misses comma, I don't know why
    rule(
        caseless('и').optional(),
        ENTER_EXIT_WORD
            .interpretation(meaning.custom(lambda p: p.value))
            .interpretation(Array.element),
    ).optional(),
).interpretation(Array)

IS_WORKING_OPEN_CLOSED_DICT = {
    'работать': 'работает',
    'открытый': 'открыт',
    'закрытый': 'закрыт'
}

IS_WORKING_OPEN_CLOSED_WORD = morph_pipeline(['работает', 'открыт', 'закрыт'])

NOT_WORD = caseless('не')

WORKING = rule(
    NOT_WORD.optional()
        .interpretation(Type.inversed.const(True)),
    normalized('есть').optional(),  # будет, была
    or_(
        # работает в (обычном, нормальном, особом) режиме
        rule(normalized('работает'), caseless('в'), gram('ADJF'), normalized('режим'))
            .interpretation(Type.status.const(IS_WORKING_OPEN_CLOSED_DICT['работать'])),
        # работает; работает/открыта/закрыта на вход
        rule(
            IS_WORKING_OPEN_CLOSED_WORD
                .interpretation(Type.status.normalized().custom(IS_WORKING_OPEN_CLOSED_DICT.__getitem__)),
            rule(
                caseless('только').optional(),
                ON_ENTER_AND_EXIT
                    .interpretation(Type.value.custom(lambda p: p.element)),
            ).optional()
        ),
        # на выход (не)? работает/открыта/закрыта
        rule(
            ON_ENTER_AND_EXIT
                .interpretation(Type.value.custom(lambda p: p.element)),
            NOT_WORD.optional()
                .interpretation(Type.inversed.const(True)),
            IS_WORKING_OPEN_CLOSED_WORD
                .interpretation(Type.status.normalized().custom(IS_WORKING_OPEN_CLOSED_DICT.__getitem__)),
        ),
    ),
).interpretation(Type)

# todo: remove word "только" and other PRCL from text
# todo: не закрыта -- custom interpretation, inversion of facts
