from typing import List, Union
from yargy import and_, interpretation, or_, rule
from yargy.pipelines import morph_pipeline
from yargy.predicates import Predicate, caseless, eq, length_eq, normalized, type
from yargy.relations import gnc_relation
from yargy.rule import Rule
from yargy.tokenizer import MorphTokenizer
from yargy.utils import Record

Record.means = lambda self, *args, **kwargs: self.interpretation(*args, **kwargs)

TOKENIZER = MorphTokenizer()  # todo move to notebook
gnc = gnc_relation()


def connect(operand: Union[Rule, type], operation: Predicate):
    return rule(
        rule(operand.optional(), operation).optional(),
        operand,
    )
