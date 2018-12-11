from yargy import or_, rule
from yargy.pipelines import morph_pipeline
from yargy.predicates import caseless, gram, normalized

# Working = fact('Working', [attribute('to', default=[])])

ENTER_EXIT_WORD = rule(
    or_(caseless('на'), caseless('для')).optional(),
    morph_pipeline(['вход', 'выход']),
)

# и на вход и на выход
ON_ENTER_AND_EXIT = rule(
    caseless('и').optional(),
    ENTER_EXIT_WORD,
    # caution: misses comma, I don't know why
    rule(
        caseless('и').optional(),
        ENTER_EXIT_WORD,
    ).optional(),
)

IS_WORKING_OPEN_CLOSED_WORD = morph_pipeline(['работает', 'открыт', 'закрыт'])

NOT_WORD = caseless('не')

WORKING = rule(
    NOT_WORD.optional(),
    normalized('есть').optional(),  # будет, была
    or_(
        # работает в (обычном, нормальном, особом) режиме
        rule(normalized('работает'), caseless('в'), gram('ADJF'), normalized('режим')),
        # работает; работает/открыта/закрыта на вход
        rule(
            IS_WORKING_OPEN_CLOSED_WORD,
            rule(
                caseless('только').optional(),
                ON_ENTER_AND_EXIT,
            ).optional()
        ),
        # на выход не? работает/открыта/закрыта
        rule(
            ON_ENTER_AND_EXIT,
            NOT_WORD.optional(),
            IS_WORKING_OPEN_CLOSED_WORD,
        ),
    ),
)

# todo: remove word "только" and other PRCL from text
# todo: не закрыта -- custom interpretation, inversion of facts
