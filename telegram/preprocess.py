from Levenshtein import distance
from typing import List, Set
from yargy.token import MorphToken

from common import TOKENIZER
from structure import Subway


def spell_dict() -> Set[str]:
    if not hasattr(spell_dict, 'result'):
        spell_dict.result = \
            {w.lower() for _ in Subway.load().stations.keys() for w in _.split() if not w.isdigit()}
    return spell_dict.result


def fix_text(text: str, spell_dict: Set[str]):
    tokens: List = list(TOKENIZER(text))
    res, offset = list(text[:]), 0
    i, l = 0, len(tokens)

    while i < l:
        token: MorphToken = (tokens[i])
        value = token.value
        value_low = value.lower()

        for word in spell_dict:
            if 0 <= distance(word, value_low) <= 1:
                # 0 - words are equal, no fix required
                # 1 - if len(value) <= len(word), then one letter is missed inside (комендан[т]ский)
                #     if len(value) >  len(word), then one letter is wrongly typed (ладож[к]ская)
                #         this changes двору -> двор, but that's ok as we parse normalized forms
                value = word
                break

            ## helps to detect mistakes in texts
            # if len(value) < len(word) and word.startswith(value_low):
            #     if (i + 2 < l) and (tokens[i + 1].value == '-'):
            #         end = tokens[i + 2].value
            #         if len(end) < len(word) and word.endswith(end.lower()):
            #             print(value, word)
            #             value = word
            #             i += 2
            #             break  # abbreviature: ин-тут, о-в остров
            #
            #     if len(value) >= 2:
            #         if (i + 1 < l) and tokens[i + 1].value == '.' \
            #             and value_low not in ['пл', 'ст', 'пр']:  # площадь станция проспект
            #             print(value, word)
            #             value = word
            #             i += 1
            #             break  # abbreviation: short words with dot
            #
            #         if len(value) >= 3:
            #             parsed = Parser(rule(
            #                 not_(or_(gram('PREP'), gram('NPRO'), gram('Geox'))),
            #             )).match(value)
            #
            #             if parsed and len(value) > 3 or len(value) / len(word) > 0.7:
            #                 print(value, word)
            #                 value = word  # prefix of the spell dictionary word
            #             break

        res[offset + token.span[0]:offset + token.span[1]] = value
        offset += len(value) - len(value_low)
        i += 1

    return ''.join(res)
