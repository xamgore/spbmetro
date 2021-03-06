from yargy import or_, rule
from yargy.interpretation import fact
from yargy.predicates import caseless, gram

from notebook.common import gnc
from notebook.time import TIME

Duration = fact('Duration', ['since', 'to'])

FROM = rule(
    or_(caseless('от'), caseless('с')),
    TIME.means(Duration.since),
)

UNTIL_PREP = or_(caseless('до'), caseless('по'))

UNTIL_TIME = rule(
    UNTIL_PREP,
    TIME.means(Duration.to),
)

UNTIL_WORD = rule(
    UNTIL_PREP,
    or_(
        gram('ADJF'),
        gram('NOUN'),
    ).match(gnc).repeatable(max=4)
).means(Duration.to)

DURATION = or_(
    rule(
        FROM,
        UNTIL_WORD.optional()
    ),
    rule(
        FROM.optional(),
        UNTIL_TIME,
    )
).means(Duration).named('DURATION')
