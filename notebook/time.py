import sys

import re
from yargy import or_, rule
from yargy.interpretation import fact
from yargy.pipelines import morph_pipeline
from yargy.predicates import caseless, custom, eq, in_

from .common import TOKENIZER

Time = fact('Time', ['hours', 'minutes'])

hour_re = re.compile(r'([01]\d|\d|2[0-3])')
is_hour = custom(hour_re.fullmatch).activate(TOKENIZER)

minute_re = re.compile(r'[0-5]\d')
is_minute = custom(minute_re.fullmatch).activate(TOKENIZER)

HOUR_UNIT = rule(
    morph_pipeline(['ч', 'час', 'часы']),
    eq('.').optional()
)

MINUTE_UNIT = rule(
    morph_pipeline(['м', 'мин', 'минуты']),
    eq('.').optional()
)

# 17:02 ч.
TIME_DIGITAL = rule(
    is_hour.means(Time.hours),
    in_(':-.'),
    is_minute.means(Time.minutes),
    or_(HOUR_UNIT, MINUTE_UNIT).optional(),
).means(Time)

# 17ч 02
TIME_HUMAN = rule(
    is_hour.means(Time.hours),
    HOUR_UNIT,
    is_minute.means(Time.minutes),
    MINUTE_UNIT.optional(),
).means(Time)

# в 15:00
TIME = rule(
    caseless('в').optional(),
    or_(
        TIME_DIGITAL,
        TIME_HUMAN,
    )
).means(Time)

if __name__ == '__main__':
    print(sys.argv)
