from Levenshtein import distance
from typing import List, Set


def fix_text(tokens: List, spell_dict: Set[str]):
    res = []
    i, l = 0, len(tokens)
    while i < l:
        token = tokens[i].value
        token_low = token.lower()

        for word in spell_dict:
            dist = distance(word, token_low)

            if dist == 0:
                break  # words are equal, no fix required
            if dist <= 1 and len(token) < len(word):
                token = word  # one mistake, in the middle of the word
                break

            ## helps to detect mistakes in texts
            # if len(token) < len(word) and word.startswith(token_low):
            #     if (i + 2 < l) and (tokens[i + 1].value == '-'):
            #         end = tokens[i + 2].value
            #         if len(end) < len(word) and word.endswith(end.lower()):
            #             print(token, word)
            #             token = word
            #             i += 2
            #             break  # abbreviature: ин-тут, о-в остров
            #
            #     if len(token) >= 2:
            #         if (i + 1 < l) and tokens[i + 1].value == '.' \
            #             and token_low not in ['пл', 'ст', 'пр']:  # площадь станция проспект
            #             print(token, word)
            #             token = word
            #             i += 1
            #             break  # abbreviation: short words with dot
            #
            #         if len(token) >= 3:
            #             parsed = Parser(rule(
            #                 not_(or_(gram('PREP'), gram('NPRO'), gram('Geox'))),
            #             )).match(token)
            #
            #             if parsed and len(token) > 3 or len(token) / len(word) > 0.7:
            #                 print(token, word)
            #                 token = word  # prefix of the spell dictionary word
            #             break

        res.append(token)
        i += 1

    return ' '.join(res)
