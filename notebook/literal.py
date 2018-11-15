from yargy.predicates import dictionary, in_, type, eq
from yargy import interpretation as interp, or_

LITERALS = {
    'один': 1,
    'два': 2,
    'три': 3
}

LITERAL = dictionary(LITERALS).means(
    interp.normalized().custom(LITERALS.get)
)

CONJ_NUMS = in_('-и,')
ONE_OR_TWO = or_(eq('1'), eq('2')).means(interp.custom(int))
