from typing import Dict, List
from yargy import interpretation, or_, rule
from yargy.predicates import normalized
from yargy.rule import Rule

from notebook.stations.restore import Restore

synonyms = {
    # 'василеостровская':         ['васька'],
    'гостиный двор':            ['гостинка'],
    'гражданский проспект':     ['гражданка'],
    # 'купчино':                  ['купчага'],
    'лиговский проспект':       ['лиговка'],
    'петроградская':            ['петроградка'],
    'технологический институт': ['техноложка'],
}


def _synonymize(word: str, syns: List[str]) -> Rule:
    return rule(or_(*map(normalized, syns))) \
        .interpretation(interpretation.const(word))


def _rules() -> Dict[str, Rule]:
    return {Restore.preprocess(k): _synonymize(k, v) for k, v in synonyms.items()}


def get(token: str):
    return _rules()[Restore.preprocess(token)]


def has(phrase: str):
    return Restore.preprocess(phrase) in _rules()
